from __future__ import annotations

from pydantic import TypeAdapter

from ytdlp_models.youtube.playlist_info import (
    BarePlaylistInfo,
    PlaylistInfo,
    TruncatedBarePlaylistInfo,
    TruncatedPlaylistInfo,
    TruncatedVerifiedPlaylistInfo,
    VerifiedPlaylistInfo,
)
from ytdlp_models.youtube.url_reference import TitledUrlReference, UrlReference, UrlReferenceWithoutId
from ytdlp_models.youtube.video_info import (
    CollabVideoInfo,
    LiveNowVideoInfo,
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
    | LiveNowVideoInfo
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
    | BarePlaylistInfo
    | TruncatedBarePlaylistInfo
    | UrlReference
    | TitledUrlReference
    | UrlReferenceWithoutId
)

ExtractResult: TypeAdapter[ExtractResultType] = TypeAdapter(ExtractResultType)
