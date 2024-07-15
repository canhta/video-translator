import pytest
from unittest.mock import patch, MagicMock
from yt_downloader import yt_downloader


@pytest.fixture
def downloader():
    return yt_downloader()


def test_youtube_downloader_initialization(downloader):
    assert isinstance(downloader, yt_downloader)
    assert downloader.ydl_opts["format"] == "bestaudio/best"
    assert downloader.ydl_opts["postprocessors"][0]["preferredcodec"] == "mp3"
    assert downloader.ydl_opts["postprocessors"][0]["preferredquality"] == "192"


@patch("yt_dlp.YoutubeDL")
def test_download_video_success(mock_ytdl, downloader):
    mock_ytdl_instance = MagicMock()
    mock_ytdl.return_value.__enter__.return_value = mock_ytdl_instance

    result = downloader.download_video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

    assert result is True
    mock_ytdl_instance.download.assert_called_once_with(
        ["https://www.youtube.com/watch?v=dQw4w9WgXcQ"]
    )


@patch("yt_dlp.YoutubeDL")
def test_download_video_failure(mock_ytdl, downloader):
    mock_ytdl_instance = MagicMock()
    mock_ytdl.return_value.__enter__.return_value = mock_ytdl_instance
    mock_ytdl_instance.download.side_effect = Exception("Download failed")

    result = downloader.download_video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

    assert result is False


if __name__ == "__main__":
    pytest.main()
