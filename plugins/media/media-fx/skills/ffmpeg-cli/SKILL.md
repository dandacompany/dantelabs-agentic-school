---
name: ffmpeg-cli
description: This skill should be used when processing video, audio, or image files with FFmpeg. Use this skill for tasks like adding text/subtitles, extracting/mixing audio, converting formats, merging/trimming videos, applying transitions/fades, overlaying images/videos, and querying media metadata. Ideal for multimedia processing, video editing, format conversion, and media file manipulation.
---

# FFmpeg CLI

## Overview

Execute FFmpeg command-line operations to process video, audio, and image files. This skill provides comprehensive FFmpeg workflows for 13 common multimedia processing tasks, from basic format conversion to advanced video editing with transitions and overlays.

## Prerequisites

Verify FFmpeg installation before proceeding:

```bash
ffmpeg -version
```

**Minimum version:** FFmpeg 4.3+ (for xfade transitions)
**Common installation:**
- macOS: `brew install ffmpeg`
- Linux: `apt-get install ffmpeg` or `yum install ffmpeg`
- Windows: Download from ffmpeg.org

## Official CLI Syntax

### Command Structure

```
ffmpeg [global_options] {[input_file_options] -i input_url} ... {[output_file_options] output_url} ...
```

> **Critical Rule**: Options are positional. Input options apply ONLY to the next `-i`. Output options apply ONLY to the next output file. Misordering options causes silent misbehavior.

```bash
# CORRECT: -ss seeks input (fast), -t limits output duration
ffmpeg -y -ss 5 -i input.mp4 -t 10 -c:v libx264 output.mp4
#      ^   ^                   ^                    ^
#      |   input option        output options       output file
#      global option

# DIFFERENT BEHAVIOR: -ss after -i seeks output (slow but accurate)
ffmpeg -y -i input.mp4 -ss 5 -t 10 -c:v libx264 output.mp4
```

### Stream Specifiers

Target specific streams with `-option:stream_specifier`:

| Pattern | Meaning | Example |
|---------|---------|---------|
| `v` | All video streams | `-c:v libx264` |
| `a` | All audio streams | `-c:a aac` |
| `s` | All subtitle streams | `-c:s mov_text` |
| `v:0` | First video stream | `-b:v:0 2M` |
| `a:1` | Second audio stream | `-c:a:1 copy` |

### Stream Mapping

```bash
# Without -map: auto-selects best video + best audio + first subtitle
ffmpeg -i input.mp4 output.mp4

# With -map: auto-selection DISABLED — must map ALL desired streams
ffmpeg -i input.mp4 -map 0:v -map 0:a output.mp4

# Multiple inputs: video from first, audio from second
ffmpeg -i video.mp4 -i audio.mp3 -map 0:v -map 1:a output.mp4
```

> **Gotcha**: Using `-map` once disables auto-selection. Forgetting to map audio = silent output.

### Seeking Behavior

| Position | Speed | Accuracy | Use Case |
|----------|-------|----------|----------|
| `-ss` before `-i` | Fast (keyframe seek) | Approximate | Stream copy, rough cuts |
| `-ss` after `-i` | Slow (decode & discard) | Frame-exact | Precise editing |
| Both combined | Fast + Accurate | Best of both | Recommended for re-encode |

```bash
# Fast seeking (good with -c copy)
ffmpeg -ss 30 -i input.mp4 -t 10 -c copy output.mp4

# Accurate seeking (re-encode required)
ffmpeg -i input.mp4 -ss 30 -t 10 -c:v libx264 -c:a aac output.mp4

# Combined: fast jump + fine-tune
ffmpeg -ss 29 -i input.mp4 -ss 1 -t 10 -c:v libx264 -c:a aac output.mp4
```

### Stream Copy vs Re-encoding

| | `-c copy` | Re-encode (`-c:v libx264`) |
|---|-----------|---------------------------|
| Speed | Very fast | Slow |
| Quality | Lossless (original) | Depends on settings |
| Filters | Cannot use | Required for filters |
| Cut accuracy | Keyframe only | Frame-exact |

```bash
# Stream copy (fast, no quality loss, no filters)
ffmpeg -i input.mp4 -c copy output.mp4

# Re-encode video only (allows video filters, copies audio)
ffmpeg -i input.mp4 -vf "scale=1280:720" -c:v libx264 -c:a copy output.mp4
```

### Common Patterns

