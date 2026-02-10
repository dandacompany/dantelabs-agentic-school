# FFmpeg Filters Reference

This document provides detailed information about FFmpeg filters used in video, audio, and image processing.

## Video Filters

### drawtext - Text Overlay

Add text overlays to video with extensive customization options.

**Basic Syntax:**
```bash
-vf "drawtext=fontfile=/path/to/font.ttf:text='Hello':fontsize=48:fontcolor=white:x=10:y=10"
```

**Key Parameters:**
- `fontfile` - Path to TrueType font file (required)
- `text` - Text content to display (escape single quotes with '')
- `fontsize` - Font size in pixels (default: 16)
- `fontcolor` - Color name or hex value (default: black)
- `x`, `y` - Position coordinates or expressions
  - Numbers: absolute pixels
  - `(w-text_w)/2` - center horizontally
  - `(h-text_h)/2` - center vertically
  - `w-text_w-10` - 10px from right edge
  - `h-th-10` - 10px from bottom edge
- `enable` - Time expression for when to show text
  - `'between(t,5,10)'` - show between 5-10 seconds
- `box` - Draw background box (0 or 1)
- `boxcolor` - Box color with alpha (e.g., `black@0.5`)
- `boxborderw` - Box border width in pixels

**Common Expressions:**
- `w` - video width
- `h` - video height
- `text_w` - rendered text width
- `text_h` - rendered text height (including line height)
- `th` - rendered text height (text only)
- `t` - timestamp in seconds

**Examples:**
```bash
# Center text
drawtext=fontfile=Arial.ttf:text='Centered':x=(w-text_w)/2:y=(h-text_h)/2

# Bottom subtitle with background
drawtext=fontfile=Arial.ttf:text='Subtitle':x=(w-text_w)/2:y=h-th-20:box=1:boxcolor=black@0.5:boxborderw=5

# Timed text (show from 5 to 10 seconds)
drawtext=fontfile=Arial.ttf:text='Limited':enable='between(t,5,10)'
```

---

### fade - Video Fade In/Out

Apply fade in or fade out effects to video.

**Syntax:**
```bash
-vf "fade=type=in:st=0:d=2"
```

**Parameters:**
- `type` - `in` or `out`
- `st` - Start time in seconds
- `d` - Duration in seconds
- `color` - Fade color (default: black)

**Examples:**
```bash
# Fade in from black for 2 seconds
fade=type=in:st=0:d=2

# Fade out to black at 28 seconds for 2 seconds
fade=type=out:st=28:d=2

# Fade in from white
fade=type=in:st=0:d=2:color=white
```

---

### xfade - Video Transitions

Apply transition effects between two video streams (FFmpeg 4.3+).

**Syntax:**
```bash
-filter_complex "[0:v][1:v]xfade=transition=fade:duration=1:offset=5[v]"
```

**Parameters:**
- `transition` - Transition type:
  - `fade`, `fadeblack`, `fadewhite`
  - `wipeleft`, `wiperight`, `wipeup`, `wipedown`
  - `slideleft`, `slideright`, `slideup`, `slidedown`
  - `circlecrop`, `rectcrop`, `distance`
  - `fadefast`, `fadeslow`
  - `pixelize`, `dissolve`, `radial`
  - `smoothleft`, `smoothright`, `smoothup`, `smoothdown`
  - And many more...
- `duration` - Transition duration in seconds
- `offset` - Time when transition starts (in first video)

**Examples:**
```bash
# Fade transition between two videos
[0:v][1:v]xfade=transition=fade:duration=1:offset=5[v]

# Wipe left transition
[0:v][1:v]xfade=transition=wipeleft:duration=0.5:offset=10[v]
```

---

### scale - Resize Video

Resize video to specific dimensions or maintain aspect ratio.

**Syntax:**
```bash
-vf "scale=1920:1080"
```

**Parameters:**
- `width:height` - Target dimensions

**Special values (from official docs):**

| Value | Meaning |
|-------|---------|
| Number | Exact pixels |
| `-1` | Maintain aspect ratio (may produce odd number) |
| `-2` | Maintain aspect ratio, round to nearest **even** value |
| `iw`, `ih` | Input width/height |
| `ow`, `oh` | Output width/height (for chained expressions) |
| `iw*0.5` | 50% of input width |
| `trunc(iw/2)*2` | Force even dimensions (manual) |

