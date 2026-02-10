# FFmpeg Official Syntax Reference

> Source: ffmpeg.org official documentation (ffmpeg.html, ffmpeg-utils.html, ffmpeg-codecs.html, ffmpeg-formats.html, ffmpeg-filters.html)

This document provides **authoritative syntax rules** extracted from FFmpeg official documentation. Use this as the ground truth when constructing FFmpeg commands.

---

## 1. CLI Grammar

### Command Structure (Official)

```
ffmpeg [global_options] {[input_file_options] -i input_url} ... {[output_file_options] output_url} ...
```

**Ordering rules:**
- Global options MUST precede all input/output specifications
- Input file options apply ONLY to the immediately following `-i`
- Output file options apply ONLY to the immediately following output URL
- Input files MUST precede output files

**Correct:**
```bash
ffmpeg -y -ss 5 -i input.mp4 -t 10 -c:v libx264 output.mp4
#      ^   ^                   ^                    ^
#      |   input option        output options       output file
#      global option
```

**Wrong:**
```bash
# -ss after output → applies to output (different behavior)
ffmpeg -y -i input.mp4 -ss 5 -t 10 output.mp4

# codec option before -i → ERROR: option not recognized
ffmpeg -c:v libx264 -i input.mp4 output.mp4
```

### Option Syntax

```
-option_name[:stream_specifier] value
```

- Boolean options: `-an` (true), can negate with `no` prefix
- Numeric values support SI prefixes: `K` (10^3), `M` (10^6), `G` (10^9)
- Binary prefixes: `Ki` (2^10), `Mi` (2^20), `Gi` (2^30)
- Append `B` to multiply by 8 (bytes to bits): `2MB` = 2,000,000 bytes = 16,000,000 bits
- File loading: `-/option_name value_from_file` loads argument from file

**Bitrate notation examples:**
```bash
-b:v 2M      # 2,000,000 bits/s (2 Mbps)
-b:v 2000k   # 2,000,000 bits/s (same as above)
-b:v 2000K   # 2,000,000 bits/s (K = 1000)
-b:a 192k    # 192,000 bits/s
```

> **Gotcha**: FFmpeg uses **bits per second** internally. `2M` = 2 Mbps, NOT 2 MBps.

---

## 2. Stream Specifiers

Stream specifiers select which stream(s) an option applies to.

### Syntax Patterns

| Pattern | Description | Example |
|---------|-------------|---------|
| `stream_index` | Stream by absolute index | `-c:0 libx264` (first stream) |
| `stream_type` | All streams of type | `-c:v libx264` (all video) |
| `stream_type:index` | Nth stream of type | `-c:a:1 aac` (second audio) |
| `p:program_id` | Streams in program | `-c:p:1 copy` |
| `#stream_id` | Stream by format-specific ID | `-c:#0x1011 copy` |
| `m:key[:value]` | Streams matching metadata | `-c:m:language:eng copy` |
| `u` | Usable configuration streams | `-c:u copy` |

### Stream Type Identifiers

| Identifier | Stream Type |
|-----------|-------------|
| `v` | Video (or `V` for video-only, excluding thumbnails) |
| `a` | Audio |
| `s` | Subtitle |
| `d` | Data |
| `t` | Attachment |

### Common Examples

```bash
# First video stream
-c:v:0 libx264

# All audio streams
-c:a aac

# Second audio stream
-map 0:a:1

# All video streams from first input
-map 0:v

# Specific stream by index
-map 0:3
```

---

## 3. Stream Mapping (`-map`)

### Automatic Selection (without -map)

Without `-map`, FFmpeg auto-selects:
- **Video**: highest resolution stream
- **Audio**: most channels stream
- **Subtitle**: first found stream

### Manual Selection (with -map)

> **Critical**: Using `-map` **disables all automatic stream selection**. You must explicitly map every stream you want in the output.

```bash
# Map video from input 0, audio from input 1
ffmpeg -i video.mp4 -i audio.mp3 -map 0:v -map 1:a output.mp4

# Map all streams from input 0
ffmpeg -i input.mp4 -map 0 output.mp4

# Exclude subtitle streams (negative mapping)
ffmpeg -i input.mp4 -map 0 -map -0:s output.mp4
```