**Copy without re-encoding (fast):**
```bash
ffmpeg -i input.mp4 -c copy output.mp4
```

**Re-encode with quality control:**
```bash
ffmpeg -i input.mp4 -c:v libx264 -crf 23 -c:a aac output.mp4
```

**Apply video filter:**
```bash
ffmpeg -i input.mp4 -vf "filter_name=param=value" -c:a copy output.mp4
```

**Complex filter graph:**
```bash
ffmpeg -i input1.mp4 -i input2.mp4 \
  -filter_complex "[0:v][1:v]filter_name[out]" \
  -map "[out]" -map 0:a output.mp4
```

## Core Operations

### 1. Add Text to Video

Add text overlays with full control over font, size, color, position, and timing.

**Basic text overlay:**
```bash
ffmpeg -i input.mp4 \
  -vf "drawtext=fontfile=/path/to/font.ttf:text='Hello World':fontsize=48:fontcolor=white:x=(w-text_w)/2:y=h-th-20" \
  -c:a copy output.mp4
```

**Parameters:**
- `fontfile` - Path to TrueType font file (required)
- `text` - Text content (escape single quotes: `don''t`)
- `fontsize` - Font size in pixels (default: 16)
- `fontcolor` - Color name or hex value
- `x`, `y` - Position (numbers or expressions)
- `enable` - Time control: `'between(t,5,10)'`

**Position expressions:**
- `(w-text_w)/2` - center horizontally
- `(h-text_h)/2` - center vertically
- `10` - 10px from left/top edge
- `w-text_w-10` - 10px from right edge
- `h-th-20` - 20px from bottom edge

**Text with background box:**
```bash
ffmpeg -i input.mp4 \
  -vf "drawtext=fontfile=/path/to/font.ttf:text='Subtitle':fontsize=48:fontcolor=white:x=(w-text_w)/2:y=h-th-20:box=1:boxcolor=black@0.5:boxborderw=5" \
  -c:a copy output.mp4
```

**Timed text (show from 5 to 10 seconds):**
```bash
ffmpeg -i input.mp4 \
  -vf "drawtext=fontfile=/path/to/font.ttf:text='Limited':fontsize=48:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2:enable='between(t,5,10)'" \
  -c:a copy output.mp4
```

### 2. Add Subtitles from SRT File

Burn subtitles from SRT file into video.

**Method 1: Using subtitles filter (recommended):**
```bash
ffmpeg -i input.mp4 -vf "subtitles=subtitle.srt" -c:a copy output.mp4
```

**Method 2: Custom styling with drawtext (programmatic):**

Parse SRT file and generate drawtext filter chain for each subtitle entry. Each entry becomes:
```bash
drawtext=fontfile=/path/to/font.ttf:text='subtitle text':fontsize=48:fontcolor=white:x=(w-text_w)/2:y=h-th-50:box=1:boxcolor=black@0.5:boxborderw=5:enable='between(t,START_TIME,END_TIME)'
```

Combine all entries with commas:
```bash
ffmpeg -i input.mp4 -vf "drawtext=...,drawtext=...,drawtext=..." -c:a copy output.mp4
```

**Custom subtitle styling:**
```bash
ffmpeg -i input.mp4 \
  -vf "subtitles=subtitle.srt:force_style='FontName=Arial,FontSize=24,PrimaryColour=&H00FFFFFF'" \
  -c:a copy output.mp4
```

### 3. Extract Audio from Video

Extract audio track in various formats.

**Extract as MP3:**
```bash
ffmpeg -i input.mp4 -vn -c:a libmp3lame -b:a 192k -map 0:a:0 output.mp3
```

**Extract as AAC:**
```bash
ffmpeg -i input.mp4 -vn -c:a aac -b:a 192k -map 0:a:0 output.aac
```

**Extract as WAV (lossless):**
```bash
ffmpeg -i input.mp4 -vn -c:a pcm_s16le -map 0:a:0 output.wav
```

**Copy audio without re-encoding:**
```bash
ffmpeg -i input.mp4 -vn -c:a copy -map 0:a:0 output.m4a
```

**Parameters:**
- `-vn` - Remove video stream
- `-c:a` - Audio codec (libmp3lame, aac, copy)
- `-b:a` - Audio bitrate (128k, 192k, 320k)
- `-map 0:a:0` - Select first audio stream

### 4. Convert Image to Video

Convert static image to video with specified duration.

