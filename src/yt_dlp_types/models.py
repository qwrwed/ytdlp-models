from __future__ import annotations

from pydantic import TypeAdapter

from yt_dlp_types.playlist_info import (
    PlaylistInfo,
    TruncatedBarePlaylistInfo,
    TruncatedPlaylistInfo,
    TruncatedVerifiedPlaylistInfo,
    VerifiedPlaylistInfo,
)
from yt_dlp_types.url_reference import TitledUrlReference, UrlReference, UrlReferenceWithoutId
from yt_dlp_types.video_info import (
    CollabVideoInfo,
    LivestreamVideoInfo,
    LocationVideoInfo,
    MusicVideoInfo,
    NoHandleVideoInfo,
    PremiereCollabVideoInfo,
    PremiereVideoInfo,
    StretchedVideoInfo,
    VideoInfo,
)

type ExtractResultType = (
    VideoInfo
    | LivestreamVideoInfo
    | PremiereVideoInfo
    | PremiereCollabVideoInfo
    | CollabVideoInfo
    | LocationVideoInfo
    | StretchedVideoInfo
    | NoHandleVideoInfo
    | MusicVideoInfo
    | PlaylistInfo
    | TruncatedPlaylistInfo
    | VerifiedPlaylistInfo
    | TruncatedVerifiedPlaylistInfo
    | TruncatedBarePlaylistInfo
    | UrlReference
    | TitledUrlReference
    | UrlReferenceWithoutId
)

ExtractResult: TypeAdapter[ExtractResultType] = TypeAdapter(ExtractResultType)
