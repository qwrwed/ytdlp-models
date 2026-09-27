# channel URLs, channel tabs, playlists, feeds and searches all come back as _type 'playlist'

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from yt_dlp_types.video_info import SizedThumbnail, Thumbnail


class SizedThumbnailWithoutPreference(BaseModel):
    model_config = ConfigDict(extra='forbid')

    url: str
    id: str
    height: int
    width: int
    resolution: str


class EntryThumbnail(BaseModel):
    model_config = ConfigDict(extra='forbid')

    url: str
    height: int
    width: int


# entries are _type 'url' stubs when extract_flat is on
class _EntryBase(BaseModel):
    model_config = ConfigDict(extra='forbid')

    x_forwarded_for_ip__: None = Field(..., alias='__x_forwarded_for_ip')
    type_: Literal['url'] = Field(..., alias='_type')
    url: str


class LinkEntry(_EntryBase):
    title: str


class MinimalVideoEntry(_EntryBase):
    id: str
    ie_key: Literal['Youtube']


class MinimalPlaylistEntry(_EntryBase):
    id: str
    ie_key: Literal['YoutubeTab']
    title: str


class _ShortsEntryBase(_EntryBase):
    id: str
    ie_key: Literal['Youtube']
    thumbnails: list[EntryThumbnail]
    view_count: int


class ShortsEntry(_ShortsEntryBase):
    title: str


class UntitledShortsEntry(_ShortsEntryBase):
    pass


# built by yt-dlp's _extract_lockup_view_model
class _LockupEntryBase(_EntryBase):
    id: str
    title: str
    thumbnails: list[EntryThumbnail]
    duration: int | None
    view_count: int | None
    timestamp: None
    availability: Literal['subscriber_only'] | None
    creators: None


class LockupEntry(_LockupEntryBase):
    ie_key: Literal['Youtube', 'YoutubeTab']
    live_status: Literal['is_upcoming'] | None
    channel: str
    channel_id: str
    channel_url: str
    uploader: str
    uploader_id: str
    uploader_url: str


# listed on the owning channel's own tab, so no owner fields are filled in
class LockupEntryWithoutOwner(_LockupEntryBase):
    ie_key: Literal['Youtube']
    live_status: Literal['is_upcoming', 'was_live'] | None
    channel_url: None
    uploader_url: None


class LockupEntryWithOwnerName(_LockupEntryBase):
    ie_key: Literal['YoutubeTab']
    live_status: None
    duration: None
    view_count: None
    availability: None
    channel: str
    channel_url: None
    uploader: str
    uploader_url: None


# built by yt-dlp's _extract_video
class _VideoRendererEntryBase(_EntryBase):
    id: str
    ie_key: Literal['Youtube']
    title: str
    thumbnails: list[EntryThumbnail]
    timestamp: None
    release_timestamp: None
    availability: None
    channel: str
    channel_is_verified: Literal[True] | None
    uploader: str
    uploader_id: str | None
    uploader_url: str | None


class VideoRendererEntry(_VideoRendererEntryBase):
    description: str | None
    duration: int
    live_status: Literal['was_live'] | None
    view_count: int | None
    channel_id: str | None
    channel_url: str | None


# live entries report concurrent_view_count in place of view_count
class LiveVideoRendererEntry(_VideoRendererEntryBase):
    description: None
    duration: None
    live_status: Literal['is_live']
    concurrent_view_count: int
    channel_id: str
    channel_url: str


class _PlaylistCore(BaseModel):
    model_config = ConfigDict(extra='forbid')

    type_: Literal['playlist'] = Field(..., alias='_type')
    id: str
    title: str
    entries: list[PlaylistEntry]
    epoch: int
    extractor: Literal['youtube:tab']
    extractor_key: Literal['YoutubeTab']
    release_year: None
    webpage_url: str


class _TopLevel(BaseModel):
    original_url: str
    webpage_url_basename: str
    webpage_url_domain: Literal['youtube.com', 'music.youtube.com']


# a channel tab nested inside a channel's playlist
class _Nested(BaseModel):
    x_forwarded_for_ip__: None = Field(..., alias='__x_forwarded_for_ip')


# present when playlistend/playlist_items cut entries off
class _Truncated(BaseModel):
    requested_entries: list[int]


class _OwnerMetadata(BaseModel):
    availability: Literal['public', 'unlisted'] | None
    channel: str | None
    channel_follower_count: int | None
    channel_id: str | None
    channel_url: str | None
    description: str | None
    modified_date: str | None
    tags: list[str]
    thumbnails: list[Thumbnail | SizedThumbnail | SizedThumbnailWithoutPreference]
    uploader: str | None
    uploader_id: str | None
    uploader_url: str | None
    view_count: int | None


class _VerifiedOwnerMetadata(BaseModel):
    availability: Literal['public']
    channel: str
    channel_follower_count: int
    channel_id: str
    channel_is_verified: Literal[True]
    channel_url: str
    description: str
    modified_date: None
    tags: list[str]
    thumbnails: list[Thumbnail | SizedThumbnail | SizedThumbnailWithoutPreference]
    uploader: str
    uploader_id: str
    uploader_url: str
    view_count: None


class PlaylistInfo(_TopLevel, _OwnerMetadata, _PlaylistCore):
    playlist_count: int


class TruncatedPlaylistInfo(_TopLevel, _OwnerMetadata, _Truncated, _PlaylistCore):
    playlist_count: int | None


class VerifiedPlaylistInfo(_TopLevel, _VerifiedOwnerMetadata, _PlaylistCore):
    playlist_count: int


class TruncatedVerifiedPlaylistInfo(_TopLevel, _VerifiedOwnerMetadata, _Truncated, _PlaylistCore):
    playlist_count: None


# no owner metadata at all
class TruncatedBarePlaylistInfo(_TopLevel, _Truncated, _PlaylistCore):
    playlist_count: None


class TabPlaylistEntry(_Nested, _VerifiedOwnerMetadata, _PlaylistCore):
    playlist_count: int


class TruncatedTabPlaylistEntry(_Nested, _VerifiedOwnerMetadata, _Truncated, _PlaylistCore):
    playlist_count: None


type PlaylistEntry = (
    LinkEntry
    | MinimalVideoEntry
    | MinimalPlaylistEntry
    | ShortsEntry
    | UntitledShortsEntry
    | LockupEntry
    | LockupEntryWithoutOwner
    | LockupEntryWithOwnerName
    | VideoRendererEntry
    | LiveVideoRendererEntry
    | TabPlaylistEntry
    | TruncatedTabPlaylistEntry
)
