from __future__ import annotations

from pydantic import TypeAdapter

from yt_dlp_types.url_reference import UrlReference
from yt_dlp_types.video_info import VideoInfo

ExtractResult = TypeAdapter(VideoInfo | UrlReference)
