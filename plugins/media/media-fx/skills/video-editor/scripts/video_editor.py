#!/usr/bin/env python3
"""
Video Auto-Editor: Whisper-based automated video editing with TTS support.

Analyzes video/audio with Whisper STT to detect and remove silence gaps,
retakes/duplicates, and garbage segments. Optionally replaces narration
with AI-generated TTS audio and trims silence dynamically.

Subcommands:
  analyze       - Transcribe and analyze video for edit opportunities
  execute       - Execute an edit plan to produce edited video
  tts-prepare   - Prepare TTS segments from whisper data and edit plan
  tts-generate  - Generate TTS audio and create video with new narration
  trim-silence  - Trim silence with dynamic or fixed caps
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
import time
import wave
from pathlib import Path


# ──────────────────────────────────────────────
# Utilities
# ──────────────────────────────────────────────

def fmt_time(seconds):
    """Format seconds to M:SS.ss"""
    m, s = divmod(seconds, 60)
    return f"{int(m)}:{s:05.2f}"


def get_duration(filepath):
    """Get media duration in seconds via ffprobe."""
    cmd = [
        "ffprobe", "-v", "quiet",
        "-show_format", "-print_format", "json",
        filepath
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffprobe failed: {result.stderr}")
    return float(json.loads(result.stdout)["format"]["duration"])


def get_media_info(filepath):
    """Get video/audio stream info."""
    cmd = [
        "ffprobe", "-v", "quiet",
        "-show_format", "-show_streams", "-print_format", "json",
        filepath
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffprobe failed: {result.stderr}")
    data = json.loads(result.stdout)
    info = {
        "duration": float(data["format"]["duration"]),
        "size_mb": int(data["format"]["size"]) / 1024 / 1024,
    }
    for s in data["streams"]:
        if s["codec_type"] == "video":
            info["video"] = f"{s['codec_name']} {s['width']}x{s['height']}"
            info["has_video"] = True
        elif s["codec_type"] == "audio":
            info["audio"] = f"{s['codec_name']} {s.get('sample_rate', '?')}Hz"
    if "has_video" not in info:
        info["has_video"] = False
    return info


def extract_audio(input_path, output_path):
    """Extract audio from video as WAV for Whisper."""
    cmd = [
        "ffmpeg", "-y",
        "-i", input_path,
        "-vn", "-acodec", "pcm_s16le",
        "-ar", "16000", "-ac", "1",
        output_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Audio extraction failed: {result.stderr[-300:]}")


# ──────────────────────────────────────────────
# Korean Text Analysis (for dynamic silence caps)
# ──────────────────────────────────────────────

SENTENCE_ENDINGS = (
    '니다', '습니다', '겁니다', '봅니다',
    '해요', '돼요', '네요', '군요', '나요',
    '예요', '거예요', '볼게요', '할게요', '드릴게요', '할거예요',
    '겠죠', '이죠', '거죠', '하죠', '있죠', '같죠', '맞죠',
    '세요', '주세요', '하세요', '보세요',
    '시다', '읍시다', '봅시다', '볼까요',
    '거든요', '잖아요', '던데요', '텐데요',
    '구요', '있구요',
)

COMMA_CONNECTORS = ('고,', '서,', '면,', '며,', '지만,', '는데,', '니까,', '으며,')

CONTINUE_PARTICLES = (
    '고', '서', '면', '는데', '니까', '지만', '하여', '해서', '으며',
    '으로', '에서', '과', '와', '의', '를', '을', '에', '는', '은',
    '부터', '까지', '처럼', '만큼', '대로', '하고', '때문에',
    '위해', '통해', '따라', '관해', '대해',
)


def classify_ending(text, cap_sentence=0.5, cap_comma=0.3, cap_continue=0.15):
    """Classify Korean text ending to determine appropriate silence cap.

    Returns (cap_seconds, reason_string).
    """
    text = text.strip()
    if not text:
        return cap_continue, "empty"

    if text[-1] in '.!?':
        return cap_sentence, "punctuation"

    for conn in COMMA_CONNECTORS:
        if text.endswith(conn):
            return cap_comma, "comma"

    for suffix in SENTENCE_ENDINGS:
        if text.endswith(suffix):
            return cap_sentence, "ending"

    for particle in CONTINUE_PARTICLES:
        if text.endswith(particle):
            return cap_continue, "continuing"

    return cap_continue, "other"


def original_to_edited(original_time, edit_plan):
    """Convert original video timestamp to edited video timestamp.

    Returns edited timestamp, or None if the time falls in a REMOVE range.
    """
    removed = 0.0
    for entry in edit_plan:
        if original_time < entry["start"]:
            break
        if entry["action"] == "REMOVE":
            if original_time < entry["end"]:
                return None
            removed += entry["end"] - entry["start"]
        elif entry["action"] == "KEEP":
            if original_time <= entry["end"]:
                break
    return round(original_time - removed, 2)


# ──────────────────────────────────────────────
# Analyze Command
# ──────────────────────────────────────────────

def find_silence_gaps(segments, min_gap=2.0):
    """Find silence gaps between segments."""
    gaps = []
    for i in range(1, len(segments)):
        gap = segments[i]["start"] - segments[i - 1]["end"]
        if gap > min_gap:
            gaps.append({
                "start": segments[i - 1]["end"],
                "end": segments[i]["start"],
                "duration": round(gap, 2),
                "before_seg": i - 1,
                "after_seg": i,
                "before_text": segments[i - 1]["text"].strip()[:50],
                "after_text": segments[i]["text"].strip()[:50],
            })
    return gaps


def find_duplicates(segments, min_chars=15):
    """Find duplicate/retake segments by text similarity."""
    dupes = []
    for i in range(len(segments)):
        for j in range(i + 1, len(segments)):
            t1 = segments[i]["text"].strip()
            t2 = segments[j]["text"].strip()
            if len(t1) > min_chars and len(t2) > min_chars:
                if t1[:min_chars] == t2[:min_chars]:
                    dupes.append({
                        "first_seg": i,
                        "first_start": segments[i]["start"],
                        "first_end": segments[i]["end"],
                        "first_text": t1[:60],
                        "second_seg": j,
                        "second_start": segments[j]["start"],
                        "second_end": segments[j]["end"],
                        "second_text": t2[:60],
                    })
    return dupes


def find_garbage_segments(segments):
    """Find short or garbled segments."""
    garbage = []
    # Characters that indicate Whisper hallucination
    hallucination_chars = ["�", "ème", "oken", "émissions", "ièrement", "בת", "стр"]
    for i, seg in enumerate(segments):
        text = seg["text"].strip()
        dur = seg["end"] - seg["start"]
        is_garbage = False
        reason = ""

        if dur < 0.3:
            is_garbage = True
            reason = f"too_short ({dur:.2f}s)"
        elif len(text) < 2:
            is_garbage = True
            reason = "empty_text"
        elif any(c in text for c in hallucination_chars):
            is_garbage = True
            reason = "hallucination"

        if is_garbage:
            garbage.append({
                "seg": i,
                "start": seg["start"],
                "end": seg["end"],
                "duration": round(dur, 2),
                "text": text[:60],
                "reason": reason,
            })
    return garbage


def generate_edit_plan(segments, gaps, dupes, garbage, long_silence_threshold=10.0):
    """
    Generate a KEEP/REMOVE edit plan.

    Rules:
    - Silence gaps > long_silence_threshold → REMOVE
    - First takes of duplicates → REMOVE (keep last take)
    - Garbage segments → REMOVE
    - Everything else → KEEP
    """
    total_duration = segments[-1]["end"] if segments else 0

    # Collect all time ranges to remove
    remove_ranges = []

    # 1. Long silence gaps
    for gap in gaps:
        if gap["duration"] >= long_silence_threshold:
            remove_ranges.append({
                "start": gap["start"],
                "end": gap["end"],
                "note": f"무음 {gap['duration']:.1f}초",
            })

    # 2. First takes of duplicates (keep the last occurrence)
    # Group duplicates by their first 15 chars to find retake groups
    retake_groups = {}
    for d in dupes:
        key = d["first_text"][:15]
        if key not in retake_groups:
            retake_groups[key] = []
        retake_groups[key].append(d)

    for key, group in retake_groups.items():
        # Find all segment indices involved
        all_segs = set()
        for d in group:
            all_segs.add((d["first_seg"], d["first_start"], d["first_end"]))
            all_segs.add((d["second_seg"], d["second_start"], d["second_end"]))
        # Sort by start time, keep the last one
        sorted_segs = sorted(all_segs, key=lambda x: x[1])
        # Remove all except the last
        for seg_idx, start, end in sorted_segs[:-1]:
            remove_ranges.append({
                "start": start,
                "end": end,
                "note": f"리테이크 1차 (seg {seg_idx})",
            })

    # 3. Garbage segments
    for g in garbage:
        remove_ranges.append({
            "start": g["start"],
            "end": g["end"],
            "note": f"가비지: {g['reason']}",
        })

    # Sort and merge overlapping remove ranges
    remove_ranges.sort(key=lambda x: x["start"])
    merged = []
    for r in remove_ranges:
        if merged and r["start"] <= merged[-1]["end"] + 1.0:
            # Merge with previous (extend end, combine notes)
            if r["end"] > merged[-1]["end"]:
                merged[-1]["end"] = r["end"]
                merged[-1]["note"] += " + " + r["note"]
        else:
            merged.append(dict(r))

    # Also merge adjacent removes with the silence gaps between them
    # If two REMOVE ranges are separated by a gap that's also flagged, merge them
    final_removes = []
    for r in merged:
        if final_removes and r["start"] - final_removes[-1]["end"] < 2.0:
            final_removes[-1]["end"] = r["end"]
            final_removes[-1]["note"] += " + " + r["note"]
        else:
            final_removes.append(dict(r))

    # Build KEEP/REMOVE plan
    plan = []
    pos = 0.0
    for r in final_removes:
        if r["start"] > pos + 0.5:
            plan.append({
                "action": "KEEP",
                "start": round(pos, 2),
                "end": round(r["start"], 2),
                "note": "",
            })
        plan.append({
            "action": "REMOVE",
            "start": round(r["start"], 2),
            "end": round(r["end"], 2),
            "note": r["note"],
        })
        pos = r["end"]

    # Final KEEP segment
    if pos < total_duration - 0.5:
        plan.append({
            "action": "KEEP",
            "start": round(pos, 2),
            "end": round(total_duration, 2),
            "note": "",
        })

    return plan


def cmd_analyze(args):
    """Transcribe and analyze video/audio for edit opportunities."""
    input_path = args.input
    if not os.path.exists(input_path):
        print(f"Error: File not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    info = get_media_info(input_path)
    print(f"Input: {input_path}")
    print(f"  Duration: {info['duration']:.1f}s ({info['duration']/60:.1f}min)")
    print(f"  Size: {info['size_mb']:.0f}MB")
    if info["has_video"]:
        print(f"  Video: {info.get('video', 'N/A')}")
    print(f"  Audio: {info.get('audio', 'N/A')}")
    print()

    # Extract audio if video
    audio_path = input_path
    tmp_audio = None
    if info["has_video"]:
        tmp_audio = tempfile.mktemp(suffix=".wav")
        print("Extracting audio from video...")
        extract_audio(input_path, tmp_audio)
        audio_path = tmp_audio

    # Run Whisper
    try:
        import whisper
    except ImportError:
        print("Error: Whisper not installed. Run: pip install openai-whisper", file=sys.stderr)
        sys.exit(1)

    model_name = args.whisper_model
    print(f"Loading Whisper {model_name} model...")
    t0 = time.time()
    model = whisper.load_model(model_name)
    print(f"Model loaded in {time.time()-t0:.1f}s")

    print(f"Transcribing ({info['duration']/60:.1f} min)...")
    t1 = time.time()
    result = model.transcribe(
        audio_path,
        language=args.language,
        word_timestamps=True,
        verbose=False,
    )
    print(f"Transcription done in {time.time()-t1:.1f}s")
    print(f"Segments: {len(result['segments'])}")

    segments = result["segments"]
    total_words = sum(len(s.get("words", [])) for s in segments)
    print(f"Total words: {total_words}")
    print()

    # Cleanup temp audio
    if tmp_audio and os.path.exists(tmp_audio):
        os.remove(tmp_audio)

    # Analyze
    print("=" * 60)
    print("Analysis")
    print("=" * 60)

    gaps = find_silence_gaps(segments, min_gap=args.min_gap)
    dupes = find_duplicates(segments)
    garbage = find_garbage_segments(segments)

    print(f"\n1. Silence Gaps (>{args.min_gap}s): {len(gaps)}개")
    for g in gaps:
        print(f"   {fmt_time(g['start'])} ~ {fmt_time(g['end'])} ({g['duration']:.1f}s)")

    print(f"\n2. Duplicates/Retakes: {len(dupes)}개")
    seen_pairs = set()
    for d in dupes:
        pair = (d["first_seg"], d["second_seg"])
        if pair not in seen_pairs:
            seen_pairs.add(pair)
            print(f"   seg[{d['first_seg']}] {fmt_time(d['first_start'])} vs seg[{d['second_seg']}] {fmt_time(d['second_start'])}")
            print(f"     \"{d['first_text']}\"")

    print(f"\n3. Garbage Segments: {len(garbage)}개")
    for g in garbage:
        print(f"   seg[{g['seg']}] {fmt_time(g['start'])} ({g['reason']}): \"{g['text']}\"")

    # Generate edit plan
    print(f"\n{'=' * 60}")
    print("Edit Plan (auto-generated)")
    print("=" * 60)

    plan = generate_edit_plan(
        segments, gaps, dupes, garbage,
        long_silence_threshold=args.silence_threshold,
    )

    keep_total = sum(e["end"] - e["start"] for e in plan if e["action"] == "KEEP")
    remove_total = sum(e["end"] - e["start"] for e in plan if e["action"] == "REMOVE")
    keep_count = sum(1 for e in plan if e["action"] == "KEEP")

    print(f"Original: {info['duration']:.0f}s ({info['duration']/60:.1f}min)")
    print(f"KEEP: {keep_total:.0f}s ({keep_total/60:.1f}min) - {keep_count}개 구간")
    print(f"REMOVE: {remove_total:.0f}s ({remove_total/60:.1f}min)")
    print(f"Result: ~{keep_total/60:.1f}min ({keep_total/info['duration']*100:.0f}%)")
    print()

    for e in plan:
        dur = e["end"] - e["start"]
        marker = "V" if e["action"] == "KEEP" else "X"
        print(f"  {marker} {e['action']:6s} [{fmt_time(e['start'])} ~ {fmt_time(e['end'])}] {dur:6.1f}s  {e['note']}")

    # Save outputs
    output_base = args.output or os.path.splitext(input_path)[0]

    # Save transcription
    transcript_path = output_base + "_whisper.json"
    with open(transcript_path, "w") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"\nTranscription saved: {transcript_path}")

    # Save analysis
    analysis = {
        "input": input_path,
        "duration": info["duration"],
        "segments_count": len(segments),
        "words_count": total_words,
        "gaps": gaps,
        "duplicates": dupes,
        "garbage": garbage,
    }
    analysis_path = output_base + "_analysis.json"
    with open(analysis_path, "w") as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2)
    print(f"Analysis saved: {analysis_path}")

    # Save edit plan
    plan_path = output_base + "_edit_plan.json"
    with open(plan_path, "w") as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)
    print(f"Edit plan saved: {plan_path}")

    print(f"\nNext step: Review the edit plan, then run:")
    print(f"  python video_editor.py execute \"{input_path}\" \"{plan_path}\"")


# ──────────────────────────────────────────────
# Execute Command
# ──────────────────────────────────────────────

def cmd_execute(args):
    """Execute an edit plan to produce the edited video/audio."""
    input_path = args.input
    plan_path = args.plan

    if not os.path.exists(input_path):
        print(f"Error: File not found: {input_path}", file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(plan_path):
        print(f"Error: Plan not found: {plan_path}", file=sys.stderr)
        sys.exit(1)

    with open(plan_path) as f:
        plan = json.load(f)

    info = get_media_info(input_path)
    keep_segments = [e for e in plan if e["action"] == "KEEP"]

    if not keep_segments:
        print("Error: No KEEP segments in plan", file=sys.stderr)
        sys.exit(1)

    print(f"Input: {input_path}")
    print(f"  Duration: {info['duration']:.1f}s ({info['duration']/60:.1f}min)")
    print(f"  KEEP segments: {len(keep_segments)}")

    keep_total = sum(e["end"] - e["start"] for e in keep_segments)
    print(f"  Expected output: ~{keep_total:.0f}s ({keep_total/60:.1f}min)")
    print()

    # Determine output path
    ext = os.path.splitext(input_path)[1]
    if args.output:
        output_path = args.output
    else:
        base = os.path.splitext(input_path)[0]
        output_path = f"{base}_edited{ext}"

    # Create temp directory for segments
    tmp_dir = tempfile.mkdtemp(prefix="video_edit_")

    try:
        # Step 1: Extract KEEP segments
        print("=== Step 1: Extracting KEEP segments ===")
        t0 = time.time()
        part_files = []

        for i, seg in enumerate(keep_segments):
            part_file = os.path.join(tmp_dir, f"part_{i:03d}{ext}")
            part_files.append(part_file)
            dur = seg["end"] - seg["start"]
            print(f"  Part {i}: {fmt_time(seg['start'])} ~ {fmt_time(seg['end'])} ({dur:.1f}s)")

            cmd = [
                "ffmpeg", "-y",
                "-ss", str(seg["start"]),
                "-to", str(seg["end"]),
                "-i", input_path,
                "-c", "copy",
                "-avoid_negative_ts", "make_zero",
                part_file,
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"    ERROR: {result.stderr[-200:]}")
                sys.exit(1)

            size = os.path.getsize(part_file) / 1024 / 1024
            print(f"    OK ({size:.1f}MB)")

        print(f"Extraction done in {time.time()-t0:.1f}s")

        # Step 2: Concatenate
        print(f"\n=== Step 2: Concatenating {len(part_files)} parts ===")
        t1 = time.time()

        concat_file = os.path.join(tmp_dir, "concat_list.txt")
        with open(concat_file, "w") as f:
            for pf in part_files:
                f.write(f"file '{pf}'\n")

        concat_output = os.path.join(tmp_dir, f"concatenated{ext}")
        cmd = [
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0",
            "-i", concat_file,
            "-c", "copy",
            concat_output,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"  ERROR: {result.stderr[-300:]}")
            sys.exit(1)

        concat_dur = get_duration(concat_output)
        print(f"  Concatenated: {concat_dur:.1f}s ({concat_dur/60:.1f}min)")
        print(f"  Done in {time.time()-t1:.1f}s")

        # Step 3: Audio denoising (optional)
        if not args.skip_denoise and info["has_video"]:
            print(f"\n=== Step 3: Audio denoising (strength={args.denoise_strength}) ===")
            t2 = time.time()

            # Extract audio
            raw_audio = os.path.join(tmp_dir, "audio_raw.wav")
            cmd = [
                "ffmpeg", "-y",
                "-i", concat_output,
                "-vn", "-acodec", "pcm_s16le",
                "-ar", "44100", "-ac", "1",
                raw_audio,
            ]
            subprocess.run(cmd, capture_output=True, text=True)

            # Denoise
            try:
                import numpy as np
                import noisereduce as nr
                import soundfile as sf
                from scipy.signal import butter, sosfilt

                audio, sr = sf.read(raw_audio)
                print(f"  Audio loaded: {len(audio)/sr:.1f}s @ {sr}Hz")

                # Spectral gating
                noise_sample = audio[: int(sr * 2.0)]
                audio = nr.reduce_noise(
                    y=audio, sr=sr,
                    y_noise=noise_sample,
                    prop_decrease=args.denoise_strength,
                    stationary=True,
                )
                print("  Spectral gating applied")

                # Silence-gap attenuation
                frame_len = int(sr * 0.02)
                n_frames = len(audio) // frame_len
                rms = np.array([
                    np.sqrt(np.mean(audio[i * frame_len:(i + 1) * frame_len] ** 2))
                    for i in range(n_frames)
                ])
                threshold = np.percentile(rms[rms > 0], 25) if np.any(rms > 0) else 0
                attenuated = 0
                for i in range(n_frames):
                    if rms[i] < threshold:
                        audio[i * frame_len:(i + 1) * frame_len] *= 0.05
                        attenuated += 1
                print(f"  Attenuated {attenuated}/{n_frames} frames")

                # Bandpass filter
                hp = args.highpass
                lp = args.lowpass
                sos_hp = butter(4, hp, btype="high", fs=sr, output="sos")
                sos_lp = butter(4, lp, btype="low", fs=sr, output="sos")
                audio = sosfilt(sos_hp, audio)
                audio = sosfilt(sos_lp, audio)
                print(f"  Bandpass filter ({hp}Hz ~ {lp}Hz) applied")

                # Save denoised audio
                denoised_audio = os.path.join(tmp_dir, "audio_denoised.wav")
                sf.write(denoised_audio, audio, sr)

                # Remux: video from concat + denoised audio
                cmd = [
                    "ffmpeg", "-y",
                    "-i", concat_output,
                    "-i", denoised_audio,
                    "-c:v", "copy",
                    "-c:a", "aac", "-b:a", args.audio_bitrate,
                    "-map", "0:v:0", "-map", "1:a:0",
                    output_path,
                ]
                subprocess.run(cmd, capture_output=True, text=True)
                print(f"  Denoising done in {time.time()-t2:.1f}s")

            except ImportError:
                print("  Warning: noisereduce/soundfile not installed. Skipping denoise.")
                print("  Install: pip install noisereduce soundfile scipy")
                import shutil
                shutil.copy2(concat_output, output_path)

        elif not args.skip_denoise and not info["has_video"]:
            # Audio-only: denoise directly
            print(f"\n=== Step 3: Audio denoising ===")
            try:
                import numpy as np
                import noisereduce as nr
                import soundfile as sf
                from scipy.signal import butter, sosfilt

                audio, sr = sf.read(concat_output)
                noise_sample = audio[: int(sr * 2.0)]
                audio = nr.reduce_noise(
                    y=audio, sr=sr,
                    y_noise=noise_sample,
                    prop_decrease=args.denoise_strength,
                    stationary=True,
                )

                hp = args.highpass
                lp = args.lowpass
                sos_hp = butter(4, hp, btype="high", fs=sr, output="sos")
                sos_lp = butter(4, lp, btype="low", fs=sr, output="sos")
                audio = sosfilt(sos_hp, audio)
                audio = sosfilt(sos_lp, audio)

                sf.write(output_path, audio, sr)
                print("  Denoised audio saved")

            except ImportError:
                print("  Warning: noisereduce not installed. Skipping denoise.")
                import shutil
                shutil.copy2(concat_output, output_path)
        else:
            import shutil
            shutil.copy2(concat_output, output_path)

    finally:
        # Cleanup temp directory
        import shutil
        shutil.rmtree(tmp_dir, ignore_errors=True)

    # Report results
    out_info = get_media_info(output_path)
    print(f"\n{'=' * 60}")
    print("Result")
    print("=" * 60)
    print(f"  Input:    {info['duration']:.0f}s ({info['duration']/60:.1f}min) | {info['size_mb']:.0f}MB")
    print(f"  Output:   {out_info['duration']:.0f}s ({out_info['duration']/60:.1f}min) | {out_info['size_mb']:.0f}MB")
    removed = info["duration"] - out_info["duration"]
    print(f"  Removed:  {removed:.0f}s ({removed/60:.1f}min)")
    print(f"  Saved to: {output_path}")


# ──────────────────────────────────────────────
# TTS Prepare Command
# ──────────────────────────────────────────────

def cmd_tts_prepare(args):
    """Prepare TTS segments from whisper data and edit plan."""
    if not os.path.exists(args.whisper):
        print(f"Error: Whisper file not found: {args.whisper}", file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(args.plan):
        print(f"Error: Edit plan not found: {args.plan}", file=sys.stderr)
        sys.exit(1)

    with open(args.whisper) as f:
        whisper_data = json.load(f)
    with open(args.plan) as f:
        edit_plan = json.load(f)

    segments = whisper_data.get("segments", whisper_data)
    if isinstance(segments, dict):
        segments = segments.get("segments", [])

    print(f"Whisper segments: {len(segments)}")
    print(f"Edit plan entries: {len(edit_plan)}")

    # Map timestamps to edited timeline
    mapped = []
    for seg in segments:
        edited_start = original_to_edited(seg["start"], edit_plan)
        edited_end = original_to_edited(seg["end"], edit_plan)
        if edited_start is not None and edited_end is not None and edited_end > edited_start:
            mapped.append({
                "start": edited_start,
                "end": edited_end,
                "duration": round(edited_end - edited_start, 2),
                "text": seg["text"].strip(),
            })

    print(f"Mapped segments: {len(mapped)}")

    # Filter garbage
    hallucination_chars = ["⁇", "ème", "oken", "émissions", "ièrement", "בת", "стр"]
    filtered = []
    garbage_count = 0
    for seg in mapped:
        text = seg["text"]
        dur = seg["duration"]
        is_garbage = False
        if dur < 0.3:
            is_garbage = True
        elif len(text) < 2:
            is_garbage = True
        elif any(c in text for c in hallucination_chars):
            is_garbage = True

        if is_garbage:
            garbage_count += 1
        else:
            filtered.append(seg)

    if garbage_count > 0:
        print(f"Filtered garbage: {garbage_count}")

    # Apply text corrections
    if args.corrections and os.path.exists(args.corrections):
        with open(args.corrections) as f:
            corrections = json.load(f)
        fix_count = 0
        for seg in filtered:
            for wrong, correct in corrections.items():
                if wrong in seg["text"]:
                    seg["text"] = seg["text"].replace(wrong, correct)
                    fix_count += 1
        if fix_count > 0:
            print(f"Applied {fix_count} text corrections")

    total_chars = sum(len(s["text"]) for s in filtered)
    print(f"\nFinal: {len(filtered)} segments, {total_chars} characters")
    if filtered:
        print(f"Timeline: {filtered[0]['start']:.1f}s ~ {filtered[-1]['end']:.1f}s")

    # Save
    output_base = args.output or os.path.splitext(args.input)[0]
    segments_path = output_base + "_tts_segments.json"
    with open(segments_path, "w") as f:
        json.dump(filtered, f, ensure_ascii=False, indent=2)
    print(f"\nSegments saved: {segments_path}")
    print(f"\nReview the segments file, then run:")
    print(f"  python video_editor.py tts-generate \"{args.input}\" \"{segments_path}\" --voice-id YOUR_VOICE_ID")


# ──────────────────────────────────────────────
# TTS Generate Command
# ──────────────────────────────────────────────

def cmd_tts_generate(args):
    """Generate TTS audio and create video with new narration."""
    try:
        import requests
    except ImportError:
        print("Error: requests not installed. Run: pip install requests", file=sys.stderr)
        sys.exit(1)

    try:
        import numpy as np
    except ImportError:
        print("Error: numpy not installed. Run: pip install numpy", file=sys.stderr)
        sys.exit(1)

    # Check API key
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        print("Error: ELEVENLABS_API_KEY not set.", file=sys.stderr)
        print("  Load with: source ~/.claude/auth/elevenlabs.env", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(args.input):
        print(f"Error: Video not found: {args.input}", file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(args.segments):
        print(f"Error: Segments file not found: {args.segments}", file=sys.stderr)
        sys.exit(1)

    with open(args.segments) as f:
        segments = json.load(f)

    video_dur = get_duration(args.input)
    total_chars = sum(len(s["text"]) for s in segments)

    print(f"Input: {args.input}")
    print(f"  Video duration: {video_dur:.1f}s ({video_dur/60:.1f}min)")
    print(f"  Segments: {len(segments)}")
    print(f"  Total characters: {total_chars}")
    print(f"  Voice ID: {args.voice_id}")
    print(f"  Model: {args.tts_model}")
    print()

    # Create TTS output directory
    output_base = args.output or os.path.splitext(args.input)[0]
    tts_dir = output_base + "_tts"
    os.makedirs(tts_dir, exist_ok=True)

    # Generate TTS for each segment
    print(f"=== Generating TTS ({len(segments)} segments) ===")
    t0 = time.time()
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{args.voice_id}"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json",
    }

    success = 0
    errors = 0
    for i, seg in enumerate(segments):
        tts_file = os.path.join(tts_dir, f"tts_{i:03d}.mp3")

        # Skip if already generated (cache)
        if os.path.exists(tts_file) and os.path.getsize(tts_file) > 0 and not args.force:
            success += 1
            if i % 20 == 0:
                print(f"  {i:03d}/{len(segments)} (cached)")
            continue

        body = {
            "text": seg["text"],
            "model_id": args.tts_model,
            "voice_settings": {
                "stability": args.stability,
                "similarity_boost": args.similarity_boost,
                "style": args.style,
            }
        }

        retries = 3
        for attempt in range(retries):
            try:
                resp = requests.post(url, headers=headers, json=body, timeout=60)
                if resp.status_code == 200:
                    with open(tts_file, 'wb') as f:
                        f.write(resp.content)
                    success += 1
                    break
                elif resp.status_code == 429:
                    wait = 2 ** attempt * 5
                    print(f"  {i:03d} rate limited, waiting {wait}s...")
                    time.sleep(wait)
                else:
                    print(f"  {i:03d} ERROR: HTTP {resp.status_code} - {resp.text[:100]}")
                    if attempt == retries - 1:
                        errors += 1
            except Exception as e:
                print(f"  {i:03d} ERROR: {e}")
                if attempt == retries - 1:
                    errors += 1
                time.sleep(2)

        if i % 20 == 0:
            elapsed = time.time() - t0
            print(f"  {i:03d}/{len(segments)} ({elapsed:.0f}s)")

    elapsed = time.time() - t0
    print(f"\nTTS done in {elapsed:.0f}s | Success: {success} | Errors: {errors}")

    if errors > 0:
        print(f"Warning: {errors} segments failed. Re-run to retry (cached segments are reused).")

    # Assemble TTS audio on silent canvas
    print(f"\n=== Assembling TTS timeline ===")
    sample_rate = 44100
    total_samples = int(video_dur * sample_rate)
    canvas = np.zeros(total_samples, dtype=np.float32)

    placed = 0
    for i, seg in enumerate(segments):
        tts_file = os.path.join(tts_dir, f"tts_{i:03d}.mp3")
        if not os.path.exists(tts_file):
            continue

        # Decode MP3 to raw PCM
        cmd = [
            "ffmpeg", "-y", "-v", "quiet",
            "-i", tts_file,
            "-f", "f32le", "-acodec", "pcm_f32le",
            "-ar", str(sample_rate), "-ac", "1",
            "pipe:1"
        ]
        result = subprocess.run(cmd, capture_output=True)
        if result.returncode != 0:
            continue

        pcm = np.frombuffer(result.stdout, dtype=np.float32)
        start_sample = int(seg["start"] * sample_rate)

        # Limit to available space before next segment
        if i + 1 < len(segments):
            max_end = int(segments[i + 1]["start"] * sample_rate)
        else:
            max_end = total_samples
        available = max_end - start_sample
        if len(pcm) > available:
            pcm = pcm[:available]

        end_sample = min(start_sample + len(pcm), total_samples)
        actual_len = end_sample - start_sample
        canvas[start_sample:end_sample] = pcm[:actual_len]
        placed += 1

    print(f"  Placed {placed}/{len(segments)} segments")

    # Normalize
    peak = np.max(np.abs(canvas))
    if peak > 0:
        canvas = canvas / peak * 0.95

    # Save as WAV
    tmp_wav = tempfile.mktemp(suffix=".wav")
    canvas_int16 = (canvas * 32767).astype(np.int16)
    with wave.open(tmp_wav, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(canvas_int16.tobytes())

    # Optional denoise
    if not args.skip_denoise:
        print(f"\n=== Denoising audio (strength={args.denoise_strength}) ===")
        try:
            import noisereduce as nr
            import soundfile as sf
            from scipy.signal import butter, sosfilt

            audio, sr = sf.read(tmp_wav, dtype='float32')
            audio = nr.reduce_noise(y=audio, sr=sr, prop_decrease=args.denoise_strength, stationary=True)

            nyq = sr / 2
            sos_hp = butter(4, args.highpass / nyq, btype='highpass', output='sos')
            sos_lp = butter(4, args.lowpass / nyq, btype='lowpass', output='sos')
            audio = sosfilt(sos_hp, audio)
            audio = sosfilt(sos_lp, audio)

            peak = np.max(np.abs(audio))
            if peak > 0:
                audio = audio / peak * 0.95

            sf.write(tmp_wav, audio, sr, subtype='PCM_16')
            print("  Denoising applied")

        except ImportError:
            print("  Warning: noisereduce/soundfile not installed. Skipping denoise.")

    # Remux with video
    ext = os.path.splitext(args.input)[1]
    output_path = output_base + "_tts" + ext
    print(f"\n=== Remuxing video ===")
    cmd = [
        "ffmpeg", "-y", "-v", "quiet", "-stats",
        "-i", args.input,
        "-i", tmp_wav,
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", args.audio_bitrate,
        "-map", "0:v:0", "-map", "1:a:0",
        "-shortest",
        output_path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    os.remove(tmp_wav)

    if result.returncode != 0:
        print(f"Error: Remux failed: {result.stderr[-300:]}", file=sys.stderr)
        sys.exit(1)

    out_info = get_media_info(output_path)
    print(f"\n{'=' * 60}")
    print("Result")
    print("=" * 60)
    print(f"  Duration: {out_info['duration']:.0f}s ({out_info['duration']/60:.1f}min)")
    print(f"  Size: {out_info['size_mb']:.0f}MB")
    print(f"  TTS dir: {tts_dir}/")
    print(f"  Saved to: {output_path}")


# ──────────────────────────────────────────────
# Trim Silence Command
# ──────────────────────────────────────────────

def cmd_trim_silence(args):
    """Trim silence from video with dynamic or fixed caps."""
    if not os.path.exists(args.input):
        print(f"Error: Video not found: {args.input}", file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(args.segments):
        print(f"Error: Segments file not found: {args.segments}", file=sys.stderr)
        sys.exit(1)
    if not os.path.isdir(args.tts_dir):
        print(f"Error: TTS directory not found: {args.tts_dir}", file=sys.stderr)
        sys.exit(1)

    with open(args.segments) as f:
        segments = json.load(f)

    video_dur = get_duration(args.input)

    # Get actual TTS durations
    print("Getting TTS audio durations...")
    tts_durs = []
    for i in range(len(segments)):
        tts_file = os.path.join(args.tts_dir, f"tts_{i:03d}.mp3")
        if os.path.exists(tts_file):
            tts_durs.append(get_duration(tts_file))
        else:
            tts_durs.append(segments[i]["duration"])

    # Build KEEP segments
    mode = args.mode
    print(f"Mode: {mode}")
    if mode == "dynamic":
        print(f"  Caps: sentence={args.cap_sentence}s, comma={args.cap_comma}s, continue={args.cap_continue}s")
    else:
        print(f"  Fixed cap: {args.cap}s")

    keep_start = 0.0
    keep_segments = []
    total_removed = 0.0
    cuts = 0
    stats = {"punctuation": 0, "ending": 0, "comma": 0, "continuing": 0, "other": 0, "empty": 0}

    for i in range(len(segments)):
        tts_end = segments[i]["start"] + tts_durs[i]

        if i + 1 < len(segments):
            next_start = segments[i + 1]["start"]
            gap = next_start - tts_end

            if mode == "dynamic":
                cap, reason = classify_ending(
                    segments[i]["text"],
                    cap_sentence=args.cap_sentence,
                    cap_comma=args.cap_comma,
                    cap_continue=args.cap_continue,
                )
                stats[reason] += 1
            else:
                cap = args.cap
                reason = "fixed"

            if gap > cap:
                seg_end = min(tts_end + cap, next_start)
                keep_segments.append({"start": keep_start, "end": seg_end})
                removed = next_start - seg_end
                total_removed += removed
                cuts += 1
                keep_start = next_start
        else:
            keep_segments.append({"start": keep_start, "end": video_dur})

    final_dur = sum(s["end"] - s["start"] for s in keep_segments)
    print(f"\nSegments: {len(keep_segments)}, Cuts: {cuts}")
    print(f"Removed: {total_removed:.1f}s ({total_removed/60:.1f}min)")
    print(f"Final: {final_dur:.1f}s ({final_dur/60:.1f}min)")
    if mode == "dynamic":
        print(f"Classification: {stats}")

    # Extract and concatenate
    tmp_dir = tempfile.mkdtemp(prefix="trim_silence_")
    try:
        print(f"\nExtracting {len(keep_segments)} segments...")
        parts = []
        for i, seg in enumerate(keep_segments):
            part_file = os.path.join(tmp_dir, f"part_{i:03d}.mp4")
            parts.append(part_file)
            cmd = [
                "ffmpeg", "-y", "-v", "quiet",
                "-i", args.input,
                "-ss", str(seg["start"]),
                "-to", str(seg["end"]),
                "-c", "copy",
                "-avoid_negative_ts", "make_zero",
                part_file,
            ]
            subprocess.run(cmd, check=True)

        concat_file = os.path.join(tmp_dir, "concat.txt")
        with open(concat_file, "w") as f:
            for p in parts:
                f.write(f"file '{p}'\n")

        ext = os.path.splitext(args.input)[1]
        if args.output:
            output_path = args.output
        else:
            base = os.path.splitext(args.input)[0]
            if mode == "dynamic":
                output_path = f"{base}_trimmed{ext}"
            else:
                output_path = f"{base}_trimmed_{args.cap}s{ext}"

        print("Concatenating...")
        cmd = [
            "ffmpeg", "-y", "-v", "quiet",
            "-f", "concat", "-safe", "0",
            "-i", concat_file,
            "-c", "copy",
            output_path,
        ]
        subprocess.run(cmd, check=True)

    finally:
        import shutil
        shutil.rmtree(tmp_dir, ignore_errors=True)

    out_info = get_media_info(output_path)
    print(f"\n{'=' * 60}")
    print("Result")
    print("=" * 60)
    print(f"  Input:  {video_dur:.0f}s ({video_dur/60:.1f}min)")
    print(f"  Output: {out_info['duration']:.0f}s ({out_info['duration']/60:.1f}min)")
    print(f"  Size:   {out_info['size_mb']:.0f}MB")
    print(f"  Saved to: {output_path}")


# ──────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Video Auto-Editor: Whisper-based automated video editing with TTS support",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # analyze
    p_analyze = subparsers.add_parser("analyze", help="Transcribe and analyze for edit opportunities")
    p_analyze.add_argument("input", help="Input video or audio file")
    p_analyze.add_argument("-o", "--output", help="Output base path (default: input basename)")
    p_analyze.add_argument("-m", "--whisper-model", default="medium",
                           choices=["tiny", "base", "small", "medium", "large"],
                           help="Whisper model size (default: medium)")
    p_analyze.add_argument("-l", "--language", default="ko", help="Language code (default: ko)")
    p_analyze.add_argument("--min-gap", type=float, default=2.0,
                           help="Minimum silence gap to report in seconds (default: 2.0)")
    p_analyze.add_argument("--silence-threshold", type=float, default=10.0,
                           help="Silence gaps longer than this are auto-removed (default: 10.0)")

    # execute
    p_execute = subparsers.add_parser("execute", help="Execute edit plan")
    p_execute.add_argument("input", help="Input video or audio file")
    p_execute.add_argument("plan", help="Edit plan JSON file")
    p_execute.add_argument("-o", "--output", help="Output file path (default: input_edited.ext)")
    p_execute.add_argument("--skip-denoise", action="store_true", help="Skip audio denoising")
    p_execute.add_argument("-s", "--denoise-strength", type=float, default=0.4,
                           help="Spectral gating strength 0.0~1.0 (default: 0.4)")
    p_execute.add_argument("--highpass", type=int, default=80,
                           help="High-pass filter frequency in Hz (default: 80)")
    p_execute.add_argument("--lowpass", type=int, default=13000,
                           help="Low-pass filter frequency in Hz (default: 13000)")
    p_execute.add_argument("-b", "--audio-bitrate", default="192k",
                           help="Output audio bitrate (default: 192k)")

    # tts-prepare
    p_tts_prep = subparsers.add_parser("tts-prepare", help="Prepare TTS segments from whisper data")
    p_tts_prep.add_argument("input", help="Edited video file")
    p_tts_prep.add_argument("whisper", help="Whisper transcription JSON (*_whisper.json)")
    p_tts_prep.add_argument("plan", help="Edit plan JSON (*_edit_plan.json)")
    p_tts_prep.add_argument("-o", "--output", help="Output base path (default: input basename)")
    p_tts_prep.add_argument("--corrections", help="Text corrections JSON file (optional)")

    # tts-generate
    p_tts_gen = subparsers.add_parser("tts-generate", help="Generate TTS audio and create video")
    p_tts_gen.add_argument("input", help="Edited video file")
    p_tts_gen.add_argument("segments", help="TTS segments JSON (*_tts_segments.json)")
    p_tts_gen.add_argument("--voice-id", required=True, help="ElevenLabs voice ID")
    p_tts_gen.add_argument("--tts-model", default="eleven_multilingual_v2",
                           help="ElevenLabs model (default: eleven_multilingual_v2)")
    p_tts_gen.add_argument("--stability", type=float, default=0.5,
                           help="Voice stability 0.0~1.0 (default: 0.5)")
    p_tts_gen.add_argument("--similarity-boost", type=float, default=0.8,
                           help="Similarity boost 0.0~1.0 (default: 0.8)")
    p_tts_gen.add_argument("--style", type=float, default=0.3,
                           help="Style 0.0~1.0 (default: 0.3)")
    p_tts_gen.add_argument("--force", action="store_true",
                           help="Re-generate all TTS files (ignore cache)")
    p_tts_gen.add_argument("-o", "--output", help="Output base path (default: input basename)")
    p_tts_gen.add_argument("--skip-denoise", action="store_true", help="Skip audio denoising")
    p_tts_gen.add_argument("-s", "--denoise-strength", type=float, default=0.4,
                           help="Spectral gating strength (default: 0.4)")
    p_tts_gen.add_argument("--highpass", type=int, default=80, help="High-pass Hz (default: 80)")
    p_tts_gen.add_argument("--lowpass", type=int, default=13000, help="Low-pass Hz (default: 13000)")
    p_tts_gen.add_argument("-b", "--audio-bitrate", default="192k",
                           help="Output audio bitrate (default: 192k)")

    # trim-silence
    p_trim = subparsers.add_parser("trim-silence", help="Trim silence with dynamic or fixed caps")
    p_trim.add_argument("input", help="Video file to trim")
    p_trim.add_argument("segments", help="TTS segments JSON file")
    p_trim.add_argument("tts_dir", help="Directory containing TTS audio files")
    p_trim.add_argument("--mode", choices=["dynamic", "fixed"], default="dynamic",
                        help="Silence cap mode (default: dynamic)")
    p_trim.add_argument("--cap", type=float, default=0.5,
                        help="Fixed silence cap in seconds (default: 0.5)")
    p_trim.add_argument("--cap-sentence", type=float, default=0.5,
                        help="Dynamic: sentence-ending cap (default: 0.5)")
    p_trim.add_argument("--cap-comma", type=float, default=0.3,
                        help="Dynamic: comma-connector cap (default: 0.3)")
    p_trim.add_argument("--cap-continue", type=float, default=0.15,
                        help="Dynamic: continuing-phrase cap (default: 0.15)")
    p_trim.add_argument("-o", "--output", help="Output file path")

    args = parser.parse_args()

    if args.command == "analyze":
        cmd_analyze(args)
    elif args.command == "execute":
        cmd_execute(args)
    elif args.command == "tts-prepare":
        cmd_tts_prepare(args)
    elif args.command == "tts-generate":
        cmd_tts_generate(args)
    elif args.command == "trim-silence":
        cmd_trim_silence(args)


if __name__ == "__main__":
    main()