**Common mistake:**
```bash
# Missing audio! -map disables auto-selection
ffmpeg -i input.mp4 -map "[v]" output.mp4
# Fix: add -map for audio too
ffmpeg -i input.mp4 -map "[v]" -map 0:a output.mp4
```

---

## 4. Seeking Behavior

### Input Seeking (`-ss` before `-i`)

```bash
ffmpeg -ss 30 -i input.mp4 -c copy output.mp4
```

- **Fast**: Seeks directly to nearest keyframe in input
- **Approximate**: May not land exactly at requested time
- Works well with `-c copy` (stream copy)
- Timestamps in output start at approximately 0

### Output Seeking (`-ss` after `-i`)

```bash
ffmpeg -i input.mp4 -ss 30 -c:v libx264 output.mp4
```

- **Accurate**: Decodes all frames, discards until timestamp reached
- **Slow**: Must decode everything from start to seek point
- Required for frame-accurate cutting
- Timestamps are shifted

### Combined Seeking (Best Practice)

```bash
ffmpeg -ss 30 -i input.mp4 -ss 0.5 -c:v libx264 output.mp4
```

- Input seeking jumps near target (fast)
- Output seeking fine-tunes (accurate)
- Best of both worlds

### `-accurate_seek` (default: enabled)

- With `-accurate_seek`: Decodes and discards frames between seek point and target
- With `-noaccurate_seek`: Preserves frames from seek point (may start slightly earlier)
- Stream copy (`-c copy`) always seeks to nearest keyframe regardless

### `-to` vs `-t` with `-ss`

```bash
# -to is ABSOLUTE (end time in input)
ffmpeg -ss 10 -i input.mp4 -to 20 output.mp4  # extracts 10s (10→20)

# -t is RELATIVE (duration from seek point)
ffmpeg -ss 10 -i input.mp4 -t 20 output.mp4   # extracts 20s (10→30)
```

> **Gotcha**: When `-ss` is before `-i`, `-to` becomes relative to the new start time.

---

## 5. Stream Copy vs Re-encoding

### Stream Copy (`-c copy`)

```bash
ffmpeg -i input.mp4 -c copy output.mp4
```

- **No re-encoding**: Preserves original quality exactly
- **Fast**: Only demuxes and remuxes
- **Cannot use filters**: Filters require decoded frames
- **Keyframe-accurate only**: Cuts may not be frame-exact

### Re-encoding

```bash
ffmpeg -i input.mp4 -c:v libx264 -c:a aac output.mp4
```

- **Allows filters**: Can apply any filter chain
- **Frame-accurate**: Precise cuts possible
- **Slower**: Full decode/encode cycle
- **Quality loss**: Unless using lossless settings

**Trade-off decision:**

| Need | Use |
|------|-----|
| Fast copy, no processing | `-c copy` |
| Apply filters | Re-encode affected stream |
| Frame-accurate cut | Re-encode video |
| Preserve exact quality | `-c copy` or lossless codec |

---

## 6. Time Duration Syntax

FFmpeg accepts two duration formats:

### Format 1: HH:MM:SS.mmm

```
[-][HH:]MM:SS[.m...]
```

- Hours are optional
- Fractional seconds use arbitrary decimal places

```bash
-ss 01:23:45.678   # 1 hour, 23 min, 45.678 sec
-ss 5:30            # 5 min, 30 sec
-ss 0:0:5.5         # 5.5 seconds
```

### Format 2: Seconds with Unit Suffix

```
[-]S+[.m...][s|ms|us]
```

- Default unit is seconds if no suffix
- `s` = seconds, `ms` = milliseconds, `us` = microseconds

```bash
-ss 90          # 90 seconds
-ss 5.5         # 5.5 seconds
-ss 5500ms      # 5.5 seconds
-t 10           # 10 seconds
```

---

## 7. Color Specification

```
[0x|#]RRGGBB[AA][@alpha]
```

