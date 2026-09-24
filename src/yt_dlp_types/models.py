from __future__ import annotations

from pydantic import TypeAdapter

from yt_dlp_types.url_reference import UrlReference
from yt_dlp_types.video_info import LivestreamVideoInfo, MusicVideoInfo, VideoInfo

ExtractResult: TypeAdapter[VideoInfo | LivestreamVideoInfo | MusicVideoInfo | UrlReference] = TypeAdapter(
    VideoInfo | LivestreamVideoInfo | MusicVideoInfo | UrlReference
)