> **Tip**: Use `-2` instead of `-1` when encoding with H.264 to automatically ensure even dimensions.

**Special Options:**
- `force_original_aspect_ratio` - `decrease` or `increase`
- `flags` - Scaling algorithm: `lanczos` (sharpest), `bicubic` (default), `bilinear` (fastest)

**Examples:**
```bash
# Scale to 720p, maintaining aspect ratio
scale=1280:720

# Scale width to 1920, auto-calculate height (ensure even)
scale=1920:-2

# Scale to 50% size
scale=iw*0.5:ih*0.5

# Ensure even dimensions (for H.264)
scale=trunc(iw/2)*2:trunc(ih/2)*2

# High-quality downscale with Lanczos
scale=1280:720:flags=lanczos

# Fit within 1920x1080 maintaining aspect ratio + pad
scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2
```

---

### overlay - Video/Image Overlay

Overlay one video/image on top of another.

**Syntax:**
```bash
-filter_complex "[0:v][1:v]overlay=x=10:y=10"
```

**Parameters:**
- `x`, `y` - Position of overlay
  - Numbers: absolute pixels
  - `main_w-overlay_w` - align to right edge
  - `(main_w-overlay_w)/2` - center horizontally
- `eof_action` - Behavior when overlay ends
  - `pass` - continue main video
  - `repeat` - freeze last frame
  - `endall` - end output
- `repeatlast` - Repeat last frame (0 or 1)
- `enable` - Time expression for when to show overlay

**Variables:**
- `main_w`, `main_h` - main video dimensions
- `overlay_w`, `overlay_h` - overlay dimensions
- `t` - timestamp

**Examples:**
```bash
# Top-left corner with 10px padding
overlay=x=10:y=10

# Bottom-right corner with 10px padding
overlay=x=main_w-overlay_w-10:y=main_h-overlay_h-10

# Center overlay
overlay=x=(main_w-overlay_w)/2:y=(main_h-overlay_h)/2

# Timed overlay (show from 5 to 15 seconds)
overlay=x=10:y=10:enable='between(t,5,15)'
```

---

### pad - Add Padding

Add padding/borders around video.

**Syntax:**
```bash
-vf "pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black"
```

**Parameters:**
- `width:height` - Output dimensions
- `x:y` - Position of input video
- `color` - Padding color (default: black)

**Variables:**
- `iw`, `ih` - input dimensions
- `ow`, `oh` - output dimensions

**Examples:**
```bash
# Center video in 1920x1080 frame with black bars
pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black

# Add 10px black border around video
pad=iw+20:ih+20:10:10:black
```

---

### rotate - Rotate Video

Rotate video by specified angle.

**Syntax:**
```bash
-vf "rotate=angle=PI/4:fillcolor=none"
```

**Parameters:**
- `angle` - Rotation angle in radians
  - `PI/2` - 90 degrees
  - `PI` - 180 degrees
  - `3*PI/2` - 270 degrees
- `fillcolor` - Background color for exposed areas
  - `none` - transparent (for PNG output)
  - Color name or hex

**Examples:**
```bash
# Rotate 90 degrees clockwise
rotate=PI/2:fillcolor=black

# Rotate 45 degrees with transparent background
rotate=PI/4:fillcolor=none
```

---

### colorchannelmixer - Adjust Color Channels

Modify color channels including alpha (opacity).

**Syntax:**
```bash
-vf "colorchannelmixer=aa=0.5"
```

**Parameters:**
- `aa` - Alpha channel multiplier (0.0 to 1.0)
  - `1.0` - fully opaque (default)
  - `0.5` - 50% transparent
  - `0.0` - fully transparent

**Examples:**
```bash
# 50% opacity
colorchannelmixer=aa=0.5

# 25% opacity
colorchannelmixer=aa=0.25
```

---

### concat - Concatenate Videos

Concatenate multiple video/audio streams.

**Syntax:**
```bash
-filter_complex "[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[outv][outa]"
```

**Parameters:**
- `n` - Number of input segments
- `v` - Number of output video streams (default: 1)
- `a` - Number of output audio streams (default: 0)

