import argparse
import sys
import os
import yt_dlp


class yt_downloader:
    def __init__(
        self, output_format="bestvideo+bestaudio/best", keep_original=True, subs_langs=["en", "vi"]
    ):
        self.output_format = output_format
        self.keep_original = keep_original
        self.subs_langs = subs_langs
        self.ydl_opts = {
            "format": output_format,
            "keepvideo": keep_original,
            "outtmpl": "output/%(title)s/%(title)s.%(ext)s",
            "subtitleslangs": subs_langs,
            "writesubtitles": True,
            "subtitlesformat": "vtt",
        }

    def download_video(self, url):
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                ydl.download([url])
            return True
        except Exception as e:
            print(f"An error occurred: {str(e)}", file=sys.stderr)
            return False


def main():
    parser = argparse.ArgumentParser(
        description="Download YouTube videos as video files by default."
    )
    parser.add_argument("url", help="URL of the YouTube video to download")
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

    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    downloader = yt_downloader(keep_original=args.keep_original, subs_langs=args.subs_langs)
    success = downloader.download_video(args.url)

    if success:
        print("Video downloaded successfully!")
    else:
        print("Failed to download video.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
