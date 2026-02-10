# FFmpeg Common Recipes

This document contains frequently used FFmpeg command patterns and recipes for common video/audio processing tasks.

## Table of Contents

1. [Text and Subtitles](#text-and-subtitles)
2. [Audio Processing](#audio-processing)
3. [Video Processing](#video-processing)
4. [Video Editing](#video-editing)
5. [Format Conversion](#format-conversion)
6. [Quality and Encoding](#quality-and-encoding)
7. [Troubleshooting](#troubleshooting)

---

## Text and Subtitles

### Add Text Overlay

**Basic text at bottom center:**
```bash
ffmpeg -i input.mp4 \
  -vf "drawtext=fontfile=/path/to/font.ttf:text='Hello World':fontsize=48:fontcolor=white:x=(w-text_w)/2:y=h-th-20" \
  -c:a copy output.mp4
```

**Text with background box:**
```bash
ffmpeg -i input.mp4 \
  -vf "drawtext=fontfile=/path/to/font.ttf:text='Hello':fontsize=48:fontcolor=white:x=(w-text_w)/2:y=h-th-20:box=1:boxcolor=black@0.5:boxborderw=5" \
  -c:a copy output.mp4
```

**Timed text (show from 5 to 10 seconds):**
```bash
ffmpeg -i input.mp4 \
  -vf "drawtext=fontfile=/path/to/font.ttf:text='Limited Time':fontsize=48:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2:enable='between(t,5,10)'" \
  -c:a copy output.mp4
```

### Add SRT Subtitles

**Burn subtitles into video (hardcoded):**
```bash
ffmpeg -i input.mp4 -vf "subtitles=subtitle.srt" -c:a copy output.mp4
```

**Add subtitles as separate track (soft subtitles):**
```bash
ffmpeg -i input.mp4 -i subtitle.srt -c copy -c:s mov_text output.mp4
```

**Custom subtitle styling:**
```bash
ffmpeg -i input.mp4 \
  -vf "subtitles=subtitle.srt:force_style='FontName=Arial,FontSize=24,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000'" \
  -c:a copy output.mp4
```

---

## Audio Processing

### Extract Audio from Video

**Extract as MP3:**
```bash
ffmpeg -i input.mp4 -vn -c:a libmp3lame -b:a 192k output.mp3
```

**Extract as AAC:**
```bash
ffmpeg -i input.mp4 -vn -c:a aac -b:a 192k output.aac
```

**Extract as WAV (lossless):**
```bash
ffmpeg -i input.mp4 -vn -c:a pcm_s16le output.wav
```

**Copy audio stream without re-encoding:**
```bash
ffmpeg -i input.mp4 -vn -c:a copy output.m4a
```

### Separate Video and Audio

**Create muted video:**
```bash
ffmpeg -i input.mp4 -an -c:v copy video_only.mp4
```

**Extract audio separately:**
```bash
ffmpeg -i input.mp4 -vn -c:a libmp3lame -b:a 192k audio.mp3
```

### Mix Audio Tracks

**Mix two audio files:**
```bash
ffmpeg -i video.mp4 -i music.mp3 \
  -filter_complex "[0:a]volume=1.0[a0];[1:a]volume=0.5[a1];[a0][a1]amix=inputs=2:duration=first[a]" \
  -map 0:v -map "[a]" -c:v copy output.mp4
```

**Replace video audio with new audio:**
```bash
ffmpeg -i video.mp4 -i new_audio.mp3 \
  -map 0:v -map 1:a -c:v copy -c:a aac -shortest output.mp4
```

**Mix with fade effects:**
```bash
ffmpeg -i video.mp4 -i music.mp3 \
  -filter_complex "
    [1:a]afade=t=in:st=0:d=2,afade=t=out:st=28:d=2,volume=0.5[a1];
    [0:a][a1]amix=inputs=2:duration=first[a]
  " \
  -map 0:v -map "[a]" -c:v copy output.mp4
```

### Audio Effects

**Fade in and fade out:**
```bash
ffmpeg -i input.mp4 \
  -af "afade=t=in:st=0:d=2,afade=t=out:st=28:d=2" \
  -c:v copy output.mp4
```

**Change volume:**
```bash
# 50% volume
ffmpeg -i input.mp4 -af "volume=0.5" -c:v copy output.mp4

# 150% volume
ffmpeg -i input.mp4 -af "volume=1.5" -c:v copy output.mp4
```

**Normalize audio:**
```bash
ffmpeg -i input.mp4 -af "loudnorm" -c:v copy output.mp4
```

---

## Video Processing

### Convert Image to Video

**Static image with duration:**
```bash
ffmpeg -loop 1 -i image.png -c:v libx264 -t 10 -pix_fmt yuv420p output.mp4
```

**Image with silent audio for compatibility:**
```bash
ffmpeg -loop 1 -i image.png \
  -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=44100 \
  -c:v libx264 -c:a aac -t 10 -pix_fmt yuv420p -shortest output.mp4
```

**Image slideshow from multiple images:**
```bash
ffmpeg -framerate 1/3 -pattern_type glob -i '*.jpg' \
  -c:v libx264 -pix_fmt yuv420p output.mp4
```

### Resize/Scale Video

**Scale to specific dimensions:**
```bash
ffmpeg -i input.mp4 -vf "scale=1920:1080" -c:a copy output.mp4
```

**Scale maintaining aspect ratio:**
```bash
# Width 1920, auto-calculate height
ffmpeg -i input.mp4 -vf "scale=1920:-1" -c:a copy output.mp4

# Height 1080, auto-calculate width
ffmpeg -i input.mp4 -vf "scale=-1:1080" -c:a copy output.mp4
```

**Scale to percentage:**
```bash
# 50% size
ffmpeg -i input.mp4 -vf "scale=iw*0.5:ih*0.5" -c:a copy output.mp4
```

**Ensure even dimensions (required for H.264):**
```bash
ffmpeg -i input.mp4 -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" -c:a copy output.mp4
```

### Overlay Image/Video

**Add logo watermark:**
```bash
ffmpeg -i video.mp4 -i logo.png \
  -filter_complex "[1:v]scale=150:-1[logo];[0:v][logo]overlay=10:10" \
  -c:a copy output.mp4
```

**Watermark at bottom-right:**
```bash
ffmpeg -i video.mp4 -i logo.png \
  -filter_complex "[1:v]scale=150:-1[logo];[0:v][logo]overlay=main_w-overlay_w-10:main_h-overlay_h-10" \
  -c:a copy output.mp4
```

**Centered watermark with opacity:**
```bash
ffmpeg -i video.mp4 -i logo.png \
  -filter_complex "[1:v]scale=150:-1,colorchannelmixer=aa=0.5[logo];[0:v][logo]overlay=(main_w-overlay_w)/2:(main_h-overlay_h)/2" \
  -c:a copy output.mp4
```

**Timed watermark (show from 5 to 15 seconds):**
```bash
ffmpeg -i video.mp4 -i logo.png \
  -filter_complex "[1:v]scale=150:-1[logo];[0:v][logo]overlay=10:10:enable='between(t,5,15)'" \
  -c:a copy output.mp4
```

**Picture-in-picture:**
```bash
ffmpeg -i main.mp4 -i small.mp4 \
  -filter_complex "[1:v]scale=320:-1[small];[0:v][small]overlay=main_w-overlay_w-10:10" \
  -c:a copy output.mp4
```

---

## Video Editing

### Trim/Cut Video

**Extract segment from 5 to 15 seconds:**
```bash
ffmpeg -i input.mp4 -ss 5 -to 15 -c copy output.mp4
```

**Extract 10 seconds starting at 5 seconds:**
```bash
ffmpeg -i input.mp4 -ss 5 -t 10 -c copy output.mp4
```

**Accurate cutting (slower but precise):**
```bash
ffmpeg -i input.mp4 -ss 5 -t 10 -c:v libx264 -c:a aac output.mp4
```

### Merge/Concatenate Videos

**Method 1: Concat demuxer (same codec/format):**
```bash
# Create file list
echo "file 'video1.mp4'" > list.txt
echo "file 'video2.mp4'" >> list.txt
echo "file 'video3.mp4'" >> list.txt

# Concatenate
ffmpeg -f concat -safe 0 -i list.txt -c copy output.mp4
```

**Method 2: Concat filter (different formats):**
```bash
ffmpeg -i video1.mp4 -i video2.mp4 -i video3.mp4 \
  -filter_complex "[0:v][0:a][1:v][1:a][2:v][2:a]concat=n=3:v=1:a=1[outv][outa]" \
  -map "[outv]" -map "[outa]" output.mp4
```

**Normalize before concat (different resolutions/framerates):**
```bash
ffmpeg -i video1.mp4 -i video2.mp4 \
  -filter_complex "
    [0:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30[v0];
    [1:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30[v1];
    [v0][0:a][v1][1:a]concat=n=2:v=1:a=1[outv][outa]
  " \
  -map "[outv]" -map "[outa]" output.mp4
```

### Video Transitions

**Fade transition between two videos (FFmpeg 4.3+):**
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

**Available transition types:**
- `fade`, `fadeblack`, `fadewhite`
- `wipeleft`, `wiperight`, `wipeup`, `wipedown`
- `slideleft`, `slideright`, `slideup`, `slidedown`
- `circlecrop`, `rectcrop`, `distance`, `dissolve`

### Fade In/Out Effects

**Video fade in/out:**
```bash
ffmpeg -i input.mp4 \
  -vf "fade=type=in:st=0:d=2,fade=type=out:st=28:d=2" \
  -c:a copy output.mp4
```

**Video and audio fade in/out:**
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

---

## Format Conversion

### Video Format Conversion

**MP4 to AVI:**
```bash
ffmpeg -i input.mp4 -c:v libx264 -c:a aac output.avi
```

**MOV to MP4:**
```bash
ffmpeg -i input.mov -c:v libx264 -c:a aac output.mp4
```

**Any format to MP4 (H.264 + AAC):**
```bash
ffmpeg -i input.* -c:v libx264 -c:a aac -strict experimental output.mp4
```

### GIF Creation

**Video to GIF:**
```bash
ffmpeg -i input.mp4 -vf "fps=10,scale=320:-1:flags=lanczos" -c:v gif output.gif
```

**High-quality GIF with palette:**
```bash
# Generate palette
ffmpeg -i input.mp4 -vf "fps=10,scale=320:-1:flags=lanczos,palettegen" palette.png

# Create GIF using palette
ffmpeg -i input.mp4 -i palette.png \
  -filter_complex "fps=10,scale=320:-1:flags=lanczos[x];[x][1:v]paletteuse" \
  output.gif
```

### Image Sequence

**Extract frames:**
```bash
# Every frame
ffmpeg -i input.mp4 frame_%04d.png

# 1 frame per second
ffmpeg -i input.mp4 -vf fps=1 frame_%04d.png
```

**Create video from image sequence:**
```bash
ffmpeg -framerate 30 -i frame_%04d.png -c:v libx264 -pix_fmt yuv420p output.mp4
```

---

## Quality and Encoding

### Control Video Quality

**CRF (Constant Rate Factor) - recommended:**
```bash
# CRF range: 0-51 (lower = better quality, default: 23)
ffmpeg -i input.mp4 -c:v libx264 -crf 18 -c:a copy output.mp4
```

**Bitrate control:**
```bash
# Fixed bitrate
ffmpeg -i input.mp4 -c:v libx264 -b:v 2M -c:a aac -b:a 192k output.mp4

# Two-pass encoding for better quality
# Pass 1
ffmpeg -i input.mp4 -c:v libx264 -b:v 2M -pass 1 -f null /dev/null
# Pass 2
ffmpeg -i input.mp4 -c:v libx264 -b:v 2M -pass 2 -c:a aac -b:a 192k output.mp4
```

### Encoding Presets

**Fast encoding (lower quality):**
```bash
ffmpeg -i input.mp4 -c:v libx264 -preset ultrafast output.mp4
```

**Balanced encoding:**
```bash
ffmpeg -i input.mp4 -c:v libx264 -preset medium output.mp4
```

**High-quality encoding (slow):**
```bash
ffmpeg -i input.mp4 -c:v libx264 -preset slow -crf 18 output.mp4
```

**Presets:** `ultrafast`, `superfast`, `veryfast`, `faster`, `fast`, `medium`, `slow`, `slower`, `veryslow`

### Compression

**Compress video maintaining quality:**
```bash
ffmpeg -i input.mp4 -c:v libx264 -crf 23 -preset medium -c:a aac -b:a 128k output.mp4
```

**Aggressive compression:**
```bash
ffmpeg -i input.mp4 -c:v libx264 -crf 28 -preset fast -c:a aac -b:a 96k output.mp4
```

---

## Troubleshooting

### Get Media Information

**Using ffprobe:**
```bash
ffprobe -v quiet -print_format json -show_format -show_streams input.mp4
```

**Quick info:**
```bash
ffmpeg -i input.mp4 2>&1 | grep -E 'Duration|Stream'
```

**Get video resolution:**
```bash
ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 input.mp4
```

**Get video duration:**
```bash
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 input.mp4
```

**Check if video has audio:**
```bash
ffprobe -i input.mp4 -show_streams -select_streams a -loglevel error
```

### Fix Common Issues

**Fix corrupted video:**
```bash
ffmpeg -i corrupted.mp4 -c copy fixed.mp4
```

**Fix audio sync issues:**
```bash
# Delay audio by 0.5 seconds
ffmpeg -i input.mp4 -itsoffset 0.5 -i input.mp4 -map 0:v -map 1:a -c copy output.mp4
```

**Convert variable framerate to constant:**
```bash
ffmpeg -i input.mp4 -vf fps=30 -c:v libx264 -c:a copy output.mp4
```

**Rotate video:**
```bash
# Rotate 90 degrees clockwise
ffmpeg -i input.mp4 -vf "transpose=1" -c:a copy output.mp4

# Rotate 180 degrees
ffmpeg -i input.mp4 -vf "transpose=2,transpose=2" -c:a copy output.mp4

# Rotate 90 degrees counter-clockwise
ffmpeg -i input.mp4 -vf "transpose=2" -c:a copy output.mp4
```

**Remove metadata:**
```bash
ffmpeg -i input.mp4 -map_metadata -1 -c copy output.mp4
```

**Add silent audio to video without audio:**
```bash
ffmpeg -i video.mp4 -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=44100 \
  -c:v copy -c:a aac -shortest output.mp4
```

### Performance Optimization

**Hardware acceleration (macOS):**
```bash
ffmpeg -hwaccel videotoolbox -i input.mp4 -c:v h264_videotoolbox -c:a copy output.mp4
```

**Hardware acceleration (Linux/NVIDIA):**
```bash
ffmpeg -hwaccel cuda -i input.mp4 -c:v h264_nvenc -c:a copy output.mp4
```

**Multi-threaded encoding:**
```bash
ffmpeg -i input.mp4 -c:v libx264 -threads 0 -c:a copy output.mp4
```

---

## Advanced Patterns

### Complex Filter Graphs

**Split video into multiple outputs:**
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

**Picture-in-picture with custom positioning:**
```bash
ffmpeg -i main.mp4 -i overlay.mp4 \
  -filter_complex "
    [1:v]scale=320:-1[pip];
    [0:v][pip]overlay=main_w-overlay_w-10:10:
      enable='between(t,5,15)'[v]
  " \
  -map "[v]" -map 0:a -c:a copy output.mp4
```

### Batch Processing

**Process all MP4 files in directory:**
```bash
for f in *.mp4; do
  ffmpeg -i "$f" -vf "scale=1280:720" -c:a copy "output_${f}"
done
```

**Convert all AVI to MP4:**
```bash
for f in *.avi; do
  ffmpeg -i "$f" -c:v libx264 -c:a aac "${f%.avi}.mp4"
done
```

---

## Command Structure Reference

### Basic Command Pattern

```bash
ffmpeg [global options] [input options] -i input.file [output options] output.file
```

### Common Global Options

- `-y` - Overwrite output file without asking
- `-n` - Never overwrite output file
- `-v quiet` - Suppress output messages
- `-stats` - Show encoding statistics
- `-threads 0` - Use all CPU cores

### Common Input Options

- `-ss 5` - Start reading from 5 seconds
- `-t 10` - Read only 10 seconds
- `-to 15` - Read until 15 seconds

### Common Output Options

- `-c:v libx264` - Video codec
- `-c:a aac` - Audio codec
- `-c copy` - Copy streams without re-encoding
- `-b:v 2M` - Video bitrate
- `-b:a 192k` - Audio bitrate
- `-crf 23` - Constant Rate Factor (quality)
- `-preset medium` - Encoding speed vs quality
- `-pix_fmt yuv420p` - Pixel format (for compatibility)
- `-map 0:v` - Map video stream from first input
- `-map 0:a` - Map audio stream from first input
- `-shortest` - Finish when shortest input ends

---

## Best Practices

1. **Always specify output codec explicitly** to avoid unexpected defaults
2. **Use `-c copy` when possible** to avoid re-encoding (faster, lossless)
3. **Test with short clips first** before processing long videos
4. **Use CRF for quality control** (18-23 for high quality, 23-28 for web)
5. **Ensure even dimensions** for H.264 videos (`scale=trunc(iw/2)*2:trunc(ih/2)*2`)
6. **Add `-pix_fmt yuv420p`** for maximum compatibility
7. **Use two-pass encoding** for best quality with fixed bitrate
8. **Normalize audio** when mixing from different sources
9. **Always backup original files** before batch processing
10. **Check FFmpeg version** for filter compatibility (`ffmpeg -version`)
