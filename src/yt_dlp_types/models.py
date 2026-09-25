from __future__ import annotations

from pydantic import TypeAdapter

from yt_dlp_types.url_reference import UrlReference
from yt_dlp_types.video_info import (
    CollabVideoInfo,
    LivestreamVideoInfo,
    LocationVideoInfo,
    MusicVideoInfo,
    PremiereCollabVideoInfo,
    StretchedVideoInfo,
    VideoInfo,
)

ExtractResult: TypeAdapter[
    VideoInfo
    | LivestreamVideoInfo
    | PremiereCollabVideoInfo
    | CollabVideoInfo
    | LocationVideoInfo
    | StretchedVideoInfo
    | MusicVideoInfo
    | UrlReference
] = TypeAdapter(
    VideoInfo
    | LivestreamVideoInfo
    | PremiereCollabVideoInfo
    | CollabVideoInfo
    | LocationVideoInfo
    | StretchedVideoInfo
    | MusicVideoInfo
    | UrlReference
)
