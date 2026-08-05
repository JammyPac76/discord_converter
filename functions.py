import subprocess
from pathlib import Path
import argparse
from tempfile import NamedTemporaryFile
import sys

def get_null():
    match sys.platform:
        case "linux": return "/dev/null"
        case _: return "NUL"

def download_video(input_link):
    download_output = f"{NamedTemporaryFile().name}.mp4"
    subprocess.run(["yt-dlp", "-S", "ext:mp4", input_link, "-o", download_output])

    return download_output

def parse_arguments():
    parser = argparse.ArgumentParser(
            description="A script used for compressing videos (specifically made for Discord's pesky filesize limit)"
            )

    parser.add_argument(
            "input_file",
            help="File input, where you insert the video."
            )

    parser.add_argument(
            "output_file",
            help="File output, where your processed video will go to."
            )

    parser.add_argument(
            "-s", "--size",
            help="Target filesize.",
            default=9.5
            )

    parser.add_argument(
            "--download",
            help="Compress a video directly from it's source (requires yt-dlp).",
            action='store_true'
            )

    return parser.parse_args()

def assign_codec(extension):

    codecs = {".mp4": {
                "video codec": "libx264",
                "audio codec": "aac",
                      },
                ".webm": {
                    "video codec": "libvpx-vp9",
                    "audio codec": "libopus",
                          }
                  }

    video_codec = codecs[extension]["video codec"]
    audio_codec = codecs[extension]["audio codec"]

    return str(video_codec), str(audio_codec)

def compress_video(input_file, output_file, target_size=0.0, audio_bitrate=0.0, fps=0.0, pixels=0.0):

    video_bitrate = (target_size*(8024))/input_file.duration
    video_bitrate -= video_bitrate * 0.02

    ffmpeg2passlog = NamedTemporaryFile().name
    null_var = get_null()
    
    if not audio_bitrate:
        audio_bitrate = video_bitrate * 0.3148565881

    video_bitrate -= audio_bitrate

    if not fps:
        fps = int(min(input_file.fps, video_bitrate * 0.08928571429))
    if not pixels:
        pixels = int(min(input_file.height,video_bitrate * 22.5))
        pixels = pixels & ~1


    commands={
            "pass1": ["ffmpeg", "-y", "-i", str(input_file.filepath), "-c:v", output_file.video_codec, "-b:v", f"{video_bitrate}k", "-maxrate", f"{video_bitrate}k", "-bufsize", f"{video_bitrate*2}k", "-vf", f"fps={fps},scale=-2:{pixels}", "-passlogfile", f"{ffmpeg2passlog}", "-pass", "1", "-an", "-f", "null", null_var],

            "pass2": ["ffmpeg", "-y", "-i", str(input_file.filepath), "-c:v", output_file.video_codec, "-b:v", f"{video_bitrate}k", "-maxrate", f"{video_bitrate}k", "-bufsize", f"{video_bitrate*2}k", "-pass", "2", "-vf", f"fps={fps},scale=-2:{pixels}", "-passlogfile", f"{ffmpeg2passlog}", "-c:a", f"{output_file.audio_codec}", "-b:a", f"{audio_bitrate}k", str(output_file.filepath)]
            }

    for command in commands:
        print(commands[command])
        subprocess.run(commands[command])