- Hex format: `0xRRGGBB` or `#RRGGBB`
- Optional alpha: `AA` suffix or `@alpha` (0.0-1.0)
- Named colors: `black`, `white`, `red`, `green`, `blue`, `none` (transparent)
- Special: `random` generates random color

```bash
fontcolor=white
fontcolor=#FF0000
fontcolor=0xFF0000
boxcolor=black@0.5      # 50% transparent black
fillcolor=none           # transparent (for PNG)
```

---

## 8. Size (Resolution) Specification

```
widthxheight
```

Or use abbreviations:

| Abbreviation | Resolution |
|-------------|------------|
| `sqcif` | 128x96 |
| `qcif` | 176x144 |
| `cif` | 352x288 |
| `vga` | 640x480 |
| `svga` | 800x600 |
| `hd480` | 852x480 |
| `hd720` | 1280x720 |
| `hd1080` | 1920x1080 |
| `2k` | 2048x1080 |
| `4k` | 4096x2160 |
| `uhd2160` | 3840x2160 |

```bash
-s 1920x1080
-s hd1080
```

---

## 9. Expression Syntax

FFmpeg supports expressions in filter parameters (used by drawtext, overlay, fade, etc.).

### Operators

| Operator | Description |
|----------|-------------|
| `+`, `-`, `*`, `/` | Arithmetic |
| `^` | Exponentiation |
| `>`, `>=`, `<`, `<=`, `==`, `!=` | Comparison (return 0.0 or 1.0) |
| `*` (unary) | NOT (0.0 if nonzero, 1.0 if zero) |
| `-` (unary) | Negate |

### Functions

| Function | Description |
|----------|-------------|
| `abs(x)` | Absolute value |
| `max(x, y)` | Maximum |
| `min(x, y)` | Minimum |
| `mod(x, y)` | Modulo |
| `pow(x, y)` | Power |
| `sqrt(x)` | Square root |
| `sin(x)`, `cos(x)`, `tan(x)` | Trigonometric |
| `exp(x)` | e^x |
| `log(x)` | Natural log |
| `ceil(x)`, `floor(x)`, `trunc(x)` | Rounding |
| `between(x, min, max)` | 1.0 if min <= x <= max |
| `if(cond, then, else)` | Conditional |
| `ifnot(cond, then, else)` | Inverse conditional |
| `clip(x, min, max)` | Clamp value |
| `st(var, expr)` | Store value in variable (0-9) |
| `ld(var)` | Load value from variable (0-9) |
| `random(seed)` | Random 0.0-1.0 |
| `not(x)` | Logical NOT |

### Constants

| Constant | Value |
|----------|-------|
| `PI` | 3.14159... |
| `E` | 2.71828... |
| `PHI` | 1.61803... (golden ratio) |

### Common Expression Patterns

```bash
# Center text horizontally
x=(w-text_w)/2

# Center overlay
x=(W-w)/2:y=(H-h)/2

# Show between 5 and 10 seconds
enable='between(t,5,10)'

# Scrolling text (moves right to left)
x='w-mod(t*100,w+text_w)'

# Blinking text (toggle every 0.5 seconds)
enable='lt(mod(t,1),0.5)'

# Dynamic font size based on time
fontsize='20+10*sin(t*2)'

# Store and retrieve values
x='st(0,w/2);ld(0)-text_w/2'
```

---

## 10. Codec Options

### libx264 (H.264 Video Encoder)

| Option | Range | Default | Description |
|--------|-------|---------|-------------|
| `-crf` | 0-51 | 23 | Quality (0=lossless, 18=visually lossless, 23=good, 28=web) |
| `-preset` | see below | medium | Speed/quality tradeoff |
| `-tune` | see below | (none) | Content-type optimization |
| `-profile:v` | see below | (auto) | H.264 profile |
| `-level` | 1.0-6.2 | (auto) | H.264 level |
| `-g` | 1-250+ | 250 | GOP size (keyframe interval in frames) |
| `-bf` | 0-16 | 3 | Max B-frames between references |
| `-b:v` | bits/s | (none) | Target bitrate (use with `-maxrate`/`-bufsize`) |
| `-maxrate` | bits/s | (none) | Maximum bitrate |
| `-bufsize` | bits | (none) | Rate control buffer size |