**Basic conversion:**
```bash
ffmpeg -loop 1 -i image.png \
  -c:v libx264 -t 10 -pix_fmt yuv420p \
  output.mp4
```

**With silent audio for compatibility:**
```bash
ffmpeg -loop 1 -i image.png \
  -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=44100 \
  -c:v libx264 -c:a aac -t 10 -pix_fmt yuv420p -shortest \
  output.mp4
```

**Custom dimensions:**
```bash
ffmpeg -loop 1 -i image.png \
  -f lavfi -i anullsrc \
  -vf "scale=1920:1080" \
  -c:v libx264 -c:a aac -t 10 -pix_fmt yuv420p -shortest \
  output.mp4
```

**Parameters:**
- `-loop 1` - Loop image input
- `-t` - Duration in seconds
- `-pix_fmt yuv420p` - Ensure compatibility
- `anullsrc` - Generate silent audio
- `-shortest` - Match shortest input duration

### 5. Merge/Concatenate Videos

Combine multiple videos into one.

**Method 1: Concat demuxer (same codec/format):**
```bash
# Create file list
echo "file 'video1.mp4'" > list.txt
echo "file 'video2.mp4'" >> list.txt

# Concatenate
ffmpeg -f concat -safe 0 -i list.txt -c copy output.mp4
```

**Method 2: Concat filter (different formats):**
```bash
ffmpeg -i video1.mp4 -i video2.mp4 -i video3.mp4 \
  -filter_complex "[0:v][0:a][1:v][1:a][2:v][2:a]concat=n=3:v=1:a=1[outv][outa]" \
  -map "[outv]" -map "[outa]" output.mp4
```

**Normalize before merging (different resolutions/framerates):**

For each input video, apply normalization:
```bash
scale=1920:1080:force_original_aspect_ratio=decrease,
pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=black,
setsar=1,
fps=30,
setpts=PTS-STARTPTS
```

For audio:
```bash
aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=stereo,
asetpts=PTS-STARTPTS
```

Then concatenate normalized streams using concat protocol or concat filter.

**Handle videos without audio:**

Check if video has audio using ffprobe. If missing, add silent audio:
```bash
ffmpeg -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=44100:duration=VIDEO_DURATION
```

Mix with video stream before normalization.

### 6. Mix Audio with Video

Combine video with background music or replace audio.

**Basic audio mixing:**
```bash
ffmpeg -i video.mp4 -i music.mp3 \
  -filter_complex "[0:a]volume=1.0[a0];[1:a]volume=0.5[a1];[a0][a1]amix=inputs=2:duration=first[a]" \
  -map 0:v -map "[a]" -c:v copy output.mp4
```

**Replace video audio:**
```bash
ffmpeg -i video.mp4 -i new_audio.mp3 \
  -map 0:v -map 1:a -c:v copy -c:a aac -shortest output.mp4
```

**Advanced mixing with fade effects:**
```bash
ffmpeg -i video.mp4 -i music.mp3 \
  -filter_complex "
    [1:a]afade=t=in:st=0:d=2,afade=t=out:st=28:d=2,volume=0.5[a1];
    [0:a]volume=1.0[a0];
    [a0][a1]amix=inputs=2:duration=first[a]
  " \
  -map 0:v -map "[a]" -c:v copy output.mp4
```

**Partial mixing with time control:**

Process audio with:
```bash
[1:a]atrim=duration=DURATION,asetpts=PTS-STARTPTS,volume=VOLUME,adelay=START_TIME*1000|START_TIME*1000[overlay]
```

Mix with main audio:
```bash
[0:a]volume=VIDEO_VOLUME[main];
[main][overlay]amix=inputs=2:duration=first[out]
```

**Loop short audio:**
```bash
[1:a]aloop=loop=-1:size=2e9,atrim=duration=VIDEO_DURATION[looped]
```

**Parameters:**
- `volume` - Volume multiplier (0.0-2.0)
- `amix:duration` - longest/shortest/first
- `adelay` - Delay in milliseconds
- `afade` - Fade in/out
- `atrim` - Trim audio duration
- `aloop` - Loop audio (-1 for infinite)

### 7. Apply Video Transitions

Apply transition effects between multiple videos (requires FFmpeg 4.3+).

**Fade transition:**
```bash
ffmpeg -i video1.mp4 -i video2.mp4 \
  -filter_complex "
    [0:v][1:v]xfade=transition=fade:duration=1:offset=5[v];
    [0:a][1:a]acrossfade=d=1[a]
  " \
  -map "[v]" -map "[a]" output.mp4
```

