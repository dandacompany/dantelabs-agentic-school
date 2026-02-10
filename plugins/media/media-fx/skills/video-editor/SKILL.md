---
name: video-editor
description: "Automated video editing with Whisper STT analysis and ElevenLabs TTS narration. This skill should be used when editing raw video recordings to remove silence gaps, retake/duplicate segments, and garbage audio, or when replacing narration with AI-generated TTS voice. Supports dynamic silence trimming based on Korean text analysis. Ideal for screen recordings, lecture captures, and narrated videos."
---

# Video Editor

Automated video editing pipeline that uses Whisper speech-to-text to detect and remove silence gaps, retakes/duplicates, and garbage segments. Optionally replaces narration with AI-generated TTS audio and trims silence dynamically.

## Prerequisites

- **ffmpeg**: `brew install ffmpeg`
- **Python packages**: `pip install -r ~/.claude/skills/video-editor/scripts/requirements.txt`
- **ElevenLabs API key** (for TTS): `source ~/.claude/auth/elevenlabs.env`

## Script Location

```
~/.claude/skills/video-editor/scripts/video_editor.py
```

## Workflows

### Workflow A: Basic Editing (analyze → execute)

Standard editing workflow to remove silence, retakes, and garbage from recordings.

```bash
SCRIPT="~/.claude/skills/video-editor/scripts/video_editor.py"

# Step 1: Analyze
python $SCRIPT analyze recording.mp4

# Step 2: Review *_edit_plan.json, then execute
python $SCRIPT execute recording.mp4 recording_edit_plan.json
```

### Workflow B: TTS Narration (analyze → execute → tts-prepare → tts-generate → trim-silence)

Replace original narration with AI-generated TTS voice, then trim excess silence.

```bash
SCRIPT="~/.claude/skills/video-editor/scripts/video_editor.py"
source ~/.claude/auth/elevenlabs.env

# Steps 1-2: Same as Workflow A
python $SCRIPT analyze recording.mp4
python $SCRIPT execute recording.mp4 recording_edit_plan.json

# Step 3: Prepare TTS segments (maps timestamps, filters garbage)
python $SCRIPT tts-prepare recording_edited.mp4 recording_whisper.json recording_edit_plan.json

# Step 4: Review *_tts_segments.json for text errors, then generate TTS
python $SCRIPT tts-generate recording_edited.mp4 recording_edited_tts_segments.json \
  --voice-id YOUR_VOICE_ID

# Step 5: Trim silence dynamically
python $SCRIPT trim-silence recording_edited_tts.mp4 \
  recording_edited_tts_segments.json recording_edited_tts/
```

## Commands

### analyze

Transcribe video with Whisper and generate an edit plan.

```bash
python scripts/video_editor.py analyze INPUT_VIDEO [OPTIONS]
```

**Output files** (saved alongside the input):
- `*_whisper.json` - Full Whisper transcription with timestamps
- `*_analysis.json` - Detailed analysis (gaps, duplicates, garbage)
- `*_edit_plan.json` - KEEP/REMOVE segment list

**Key parameters**:
- `-m, --whisper-model`: Model size (default: medium)
- `-l, --language`: Language code (default: ko)
- `--silence-threshold`: Auto-remove silences above this duration (default: 10.0)
- `--min-gap`: Minimum gap to report (default: 2.0)

### execute

Apply the edit plan to produce the edited video.

```bash
python scripts/video_editor.py execute INPUT_VIDEO EDIT_PLAN.json [OPTIONS]
```

**Key parameters**:
- `-o, --output`: Output file path (default: `*_edited.ext`)
- `--skip-denoise`: Skip audio denoising
- `-s, --denoise-strength`: Spectral gating strength 0.0-1.0 (default: 0.4)
- `--highpass/--lowpass`: Bandpass filter range in Hz (default: 80-13000)

### tts-prepare

Map Whisper segments to edited video timestamps and prepare for TTS generation.

```bash
python scripts/video_editor.py tts-prepare EDITED_VIDEO WHISPER.json EDIT_PLAN.json [OPTIONS]
```

This command:
1. Loads Whisper transcription and edit plan
2. Maps original timestamps to the edited video timeline
3. Filters garbage segments (short, empty, hallucination)
4. Optionally applies text corrections from a JSON file
5. Saves `*_tts_segments.json` for review

**Key parameters**:
- `--corrections`: JSON file with text corrections (`{"wrong": "correct", ...}`)

**Output**: `*_tts_segments.json` - Array of segments with edited timestamps and cleaned text.

Review this file before proceeding to fix Whisper transcription errors.

### tts-generate

Generate TTS audio using ElevenLabs API and create video with new narration.

```bash
python scripts/video_editor.py tts-generate EDITED_VIDEO SEGMENTS.json --voice-id VOICE_ID [OPTIONS]
```

This command:
1. Generates TTS audio for each segment via ElevenLabs API
2. Assembles TTS clips on a silent audio canvas matching video duration
3. Optionally denoises the assembled audio
4. Remuxes with the video (stream copy, no re-encoding)