**Presets** (speed → quality):
`ultrafast` > `superfast` > `veryfast` > `faster` > `fast` > `medium` > `slow` > `slower` > `veryslow` > `placebo`

**Tunes:**
- `film` - Live action content
- `animation` - Animated content
- `grain` - Preserve film grain
- `stillimage` - Still image content
- `fastdecode` - Faster decoding
- `zerolatency` - Low-latency streaming

**Profiles:**
- `baseline` - Most compatible (no B-frames, no CABAC)
- `main` - Good compatibility
- `high` - Best quality (default)
- `high10` - 10-bit color depth
- `high422` - 4:2:2 chroma subsampling
- `high444` - 4:4:4 chroma subsampling (predictive)

```bash
# Recommended: CRF-based quality control
ffmpeg -i input.mp4 -c:v libx264 -crf 23 -preset medium output.mp4

# Streaming: constrained bitrate
ffmpeg -i input.mp4 -c:v libx264 -b:v 2M -maxrate 2.5M -bufsize 5M output.mp4

# Maximum compatibility
ffmpeg -i input.mp4 -c:v libx264 -profile:v baseline -level 3.1 -pix_fmt yuv420p output.mp4

# Low latency
ffmpeg -i input.mp4 -c:v libx264 -preset fast -tune zerolatency output.mp4
```

### AAC (Audio Encoder)

| Option | Range | Default | Description |
|--------|-------|---------|-------------|
| `-b:a` | bits/s | 128k | Target bitrate |
| `-profile:a` | see below | aac_low | AAC profile |
| `-aac_coder` | see below | twoloop | Encoding algorithm |

**Profiles:** `aac_low` (LC), `aac_ltp` (LTP), `mpeg2_aac_low` (MPEG-2 LC)

**Coders:**
- `twoloop` - Default, good quality
- `anmr` - Best quality, very slow
- `fast` - Fastest, lower quality

```bash
# Standard quality
ffmpeg -i input.mp4 -c:a aac -b:a 192k output.mp4

# High quality
ffmpeg -i input.mp4 -c:a aac -b:a 256k -profile:a aac_low output.mp4

# VBR (variable bitrate, quality-based)
ffmpeg -i input.mp4 -c:a aac -q:a 2 output.mp4
```

### libmp3lame (MP3 Encoder)

| Option | Range | Default | Description |
|--------|-------|---------|-------------|
| `-b:a` | bits/s | 128k | CBR bitrate |
| `-q:a` | 0-9 | 4 | VBR quality (0=best ~245kbps, 9=worst ~65kbps) |
| `-compression_level` | 0-9 | 5 | Encoding complexity (0=best/slowest, 9=worst/fastest) |
| `-joint_stereo` | 0/1 | 1 | Joint stereo encoding |
| `-reservoir` | 0/1 | 1 | Bit reservoir (smoother VBR) |

```bash
# CBR 192kbps
ffmpeg -i input.wav -c:a libmp3lame -b:a 192k output.mp3

# VBR high quality (~190kbps average)
ffmpeg -i input.wav -c:a libmp3lame -q:a 2 output.mp3

# VBR standard quality (~130kbps average)
ffmpeg -i input.wav -c:a libmp3lame -q:a 4 output.mp3
```

**VBR Quality Reference:**

| `-q:a` | Average Bitrate |
|---------|----------------|
| 0 | ~245 kbps |
| 2 | ~190 kbps |
| 4 | ~130 kbps |
| 6 | ~115 kbps |
| 9 | ~65 kbps |

> **Gotcha**: VBR (`-q:a`) and CBR (`-b:a`) are mutually exclusive. Don't use both.

---

## 11. Format Options

### Concat Demuxer

Script format for file-based concatenation:

```
ffconcat version 1.0

file segment1.mp4
duration 5.0
outpoint 5.0

file segment2.mp4
duration 10.0

file segment3.mp4
```

**Directives:**
- `file` - Path to media file (required)
- `duration` - Duration of the file
- `inpoint` - Start time within the file
- `outpoint` - End time within the file

