# clip.mp4 ffprobe
```
> ffprobe -show_format -show_streams -of json test_footage/clip.MP4 
ffprobe version 8.1.2 Copyright (c) 2007-2026 the FFmpeg developers
  built with Apple clang version 21.0.0 (clang-2100.0.123.102)
  configuration: --prefix=/opt/homebrew/Cellar/ffmpeg/8.1.2_1 --enable-shared --enable-pthreads --enable-version3 --cc=clang --host-cflags= --host-ldflags= --enable-ffplay --enable-gpl --enable-libsvtav1 --enable-libopus --enable-libx264 --enable-libmp3lame --enable-libdav1d --enable-libvmaf --enable-libvpx --enable-libx265 --enable-openssl --enable-videotoolbox --enable-audiotoolbox --enable-neon
  libavutil      60. 26.102 / 60. 26.102
  libavcodec     62. 28.102 / 62. 28.102
  libavformat    62. 12.102 / 62. 12.102
  libavdevice    62.  3.102 / 62.  3.102
  libavfilter    11. 14.102 / 11. 14.102
  libswscale      9.  5.102 /  9.  5.102
  libswresample   6.  3.102 /  6.  3.102
{
Input #0, mov,mp4,m4a,3gp,3g2,mj2, from 'test_footage/clip.MP4':
  Metadata:
    major_brand     : mp42
    minor_version   : 0
    compatible_brands: isomavc1mp42
    creation_time   : 2026-07-29T19:17:21.000000Z
  Duration: 00:03:00.00, start: 0.000000, bitrate: 30779 kb/s
  Stream #0:0[0x1](eng): Video: h264 (High) (avc1 / 0x31637661), yuvj420p(pc, bt709, progressive), 2560x1440, 30309 kb/s, 30 fps, 30 tbr, 92400 tbn (default)
    Metadata:
      creation_time   : 2026-07-29T19:17:21.000000Z
      handler_name    : VideoHandler
      encoder         : h264
  Stream #0:1[0x2](eng): Audio: aac (LC) (mp4a / 0x6134706D), 32000 Hz, mono, fltp, 96 kb/s (default)
    Metadata:
      creation_time   : 2026-07-29T19:17:21.000000Z
      handler_name    : SoundHandler
    "streams": [
        {
            "index": 0,
            "codec_name": "h264",
            "codec_long_name": "H.264 / AVC / MPEG-4 AVC / MPEG-4 part 10",
            "profile": "High",
            "codec_type": "video",
            "codec_tag_string": "avc1",
            "codec_tag": "0x31637661",
            "mime_codec_string": "avc1.640033",
            "width": 2560,
            "height": 1440,
            "coded_width": 2560,
            "coded_height": 1440,
            "has_b_frames": 0,
            "pix_fmt": "yuvj420p",
            "level": 51,
            "color_range": "pc",
            "color_space": "bt709",
            "color_transfer": "bt709",
            "color_primaries": "bt709",
            "chroma_location": "left",
            "field_order": "progressive",
            "is_avc": "true",
            "nal_length_size": "4",
            "id": "0x1",
            "r_frame_rate": "30/1",
            "avg_frame_rate": "30/1",
            "time_base": "1/92400",
            "start_pts": 0,
            "start_time": "0.000000",
            "duration_ts": 16632000,
            "duration": "180.000000",
            "bit_rate": "30309838",
            "bits_per_raw_sample": "8",
            "nb_frames": "5400",
            "extradata_size": 39,
            "disposition": {
                "default": 1,
                "dub": 0,
                "original": 0,
                "comment": 0,
                "lyrics": 0,
                "karaoke": 0,
                "forced": 0,
                "hearing_impaired": 0,
                "visual_impaired": 0,
                "clean_effects": 0,
                "attached_pic": 0,
                "timed_thumbnails": 0,
                "non_diegetic": 0,
                "captions": 0,
                "descriptions": 0,
                "metadata": 0,
                "dependent": 0,
                "still_image": 0,
                "multilayer": 0
            },
            "tags": {
                "creation_time": "2026-07-29T19:17:21.000000Z",
                "language": "eng",
                "handler_name": "\fVideoHandler",
                "encoder": "h264"
            }
        },
        {
            "index": 1,
            "codec_name": "aac",
            "codec_long_name": "AAC (Advanced Audio Coding)",
            "profile": "LC",
            "codec_type": "audio",
            "codec_tag_string": "mp4a",
            "codec_tag": "0x6134706d",
            "mime_codec_string": "mp4a.40.2",
            "sample_fmt": "fltp",
            "sample_rate": "32000",
            "channels": 1,
            "channel_layout": "mono",
            "bits_per_sample": 0,
            "initial_padding": 0,
            "id": "0x2",
            "r_frame_rate": "0/0",
            "avg_frame_rate": "0/0",
            "time_base": "1/32000",
            "start_pts": 0,
            "start_time": "0.000000",
            "duration_ts": 5760000,
            "duration": "180.000000",
            "bit_rate": "96000",
            "nb_frames": "5625",
            "extradata_size": 2,
            "disposition": {
                "default": 1,
                "dub": 0,
                "original": 0,
                "comment": 0,
                "lyrics": 0,
                "karaoke": 0,
                "forced": 0,
                "hearing_impaired": 0,
                "visual_impaired": 0,
                "clean_effects": 0,
                "attached_pic": 0,
                "timed_thumbnails": 0,
                "non_diegetic": 0,
                "captions": 0,
                "descriptions": 0,
                "metadata": 0,
                "dependent": 0,
                "still_image": 0,
                "multilayer": 0
            },
            "tags": {
                "creation_time": "2026-07-29T19:17:21.000000Z",
                "language": "eng",
                "handler_name": "\fSoundHandler"
            }
        }
    ],
    "format": {
        "filename": "test_footage/clip.MP4",
        "nb_streams": 2,
        "nb_programs": 0,
        "nb_stream_groups": 0,
        "format_name": "mov,mp4,m4a,3gp,3g2,mj2",
        "format_long_name": "QuickTime / MOV",
        "start_time": "0.000000",
        "duration": "180.000000",
        "size": "692543424",
        "bit_rate": "30779707",
        "probe_score": 100,
        "tags": {
            "major_brand": "mp42",
            "minor_version": "0",
            "compatible_brands": "isomavc1mp42",
            "creation_time": "2026-07-29T19:17:21.000000Z"
        }
    }
}
```