**Multiple videos with transitions:**
```bash
ffmpeg -i v1.mp4 -i v2.mp4 -i v3.mp4 \
  -filter_complex "
    [0:v][1:v]xfade=transition=fade:duration=1:offset=5[v01];
    [v01][2:v]xfade=transition=wipeleft:duration=1:offset=10[v];
    [0:a][1:a]acrossfade=d=1[a01];
    [a01][2:a]acrossfade=d=1[a]
  " \
  -map "[v]" -map "[a]" output.mp4
```

**Available transitions:**
- `fade`, `fadeblack`, `fadewhite`
- `wipeleft`, `wiperight`, `wipeup`, `wipedown`
- `slideleft`, `slideright`, `slideup`, `slidedown`
- `circlecrop`, `rectcrop`, `distance`
- `dissolve`, `pixelize`, `radial`

**Normalize videos before transition:**

When videos have different resolutions or framerates:
```bash
[0:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black,settb=AVTB[v0];
[1:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black,settb=AVTB[v1];
[v0][v1]xfade=transition=fade:duration=1:offset=5[v]
```

**Fallback for FFmpeg < 4.3:**

Use fade + concat instead:
```bash
# First video: fade out at end
[0:v]fade=t=out:st=5:d=1[v0];
# Second video: fade in at start
[1:v]fade=t=in:st=0:d=1[v1];
# Concatenate
[v0][0:a][v1][1:a]concat=n=2:v=1:a=1[outv][outa]
```

**Parameters:**
- `transition` - Transition type
- `duration` - Transition duration in seconds
- `offset` - When transition starts in first video
- `acrossfade:d` - Audio crossfade duration

### 8. Overlay Video/Image

Place one video or image on top of another.

**Basic overlay (logo/watermark):**
```bash
ffmpeg -i video.mp4 -i logo.png \
  -filter_complex "[1:v]scale=150:-1[logo];[0:v][logo]overlay=10:10" \
  -c:a copy output.mp4
```

**Positioned overlays:**
```bash
# Bottom-right corner
overlay=main_w-overlay_w-10:main_h-overlay_h-10

# Center
overlay=(main_w-overlay_w)/2:(main_h-overlay_h)/2

# Top-right
overlay=main_w-overlay_w-10:10
```

**Overlay with opacity:**
```bash
ffmpeg -i video.mp4 -i logo.png \
  -filter_complex "[1:v]scale=150:-1,colorchannelmixer=aa=0.5[logo];[0:v][logo]overlay=10:10" \
  -c:a copy output.mp4
```

**Timed overlay (show from 5 to 15 seconds):**
```bash
ffmpeg -i video.mp4 -i logo.png \
  -filter_complex "[1:v]scale=150:-1[logo];[0:v][logo]overlay=10:10:enable='between(t,5,15)'" \
  -c:a copy output.mp4
```

**Picture-in-picture:**
```bash
ffmpeg -i main.mp4 -i small.mp4 \
  -filter_complex "
    [1:v]scale=320:-1[pip];
    [0:v][pip]overlay=main_w-overlay_w-10:10[v]
  " \
  -map "[v]" -map 0:a -c:a copy output.mp4
```

**Audio handling options:**

```bash
# Use main video audio only
-map 0:a

# Use overlay video audio only
-map 1:a

# Mix both audio tracks
-filter_complex "...[v];[0:a]volume=1.0[a0];[1:a]volume=0.5[a1];[a0][a1]amix=inputs=2:duration=longest[a]"
-map "[v]" -map "[a]"
```

**Parameters:**
- `scale` - Resize overlay (width:height, -1 for auto)
- `colorchannelmixer=aa` - Opacity (0.0-1.0)
- `overlay=x:y` - Position
- `enable` - Time control
- `eof_action=pass` - Continue main after overlay ends

### 9. Separate Video and Audio

Split video into separate video (muted) and audio files.

**Create muted video:**
```bash
ffmpeg -i input.mp4 -an -c:v copy video_only.mp4
```

**Extract audio:**
```bash
ffmpeg -i input.mp4 -vn -c:a libmp3lame -b:a 192k -map 0:a:0 audio.mp3
```

**Both in one operation:**
```bash
# Muted video
ffmpeg -i input.mp4 -an -c:v copy video_only.mp4

# Audio file
ffmpeg -i input.mp4 -vn -c:a libmp3lame -b:a 192k -map 0:a:0 audio.mp3
```

