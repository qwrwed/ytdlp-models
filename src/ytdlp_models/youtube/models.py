from __future__ import annotations

from typing import Annotated

from pydantic import Discriminator, Tag, TypeAdapter

from ytdlp_models.youtube.playlist_info import (
    BarePlaylistInfo,
    PlaylistInfo,
    TruncatedBarePlaylistInfo,
    TruncatedPlaylistInfo,
    TruncatedVerifiedPlaylistInfo,
    VerifiedPlaylistInfo,
    result_tag,
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

type ExtractResultType = Annotated[
    Annotated[
        VideoInfo
        | LivestreamVideoInfo
        | LiveNowVideoInfo
        | PremiereVideoInfo
        | PremiereCollabVideoInfo
        | CollabVideoInfo
        | LocationVideoInfo
        | StretchedVideoInfo
        | NoHandleVideoInfo
        | MusicVideoInfo,
        Tag('video'),
    ]
    | Annotated[PlaylistInfo, Tag('PlaylistInfo')]
    | Annotated[TruncatedPlaylistInfo, Tag('TruncatedPlaylistInfo')]
    | Annotated[VerifiedPlaylistInfo, Tag('VerifiedPlaylistInfo')]
    | Annotated[TruncatedVerifiedPlaylistInfo, Tag('TruncatedVerifiedPlaylistInfo')]
    | Annotated[BarePlaylistInfo, Tag('BarePlaylistInfo')]
    | Annotated[TruncatedBarePlaylistInfo, Tag('TruncatedBarePlaylistInfo')]
    | Annotated[UrlReference | TitledUrlReference | UrlReferenceWithoutId, Tag('url')],
    Discriminator(result_tag),
]

ExtractResult: TypeAdapter[ExtractResultType] = TypeAdapter(ExtractResultType)