**Options:**
- `-safe 0` - Allow unsafe file paths (absolute paths, `..`)
- `-auto_convert 1` - Auto-convert parameters for concat compatibility

```bash
# Standard usage
ffmpeg -f concat -safe 0 -i filelist.txt -c copy output.mp4

# With trimming per segment
# filelist.txt:
# ffconcat version 1.0
# file input1.mp4
# inpoint 5.0
# outpoint 15.0
# file input2.mp4
# inpoint 0.0
# outpoint 30.0
```

### Probing Options

```bash
# Increase probe size for problematic files
ffmpeg -probesize 50M -analyzeduration 100M -i input.mp4 output.mp4
```

| Option | Default | Description |
|--------|---------|-------------|
| `-probesize` | 5,000,000 bytes | Size of data to probe |
| `-analyzeduration` | 5,000,000 µs | Duration of data to analyze |

### Output Optimization

```bash
# Web-optimized MP4 (move moov atom to front)
ffmpeg -i input.mp4 -c copy -movflags +faststart output.mp4

# Fragmented MP4 (for streaming)
ffmpeg -i input.mp4 -c copy -movflags frag_keyframe+empty_moov output.mp4
```

---

## 12. Critical Gotchas

### 1. Option Ordering

Options apply to the NEXT specified file only:

```bash
# CORRECT: -ss applies to input
ffmpeg -ss 10 -i input.mp4 -t 5 output.mp4

# DIFFERENT: -ss applies to output (slower, accurate)
ffmpeg -i input.mp4 -ss 10 -t 5 output.mp4
```

### 2. -map Disables Auto-Selection

```bash
# Auto-selects video + audio + subtitle
ffmpeg -i input.mp4 output.mp4

# ONLY maps video! Audio is lost!
ffmpeg -i input.mp4 -map 0:v output.mp4

# Fix: explicitly map audio too
ffmpeg -i input.mp4 -map 0:v -map 0:a output.mp4
```

### 3. Stream Copy Cannot Use Filters

```bash
# ERROR: filters require re-encoding
ffmpeg -i input.mp4 -vf "scale=1280:720" -c copy output.mp4

# CORRECT: re-encode video, copy audio
ffmpeg -i input.mp4 -vf "scale=1280:720" -c:v libx264 -c:a copy output.mp4
```

### 4. Bitrate Units

FFmpeg uses **bits per second**, not bytes:

```bash
-b:v 2M     # 2 Megabits/s = 250 KiloBytes/s
-b:a 192k   # 192 kilobits/s = 24 KiloBytes/s
```

### 5. Even Dimensions for H.264

H.264 requires width and height to be divisible by 2:

```bash
# May fail if source has odd dimensions
ffmpeg -i input.mp4 -c:v libx264 output.mp4

# Safe: force even dimensions
ffmpeg -i input.mp4 -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" -c:v libx264 output.mp4
```

### 6. Filter Escaping (Multi-Level)

Three levels of escaping may be needed:

```bash
# Level 1: Filter option value escaping
# Colon in text: escape with backslash
drawtext=text='Time\: 12\:30'

# Level 2: Filtergraph special characters (:[],;)
# Wrapped in single quotes for the shell
-vf "drawtext=text='Hello World':fontsize=48"

# Level 3: Shell metacharacters
# Use double quotes around -filter_complex, single quotes inside
ffmpeg -i input.mp4 -filter_complex "[0:v]drawtext=text='Hello':fontsize=48[out]" ...
```

### 7. Pixel Format Compatibility

```bash
# Ensure maximum playback compatibility
-pix_fmt yuv420p

# Check supported pixel formats for encoder
ffmpeg -h encoder=libx264 | grep pix_fmts
```

### 8. Audio Sample Rate Mismatch

When mixing audio from different sources:
```bash
# Normalize sample rates before mixing
[0:a]aformat=sample_rates=44100:channel_layouts=stereo[a0];
[1:a]aformat=sample_rates=44100:channel_layouts=stereo[a1];
[a0][a1]amix=inputs=2[out]
```
