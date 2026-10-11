# runs yt-dlp against YouTube, so it's deselected by default; run with `pytest -m network`

from __future__ import annotations

import tomllib
from collections.abc import Iterator
from pathlib import Path

import pytest
import yt_dlp

from ytdlp_models.youtube.models import ExtractResult

URL_LISTS = tomllib.loads((Path(__file__).parent / 'youtube_urls.toml').read_text())

OPTS: yt_dlp._YoutubeDLOptions = {
    'quiet': True,
    'no_warnings': True,
    # caps playlist entries; yt-dlp adds requested_entries whenever this cuts some off
    'playlistend': 3,
}


@pytest.fixture(scope='module')
def flat_ydl() -> Iterator[yt_dlp.YoutubeDL]:
    with yt_dlp.YoutubeDL({**OPTS, 'extract_flat': True}) as ydl:
        yield ydl


@pytest.fixture(scope='module')
def full_ydl() -> Iterator[yt_dlp.YoutubeDL]:
    with yt_dlp.YoutubeDL({**OPTS, 'extract_flat': False}) as ydl:
        yield ydl


@pytest.mark.network
class A_live_extract_result:
    @pytest.mark.parametrize('url', URL_LISTS['urls'] + URL_LISTS['flat_only_urls'])
    def matches_a_model_with_flat_extraction(self, flat_ydl: yt_dlp.YoutubeDL, url: str) -> None:
        info_dict = flat_ydl.extract_info(url, download=False)

        ExtractResult.validate_python(info_dict)

    @pytest.mark.parametrize('url', URL_LISTS['urls'])
    def matches_a_model_with_full_extraction(self, full_ydl: yt_dlp.YoutubeDL, url: str) -> None:
        info_dict = full_ydl.extract_info(url, download=False)

        ExtractResult.validate_python(info_dict)