**Parameters:**
- `-an` - Remove audio stream
- `-vn` - Remove video stream
- `-c:v copy` - Copy video without re-encoding
- `-c:a` - Audio codec (libmp3lame, aac, copy)

### 10. Apply Fade In/Out

Add fade in or fade out effects to video and/or audio.

**Video fade in/out:**
```bash
ffmpeg -i input.mp4 \
  -vf "fade=type=in:st=0:d=2,fade=type=out:st=28:d=2" \
  -c:a copy output.mp4
```

**Audio fade in/out:**
```bash
ffmpeg -i input.mp4 \
  -af "afade=type=in:st=0:d=2,afade=type=out:st=28:d=2" \
  -c:v copy output.mp4
```

**Both video and audio fade:**
```bash
ffmpeg -i input.mp4 \
  -vf "fade=type=in:st=0:d=2,fade=type=out:st=28:d=2" \
  -af "afade=type=in:st=0:d=2,afade=type=out:st=28:d=2" \
  output.mp4
```

**Fade to/from white:**
```bash
ffmpeg -i input.mp4 \
  -vf "fade=type=in:st=0:d=2:color=white" \
  -c:a copy output.mp4
```

**Parameters:**
- `type` - `in` or `out`
- `st` - Start time in seconds
- `d` - Duration in seconds
- `color` - Fade color (default: black)

### 11. Add Image Stamp/Watermark

Add logo, watermark, or stamp image to video.

**Basic stamp:**
```bash
ffmpeg -i video.mp4 -i stamp.png \
  -filter_complex "[1:v]scale=150:-1[stamp];[0:v][stamp]overlay=10:10" \
  -c:a copy output.mp4
```

**Rotated stamp:**
```bash
ffmpeg -i video.mp4 -i stamp.png \
  -filter_complex "
    [1:v]scale=150:-1,rotate=PI/4:fillcolor=none[stamp];
    [0:v][stamp]overlay=10:10
  " \
  -c:a copy output.mp4
```

**Stamp with opacity:**
```bash
ffmpeg -i video.mp4 -i stamp.png \
  -filter_complex "
    [1:v]scale=150:-1,colorchannelmixer=aa=0.5[stamp];
    [0:v][stamp]overlay=10:10
  " \
  -c:a copy output.mp4
```

**Timed stamp (show from 5 to 15 seconds):**
```bash
ffmpeg -i video.mp4 -i stamp.png \
  -filter_complex "
    [1:v]scale=150:-1[stamp];
    [0:v][stamp]overlay=10:10:enable='between(t,5,15)'
  " \
  -c:a copy output.mp4
```

**Parameters:**
- `scale` - Resize stamp (width:height, -1 for auto)
- `rotate` - Rotation angle in radians (PI/2 = 90°, PI/4 = 45°)
- `colorchannelmixer=aa` - Opacity (0.0-1.0)
- `overlay=x:y` - Position
- `enable` - Time control

### 12. Trim/Cut Video

Extract portion of video between specified times.

**Fast cut (keyframe-accurate, input seeking):**
```bash
ffmpeg -ss 5 -i input.mp4 -t 10 -c copy output.mp4
```

**Accurate cut (frame-exact, output seeking + re-encode):**
```bash
ffmpeg -i input.mp4 -ss 5 -t 10 -c:v libx264 -c:a aac output.mp4
```

**Combined seeking (fast + accurate):**
```bash
ffmpeg -ss 4 -i input.mp4 -ss 1 -t 10 -c:v libx264 -c:a aac output.mp4
```

**Extract from 5 to 15 seconds:**
```bash
ffmpeg -ss 5 -i input.mp4 -to 10 -c copy output.mp4
```

**Time duration formats:**
```bash
-ss 01:23:45.678   # HH:MM:SS.mmm
-ss 5:30            # MM:SS (5 min 30 sec)
-ss 90              # seconds (numeric)
-ss 5500ms          # milliseconds with suffix
```

**Parameters:**
- `-ss` before `-i` - Input seeking (fast, keyframe-accurate)
- `-ss` after `-i` - Output seeking (slow, frame-accurate)
- `-to` - End time (absolute when `-ss` is after `-i`, relative when before)
- `-t` - Duration (always relative from seek point)
- `-c copy` - Stream copy (fast, keyframe-accurate only)
- `-c:v libx264` - Re-encode for frame-accurate cutting