**Examples:**
```bash
# Concatenate 3 videos with audio
[0:v][0:a][1:v][1:a][2:v][2:a]concat=n=3:v=1:a=1[outv][outa]

# Concatenate video-only streams
[0:v][1:v][2:v]concat=n=3:v=1:a=0[outv]
```

---

## Audio Filters

### afade - Audio Fade In/Out

Apply fade in or fade out effects to audio.

**Syntax:**
```bash
-af "afade=type=in:st=0:d=2"
```

**Parameters:**
- `type` - `in` or `out`
- `st` - Start time in seconds
- `d` - Duration in seconds
- `curve` - Fade curve type (optional)
  - `tri` - linear (default)
  - `qua` - quadratic
  - `cub` - cubic
  - `exp` - exponential

**Examples:**
```bash
# Fade in for 2 seconds
afade=type=in:st=0:d=2

# Fade out at 28 seconds for 2 seconds
afade=type=out:st=28:d=2

# Exponential fade in
afade=type=in:st=0:d=2:curve=exp
```

---

### amix - Mix Multiple Audio Streams

Mix multiple audio streams together.

**Syntax:**
```bash
-filter_complex "[0:a][1:a]amix=inputs=2:duration=first[a]"
```

**Parameters:**
- `inputs` - Number of input streams
- `duration` - Output duration
  - `longest` - duration of longest input
  - `shortest` - duration of shortest input
  - `first` - duration of first input
- `dropout_transition` - Smooth transition time in seconds

**Examples:**
```bash
# Mix two audio tracks, use first video's duration
[0:a][1:a]amix=inputs=2:duration=first[a]

# Mix three tracks, use longest duration
[0:a][1:a][2:a]amix=inputs=3:duration=longest[a]
```

---

### acrossfade - Audio Crossfade

Crossfade between two audio streams.

**Syntax:**
```bash
-filter_complex "[0:a][1:a]acrossfade=d=2[a]"
```

**Parameters:**
- `d` - Crossfade duration in seconds
- `c1`, `c2` - Crossfade curve types
  - `tri` - linear (default)
  - `qua` - quadratic
  - `cub` - cubic
  - `exp` - exponential

**Examples:**
```bash
# 2-second linear crossfade
[0:a][1:a]acrossfade=d=2[a]

# 1-second exponential crossfade
[0:a][1:a]acrossfade=d=1:c1=exp:c2=exp[a]
```

---

### volume - Adjust Volume

Adjust audio volume.

**Syntax:**
```bash
-af "volume=0.5"
```

**Parameters:**
- `volume` - Volume multiplier
  - `1.0` - original volume (default)
  - `0.5` - 50% volume
  - `2.0` - 200% volume (may cause clipping)
- `precision` - `fixed` or `float` or `double`

**Examples:**
```bash
# Reduce volume to 50%
volume=0.5

# Increase volume to 150%
volume=1.5

# Mute audio
volume=0
```

---

### aformat - Audio Format Conversion

Convert audio to specific format/sample rate/channel layout.

**Syntax:**
```bash
-af "aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=stereo"
```

**Parameters:**
- `sample_fmts` - Sample format
  - `fltp` - float planar
  - `s16` - signed 16-bit
- `sample_rates` - Sample rate in Hz
  - `44100` - CD quality
  - `48000` - DVD quality
- `channel_layouts` - Channel layout
  - `mono`, `stereo`, `5.1`

**Examples:**
```bash
# Convert to 44.1kHz stereo
aformat=sample_rates=44100:channel_layouts=stereo

# Convert to float planar format
aformat=sample_fmts=fltp
```

---

### atrim - Trim Audio

Extract portion of audio stream.

**Syntax:**
```bash
-af "atrim=start=5:duration=10"
```

**Parameters:**
- `start` - Start time in seconds
- `end` - End time in seconds
- `duration` - Duration in seconds

**Examples:**
```bash
# Extract 10 seconds starting at 5 seconds
atrim=start=5:duration=10

# Extract from 5 to 15 seconds
atrim=start=5:end=15
```

---

### adelay - Delay Audio

Add delay to audio stream.

**Syntax:**
```bash
-af "adelay=1000|1000"
```

**Parameters:**
- Delays in milliseconds, pipe-separated for each channel
- `1000|1000` - 1 second delay on both channels (stereo)

**Examples:**
```bash
# 1-second delay on both channels
adelay=1000|1000

# 500ms delay
adelay=500|500
```

