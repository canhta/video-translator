import argparse
import sys
import os
import yt_dlp


class yt_downloader:
    def __init__(
        self,
        video_format="bestvideo",
        audio_format="bestaudio",
        keep_original=True,
        subs_langs=["en", "vi"],
    ):
        self.video_format = video_format
        self.audio_format = audio_format
        self.keep_original = keep_original
        self.subs_langs = subs_langs
        self.ydl_opts = {
            "format": f"{video_format}+{audio_format}/best",
            "keepvideo": keep_original,
            "outtmpl": "input/%(id)s/%(id)s_%(format_id)s.%(ext)s",
            "subtitleslangs": subs_langs,
            "writesubtitles": True,
        }

    def download_video(self, url):
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                video_id = info["id"]

                # Download video without audio
                ydl_opts_video = self.ydl_opts.copy()
                ydl_opts_video["format"] = self.video_format
                ydl_opts_video["outtmpl"] = f"input/{video_id}/video.%(ext)s"
                ydl_opts_video["postprocessors"] = [
                    {
                        "key": "FFmpegVideoConvertor",
                        "preferedformat": "mp4",
                    }
                ]
                with yt_dlp.YoutubeDL(ydl_opts_video) as ydl_video:
                    ydl_video.download([url])

                # Download audio
                ydl_opts_audio = self.ydl_opts.copy()
                ydl_opts_audio["format"] = self.audio_format
                ydl_opts_audio["outtmpl"] = f"input/{video_id}/audio.%(ext)s"
                ydl_opts_audio["postprocessors"] = [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }
                ]
                with yt_dlp.YoutubeDL(ydl_opts_audio) as ydl_audio:
                    ydl_audio.download([url])

            return True
        except Exception as e:
            print(f"An error occurred: {str(e)}", file=sys.stderr)
            return False


def main():
    parser = argparse.ArgumentParser(
        description="Download YouTube videos as separate high-quality video and audio files."
    )
    parser.add_argument("id", help="ID of the YouTube video to download")
    parser.add_argument(
        "-k",
        "--keep-original",
        action="store_true",
        help="Keep the original video file after downloading (default: True)",
    )
    parser.add_argument(
        "-s",
        "--subs-langs",
        nargs="*",
        default=["en", "vi"],
        help="Subtitle languages to download (default: ['en', 'vi'])",
    )
    args = parser.parse_args()

    output_dir = "input"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    downloader = yt_downloader(keep_original=args.keep_original, subs_langs=args.subs_langs)
    success = downloader.download_video(f"https://youtube.com/watch?v={args.id}")

    if success:
        print("Video and audio downloaded successfully!")
    else:
        print("Failed to download video and audio.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