**Key parameters**:
- `--voice-id` (required): ElevenLabs voice ID
- `--tts-model`: ElevenLabs model (default: eleven_multilingual_v2)
- `--stability`: Voice stability 0.0-1.0 (default: 0.5)
- `--similarity-boost`: Similarity boost 0.0-1.0 (default: 0.8)
- `--style`: Style exaggeration 0.0-1.0 (default: 0.3)
- `--force`: Re-generate all TTS files (ignores cache)
- `--skip-denoise`: Skip audio denoising
- `-s, --denoise-strength`: Denoise strength (default: 0.4)

**Output files**:
- `*_tts/tts_NNN.mp3` - Individual TTS audio files (cached for re-runs)
- `*_tts.mp4` - Video with TTS narration

**Caching**: Successfully generated TTS files are reused on re-run. Use `--force` to regenerate.

**Authentication**: Requires `ELEVENLABS_API_KEY` environment variable. Load with `source ~/.claude/auth/elevenlabs.env`.

### trim-silence

Trim silence from video with dynamic or fixed caps. Designed for TTS videos where silence gaps between segments need to be reduced.

```bash
python scripts/video_editor.py trim-silence TTS_VIDEO SEGMENTS.json TTS_DIR/ [OPTIONS]
```

**Dynamic mode** (default): Analyzes Korean text endings to set appropriate silence caps per segment:
- **Sentence endings** (니다, 예요, 겠죠, `.`, `!`, `?`): 0.5s cap
- **Comma connectors** (고,, 서,, 지만,): 0.3s cap
- **Continuing phrases** (조사, 연결어미, 기타): 0.15s cap

**Fixed mode**: Applies a uniform silence cap to all gaps.

**Key parameters**:
- `--mode`: `dynamic` (default) or `fixed`
- `--cap`: Fixed silence cap in seconds (default: 0.5)
- `--cap-sentence`: Dynamic sentence-ending cap (default: 0.5)
- `--cap-comma`: Dynamic comma-connector cap (default: 0.3)
- `--cap-continue`: Dynamic continuing-phrase cap (default: 0.15)

**Examples**:
```bash
# Dynamic mode (recommended for Korean)
python $SCRIPT trim-silence video_tts.mp4 segments.json tts_dir/

# Fixed mode with 0.5s cap
python $SCRIPT trim-silence video_tts.mp4 segments.json tts_dir/ --mode fixed --cap 0.5

# Tighter dynamic caps for fast-paced content
python $SCRIPT trim-silence video_tts.mp4 segments.json tts_dir/ \
  --cap-sentence 0.3 --cap-comma 0.2 --cap-continue 0.1
```

## Text Corrections

Whisper may transcribe Korean words incorrectly. Create a corrections JSON file to fix recurring errors:

```json
{
  "프론프트": "프롬프트",
  "핵심 기동": "핵심 기둥",
  "파이성": "파이썬"
}
```

Apply during `tts-prepare`:
```bash
python $SCRIPT tts-prepare video.mp4 whisper.json plan.json --corrections fixes.json
```

## Edit Plan Format

```json
[
  {"action": "KEEP", "start": 0.0, "end": 56.48, "note": ""},
  {"action": "REMOVE", "start": 56.48, "end": 77.52, "note": "무음 21.0초"},
  {"action": "KEEP", "start": 77.52, "end": 189.46, "note": ""}
]
```

## Detection Logic

### Silence Gaps

Gaps between Whisper segments exceeding `--silence-threshold` (default 10s) are automatically marked as REMOVE.

### Retake/Duplicate Detection

Segments sharing the same opening text (first 15 characters) are identified as retakes. The plan keeps only the last occurrence.

### Garbage Segments

Detected by: duration under 0.3s, empty text, or Whisper hallucination patterns.

### Dynamic Silence Classification (Korean)

For `trim-silence` dynamic mode, segment endings are classified into three tiers using Korean linguistic patterns:
- **Sentence endings**: 종결어미 (합니다, 해요, 겠죠, etc.) and punctuation
- **Comma connectors**: 접속 연결 (고,, 서,, 지만,, etc.)
- **Continuing phrases**: 조사/연결어미 (을, 에서, 고, 면, etc.) and unclassified endings

## Technical Notes

- **Stream copy**: Video segments are extracted with `-c copy`. No re-encoding preserves original quality.
- **TTS caching**: Generated MP3 files persist in `*_tts/` directory. Re-running `tts-generate` skips existing files.
- **Silent canvas**: TTS assembly creates a full-duration silent array, places each TTS clip at its timestamp, then normalizes.
- **Denoise pipeline**: Spectral gating (noisereduce) → bandpass filter (80Hz-13kHz) → normalization.

## ElevenLabs API

**Quota costs**: ~1 character = 1 character from quota. Estimate: 30 chars/segment x 100 segments = 3,000 chars.

**Models**:
- `eleven_multilingual_v2` - High quality, Korean support (default)
- `eleven_turbo_v2_5` - Faster, slightly lower quality

**Rate limiting**: Automatic retry with exponential backoff (3 retries, 5s/10s/20s waits).

## Resources

- **scripts/video_editor.py** - Main CLI with all subcommands
- **scripts/requirements.txt** - Python package dependencies