> **Gotcha**: `-to` behaves differently depending on `-ss` position. With input seeking (`-ss` before `-i`), `-to` becomes relative to the new start.

### 13. Probe Media Information

Query metadata and technical details of media files.

**Complete metadata (JSON):**
```bash
ffprobe -v quiet -print_format json -show_format -show_streams input.mp4
```

**Quick info:**
```bash
ffmpeg -i input.mp4 2>&1 | grep -E 'Duration|Stream'
```

**Video resolution:**
```bash
ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 input.mp4
```

**Video duration:**
```bash
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 input.mp4
```

**Check if video has audio:**
```bash
ffprobe -i input.mp4 -show_streams -select_streams a -loglevel error
```

**Framerate:**
```bash
ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate -of default=noprint_wrappers=1:nokey=1 input.mp4
```

**Codec information:**
```bash
ffprobe -v error -select_streams v:0 -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 input.mp4
```

## Advanced Patterns

### Complex Filter Graphs

**Multiple outputs from single input:**
```bash
ffmpeg -i input.mp4 \
  -filter_complex "
    [0:v]split=2[v1][v2];
    [v1]scale=1920:1080[out1];
    [v2]scale=1280:720[out2]
  " \
  -map "[out1]" -c:v libx264 output_1080p.mp4 \
  -map "[out2]" -c:v libx264 output_720p.mp4
```

**Side-by-side comparison:**
```bash
ffmpeg -i left.mp4 -i right.mp4 \
  -filter_complex "
    [0:v]scale=640:480[left];
    [1:v]scale=640:480[right];
    [left][right]hstack[v]
  " \
  -map "[v]" output.mp4
```

### Quality Control

**CRF (Constant Rate Factor) — recommended for local files:**

| CRF | Quality | Use Case |
|-----|---------|----------|
| 0 | Lossless | Archival |
| 18 | Visually lossless | Professional editing |
| 23 | Good (default) | General purpose |
| 28 | Acceptable | Web distribution |
| 51 | Worst | (not recommended) |

```bash
ffmpeg -i input.mp4 -c:v libx264 -crf 23 -preset medium -c:a aac output.mp4
```

**Constrained bitrate — recommended for streaming:**
```bash
# Average bitrate with buffer control
ffmpeg -i input.mp4 -c:v libx264 -b:v 2M -maxrate 2.5M -bufsize 5M -c:a aac output.mp4
```

> **Gotcha**: `-b:v 2M` = 2 Megabits/s (not bytes). FFmpeg uses bits/s. Use `K`, `M`, `G` suffixes.

**Two-pass encoding (best quality at target bitrate):**
```bash
# Pass 1 (analysis only — output to /dev/null)
ffmpeg -i input.mp4 -c:v libx264 -b:v 2M -pass 1 -f null /dev/null

# Pass 2 (actual encoding using analysis)
ffmpeg -i input.mp4 -c:v libx264 -b:v 2M -pass 2 -c:a aac output.mp4
```

**Encoding presets** (speed → quality tradeoff):

`ultrafast` > `superfast` > `veryfast` > `faster` > `fast` > `medium` > `slow` > `slower` > `veryslow`

**Tunes** (content-type optimization):
```bash
# Animation
ffmpeg -i input.mp4 -c:v libx264 -crf 20 -tune animation output.mp4

# Screen recording
ffmpeg -i input.mp4 -c:v libx264 -crf 18 -tune stillimage output.mp4

# Streaming (low latency)
ffmpeg -i input.mp4 -c:v libx264 -preset fast -tune zerolatency output.mp4
```

**Audio codec options:**
```bash
# AAC at 192kbps
-c:a aac -b:a 192k

# MP3 VBR high quality (~190kbps average)
-c:a libmp3lame -q:a 2

# MP3 CBR 192kbps
-c:a libmp3lame -b:a 192k
```

> **Gotcha**: VBR (`-q:a`) and CBR (`-b:a`) are mutually exclusive for MP3. Don't use both.

### Hardware Acceleration

**macOS (VideoToolbox):**
```bash
ffmpeg -hwaccel videotoolbox -i input.mp4 -c:v h264_videotoolbox output.mp4
```

**Linux/NVIDIA (NVENC):**
```bash
ffmpeg -hwaccel cuda -i input.mp4 -c:v h264_nvenc output.mp4
```