---

### aloop - Loop Audio

Loop audio stream.

**Syntax:**
```bash
-af "aloop=loop=-1:size=2e9"
```

**Parameters:**
- `loop` - Number of loops
  - `-1` - infinite loop
  - `0` - no loop (default)
  - `n` - loop n times
- `size` - Maximum loop size in samples

**Examples:**
```bash
# Infinite loop
aloop=loop=-1:size=2e9

# Loop 3 times
aloop=loop=3:size=2e9
```

---

### asetpts - Reset Audio Timestamps

Reset presentation timestamps for audio.

**Syntax:**
```bash
-af "asetpts=PTS-STARTPTS"
```

**Common Usage:**
- `PTS-STARTPTS` - Reset timestamps to start at 0

This filter is essential when concatenating or mixing audio to ensure proper synchronization.

---

## Special Inputs

### anullsrc - Silent Audio Source

Generate silent audio stream.

**Syntax:**
```bash
-f lavfi -i anullsrc=channel_layout=stereo:sample_rate=44100
```

**Parameters:**
- `channel_layout` - `mono`, `stereo`, etc.
- `sample_rate` - Sample rate in Hz (default: 44100)

**Usage:**
Used to add silent audio track to video files that don't have audio, ensuring compatibility.

**Example:**
```bash
ffmpeg -i video_no_audio.mp4 -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=44100 \
  -c:v copy -c:a aac -shortest output.mp4
```

---

## Filter Graph Syntax

### Hierarchy (Official)

A **filtergraph** is the complete filter description, consisting of:

```
filtergraph = filterchain { ";" filterchain }
filterchain = filter { "," filter }
filter      = [input_labels] filter_name [@id] [= arguments] [output_labels]
```

- **Semicolons (`;`)** separate independent filterchains
- **Commas (`,`)** chain filters sequentially within a filterchain
- **Labels (`[name]`)** connect outputs to inputs across filterchains

### Filter Argument Formats

```bash
# Key-value pairs (most common)
filter_name=key1=value1:key2=value2

# Positional values
filter_name=value1:value2

# Mixed format
filter_name=value1:key2=value2

# Multi-item values use pipe separator
filter_name=key=value1|value2|value3
```

### Simple Filters (`-vf`, `-af`)

For single input/output (shorthand for simple filterchains):
```bash
-vf "filter1=param1=value1,filter2=param2=value2"
-af "filter1,filter2"
```

### Complex Filter Graphs (`-filter_complex`)

For multiple inputs/outputs or cross-stream routing:
```bash
-filter_complex "
  [0:v]scale=1920:1080[scaled];
  [scaled][1:v]overlay=x=10:y=10[out]
" -map "[out]"
```

**Stream Labels:**
- `[0:v]` - first input, video stream
- `[0:a]` - first input, audio stream
- `[1:v]` - second input, video stream
- `[label]` - intermediate or output label
- Unlabeled outputs auto-connect to next filter's unlabeled input

**Chain Operators:**
- `,` - chain filters sequentially (output → input)
- `;` - separate independent filterchains (use labels to connect)

### Escaping Rules (Multi-Level)

FFmpeg filter strings require up to 3 levels of escaping:

**Level 1 — Filter option values:**
Escape special characters within option values using backslash:
```bash
# Colon in text content
drawtext=text='Time\: 12\:30'

# Single quote in text
drawtext=text='don'\''t'
```

**Level 2 — Filtergraph structure characters:**
These characters have special meaning in filtergraph syntax: `[ ] , ; '`
```bash
# Use backslash to escape if needed literally
drawtext=text='Hello\; World'
```

**Level 3 — Shell metacharacters:**
```bash
# Wrap -filter_complex value in double quotes
# Use single quotes for inner string values
ffmpeg -i input.mp4 -filter_complex "[0:v]drawtext=text='Hello World':fontsize=48[out]" ...

# Avoid shell interpretation of special chars
ffmpeg -i input.mp4 -vf "drawtext=text='Price\: \$100'" ...
```

**Best practice**: Use double quotes around the entire filter string, single quotes for text values inside.

### Expression Evaluation

Many filter parameters accept expressions with these variables and functions:

**Common Variables:**