**Auto-detect:**
```bash
ffmpeg -hwaccel auto -i input.mp4 -c:v libx264 output.mp4
```

## Common Issues and Solutions

### Fix Corrupted Video
```bash
ffmpeg -i corrupted.mp4 -c copy fixed.mp4
```

### Add Silent Audio to Video
```bash
ffmpeg -i video.mp4 -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=44100 \
  -c:v copy -c:a aac -shortest output.mp4
```

### Ensure Even Dimensions (H.264 requirement)
```bash
ffmpeg -i input.mp4 -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" -c:a copy output.mp4
```

### Convert Variable to Constant Framerate
```bash
ffmpeg -i input.mp4 -vf fps=30 -c:v libx264 -c:a copy output.mp4
```

### Rotate Video
```bash
# 90° clockwise
ffmpeg -i input.mp4 -vf "transpose=1" -c:a copy output.mp4

# 90° counter-clockwise
ffmpeg -i input.mp4 -vf "transpose=2" -c:a copy output.mp4

# 180°
ffmpeg -i input.mp4 -vf "transpose=2,transpose=2" -c:a copy output.mp4
```

### Remove Metadata
```bash
ffmpeg -i input.mp4 -map_metadata -1 -c copy output.mp4
```

## Best Practices

1. **Test with short clips first** before processing long videos
2. **Use `-c copy` when possible** to avoid re-encoding (faster, lossless)
3. **Always specify codecs explicitly** to avoid unexpected defaults
4. **Ensure even dimensions** for H.264: `scale=trunc(iw/2)*2:trunc(ih/2)*2`
5. **Add `-pix_fmt yuv420p`** for maximum compatibility
6. **Use CRF (18-28) for quality control** instead of fixed bitrate
7. **Check FFmpeg version** for filter compatibility: `ffmpeg -version`
8. **Backup original files** before batch processing
9. **Use `-y` flag cautiously** (overwrites without confirmation)
10. **Normalize audio** when mixing from different sources

## Common Global Options

- `-y` - Overwrite output file without asking
- `-n` - Never overwrite output file
- `-v quiet` - Suppress output messages
- `-stats` - Show encoding statistics
- `-threads 0` - Use all CPU cores

## Reference Documentation

### Official Syntax Reference

For authoritative FFmpeg syntax rules extracted from official documentation (ffmpeg.org), consult:

```bash
references/ffmpeg-syntax-reference.md
```

This includes:
- CLI grammar and option ordering rules
- Stream specifier syntax (all patterns)
- Stream mapping and auto-selection behavior
- Seeking behavior (input vs output seeking)
- Time duration, color, size, expression syntax
- Codec options with valid ranges (libx264, AAC, libmp3lame)
- Format options (concat demuxer, probing)
- Critical gotchas and common mistakes

### Detailed Filter Reference

For comprehensive documentation on all FFmpeg filters, parameters, and advanced usage patterns, consult:

```bash
references/ffmpeg-filters.md
```

This includes:
- Video filters: drawtext, fade, xfade, scale, overlay, pad, rotate, etc.
- Audio filters: afade, amix, acrossfade, volume, aformat, etc.
- Filter graph syntax hierarchy and escaping rules
- Expression evaluation (variables, functions, constants)
- Performance tips and common pitfalls
- Version compatibility information

### Common Recipes and Patterns

For frequently used command patterns and real-world examples, consult:

```bash
references/common-recipes.md
```

This includes:
- Text and subtitles recipes
- Audio processing workflows
- Video editing patterns
- Format conversion examples
- Quality optimization techniques
- Troubleshooting solutions
- Batch processing scripts

**Access references when:**
- Need accurate syntax rules → `ffmpeg-syntax-reference.md`
- Need filter parameters or escaping rules → `ffmpeg-filters.md`
- Need real-world command examples → `common-recipes.md`

## Version Requirements

- **FFmpeg 4.3+** - Required for xfade transitions
- **FFmpeg 3.0+** - Most other filters
- Check version: `ffmpeg -version`
- Check filter availability: `ffmpeg -filters | grep filter_name`

## Output Format Compatibility

**Ensure H.264/AAC compatibility:**
```bash
-c:v libx264 -c:a aac -pix_fmt yuv420p -movflags +faststart
```

**Parameters:**
- `-pix_fmt yuv420p` - Maximum playback compatibility
- `-movflags +faststart` - Enable web streaming (MP4)
- Even dimensions required for H.264