| Variable | Scope | Description |
|----------|-------|-------------|
| `t` | drawtext, overlay, fade | Timestamp in seconds |
| `n` | drawtext | Frame number |
| `w`, `h` | drawtext | Video dimensions |
| `text_w`, `text_h` | drawtext | Rendered text dimensions |
| `W`, `H` | overlay | Main input dimensions |
| `w`, `h` | overlay | Overlay input dimensions |
| `main_w`, `main_h` | overlay | Main input (alias) |
| `overlay_w`, `overlay_h` | overlay | Overlay (alias) |
| `iw`, `ih` | scale | Input dimensions |
| `ow`, `oh` | pad | Output dimensions |

**Useful Functions:**

| Function | Example |
|----------|---------|
| `between(x, min, max)` | `enable='between(t,5,10)'` |
| `if(cond, then, else)` | `fontsize='if(lt(t,5),24,48)'` |
| `mod(x, y)` | `x='mod(t*100,w)'` (scrolling) |
| `sin(x)`, `cos(x)` | `fontsize='20+10*sin(t*2)'` (pulsing) |
| `st(var, expr)` | `x='st(0,w/2);ld(0)-text_w/2'` |
| `ld(var)` | Load stored variable (0-9) |

**Constants:** `PI` (3.14159...), `E` (2.71828...), `PHI` (1.61803...)

---

## Performance Tips

1. **Avoid Re-encoding When Possible**
   - Use `-c copy` to stream copy when no processing is needed
   - Only apply filters to streams that need modification

2. **Use Hardware Acceleration**
   - `-hwaccel auto` - enable hardware decoding
   - `-c:v h264_videotoolbox` - hardware encoding (macOS)

3. **Optimize Filter Order**
   - Apply scale/crop early to reduce processing load
   - Combine filters when possible

4. **Use Two-Pass Encoding for Better Quality**
   ```bash
   # Pass 1
   ffmpeg -i input.mp4 -c:v libx264 -b:v 2M -pass 1 -f null /dev/null
   # Pass 2
   ffmpeg -i input.mp4 -c:v libx264 -b:v 2M -pass 2 output.mp4
   ```

---

## Common Pitfalls

1. **Escaping Special Characters (3 levels)**
   - Level 1 — Colons in text: `text='Time\: 12\:30'`
   - Level 2 — Single quotes in text: `text='don'\''t'`
   - Level 3 — Shell escaping: wrap `-filter_complex` in double quotes
   - **Rule of thumb**: Double quotes outside, single quotes inside, backslash for colons

2. **Even Dimensions Required**
   - H.264 requires width AND height divisible by 2
   - Use `scale=-2:720` (auto-even) or `scale=trunc(iw/2)*2:trunc(ih/2)*2` (manual)
   - **Gotcha**: `scale=1920:-1` may produce odd height → use `-2` instead

3. **Audio Sync Issues**
   - Always use `asetpts=PTS-STARTPTS` after trimming or splitting audio
   - Use `setpts=PTS-STARTPTS` for video when concatenating
   - Normalize `sample_rates` and `channel_layouts` before mixing different sources

4. **Filter Order Matters**
   - Scale/crop BEFORE overlay → reduces processing load
   - Format conversion (pix_fmt) EARLY in the chain
   - `setpts`/`asetpts` AFTER trim/split operations

5. **Time Base Issues**
   - Use `settb=AVTB` before xfade transitions
   - Essential when combining videos with different timebase settings
   - Without it: transitions may have wrong timing

6. **Stream Copy vs Filters**
   - `-c copy` with `-vf` or `-af` → ERROR: filters need decoded frames
   - **Fix**: Re-encode the stream that needs filtering: `-c:v libx264 -c:a copy`

7. **-map Disables Auto-Selection**
   - Using `-map "[v]"` without `-map 0:a` → silent output
   - Always map ALL desired streams when using `-map`

8. **Bitrate Units**
   - FFmpeg uses bits/s, not bytes/s
   - `-b:v 2M` = 2 Megabits/s = 250 KB/s
   - Use `K` (1000), `M` (1000000), `G` (1000000000)

---

## Version Compatibility

- **xfade filter**: Requires FFmpeg 4.3+
- **Most other filters**: Available in FFmpeg 3.0+

Check FFmpeg version:
```bash
ffmpeg -version
```

Check available filters:
```bash
ffmpeg -filters | grep <filter_name>
```
