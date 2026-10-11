from __future__ import annotations

from typing import Any

import pytest
from pydantic import TypeAdapter, ValidationError

import youtube_payloads as payloads
from ytdlp_models.youtube import playlist_info, url_reference, video_info
from ytdlp_models.youtube.models import ExtractResult

PlaylistEntry: TypeAdapter[playlist_info.PlaylistEntry] = TypeAdapter(playlist_info.PlaylistEntry)


class A_video_result:
    @pytest.mark.parametrize('media_type', ['video', 'short'])
    def becomes_VideoInfo_when_on_demand_from_a_channel_with_a_handle(self, media_type: str) -> None:
        payload = payloads.video(media_type=media_type)

        result = ExtractResult.validate_python(payload)

        assert type(result) is video_info.VideoInfo

    def becomes_NoHandleVideoInfo_when_its_channel_has_no_handle(self) -> None:
        payload = payloads.no_handle_video()

        result = ExtractResult.validate_python(payload)

        assert type(result) is video_info.NoHandleVideoInfo

    def becomes_LivestreamVideoInfo_when_it_was_live(self) -> None:
        payload = payloads.livestream_video()

        result = ExtractResult.validate_python(payload)

        assert type(result) is video_info.LivestreamVideoInfo

    def becomes_LiveNowVideoInfo_when_it_is_live(self) -> None:
        payload = payloads.live_now_video()

        result = ExtractResult.validate_python(payload)

        assert type(result) is video_info.LiveNowVideoInfo

    def becomes_PremiereVideoInfo_when_it_has_a_release_time_but_was_never_live(self) -> None:
        payload = payloads.premiere_video()

        result = ExtractResult.validate_python(payload)

        assert type(result) is video_info.PremiereVideoInfo

    def becomes_PremiereCollabVideoInfo_when_a_premiere_has_creators(self) -> None:
        payload = payloads.premiere_collab_video()

        result = ExtractResult.validate_python(payload)

        assert type(result) is video_info.PremiereCollabVideoInfo

    def becomes_CollabVideoInfo_when_it_has_creators_and_no_release_time(self) -> None:
        payload = payloads.collab_video()

        result = ExtractResult.validate_python(payload)

        assert type(result) is video_info.CollabVideoInfo

    def becomes_LocationVideoInfo_when_it_has_a_location(self) -> None:
        payload = payloads.location_video()

        result = ExtractResult.validate_python(payload)

        assert type(result) is video_info.LocationVideoInfo

    def becomes_StretchedVideoInfo_when_it_has_a_stretched_ratio(self) -> None:
        payload = payloads.stretched_video()

        result = ExtractResult.validate_python(payload)

        assert type(result) is video_info.StretchedVideoInfo

    def becomes_MusicVideoInfo_when_it_has_music_credits(self) -> None:
        payload = payloads.music_video()

        result = ExtractResult.validate_python(payload)

        assert type(result) is video_info.MusicVideoInfo


class A_video_result_is_rejected:
    def when_it_has_an_unknown_key(self) -> None:
        payload = payloads.video(unknown_key='value')

        with pytest.raises(ValidationError):
            ExtractResult.validate_python(payload)


class A_playlist_result:
    @pytest.mark.parametrize('playlist_count', [0, 1, 1000])
    def becomes_PlaylistInfo_when_it_has_owner_metadata_and_all_entries(self, playlist_count: int) -> None:
        payload = payloads.playlist(payloads.TOP_LEVEL, payloads.OWNER_METADATA, playlist_count=playlist_count)

        result = ExtractResult.validate_python(payload)

        assert type(result) is playlist_info.PlaylistInfo

    @pytest.mark.parametrize('playlist_count', [None, 1])
    def becomes_TruncatedPlaylistInfo_when_it_has_owner_metadata_and_entries_cut_off(
        self, playlist_count: int | None
    ) -> None:
        payload = payloads.playlist(
            payloads.TOP_LEVEL, payloads.OWNER_METADATA, payloads.TRUNCATED, playlist_count=playlist_count
        )

        result = ExtractResult.validate_python(payload)

        assert type(result) is playlist_info.TruncatedPlaylistInfo

    def becomes_VerifiedPlaylistInfo_when_its_owner_is_verified(self) -> None:
        payload = payloads.playlist(payloads.TOP_LEVEL, payloads.VERIFIED_OWNER_METADATA, playlist_count=1)

        result = ExtractResult.validate_python(payload)

        assert type(result) is playlist_info.VerifiedPlaylistInfo

    @pytest.mark.parametrize('playlist_count', [None, 1])
    def becomes_TruncatedVerifiedPlaylistInfo_when_its_owner_is_verified_and_entries_are_cut_off(
        self, playlist_count: int | None
    ) -> None:
        payload = payloads.playlist(
            payloads.TOP_LEVEL, payloads.VERIFIED_OWNER_METADATA, payloads.TRUNCATED, playlist_count=playlist_count
        )

        result = ExtractResult.validate_python(payload)

        assert type(result) is playlist_info.TruncatedVerifiedPlaylistInfo

    def becomes_BarePlaylistInfo_when_it_has_no_owner_metadata(self) -> None:
        payload = payloads.playlist(payloads.TOP_LEVEL, playlist_count=1)

        result = ExtractResult.validate_python(payload)

        assert type(result) is playlist_info.BarePlaylistInfo

    def becomes_TruncatedBarePlaylistInfo_when_it_has_no_owner_metadata_and_entries_are_cut_off(self) -> None:
        payload = payloads.playlist(payloads.TOP_LEVEL, payloads.TRUNCATED, playlist_count=None)

        result = ExtractResult.validate_python(payload)

        assert type(result) is playlist_info.TruncatedBarePlaylistInfo


class A_url_result:
    @pytest.mark.parametrize('ie_key', ['Youtube', 'YoutubeTab'])
    def becomes_UrlReference_when_it_has_an_id(self, ie_key: str) -> None:
        payload = payloads.url_reference(ie_key=ie_key, id='video-id')

        result = ExtractResult.validate_python(payload)

        assert type(result) is url_reference.UrlReference

    def becomes_TitledUrlReference_when_it_has_an_id_and_a_title(self) -> None:
        payload = payloads.url_reference(id='video-id', title='title')

        result = ExtractResult.validate_python(payload)

        assert type(result) is url_reference.TitledUrlReference

    def becomes_UrlReferenceWithoutId_when_it_has_no_id(self) -> None:
        payload = payloads.url_reference()

        result = ExtractResult.validate_python(payload)

        assert type(result) is url_reference.UrlReferenceWithoutId


class A_playlist_entry:
    @pytest.mark.parametrize(
        ('payload', 'expected'),
        [
            (payloads.entry(title='title'), playlist_info.LinkEntry),
            (payloads.entry(id='video-id', ie_key='Youtube'), playlist_info.MinimalVideoEntry),
            (payloads.entry(id='playlist-id', ie_key='YoutubeTab', title='title'), playlist_info.MinimalPlaylistEntry),
            (payloads.shorts_entry(view_count=1, title='title'), playlist_info.ShortsEntry),
            (payloads.shorts_entry(view_count=1), playlist_info.UntitledShortsEntry),
            (payloads.shorts_entry(title='title'), playlist_info.ShortsEntryWithoutViewCount),
        ],
        ids=lambda value: value.__name__ if isinstance(value, type) else '',
    )
    def from_flat_extraction_becomes_the_stub_class_matching_its_fields(self, payload: dict[str, Any], expected: type) -> None:
        result = PlaylistEntry.validate_python(payload)

        assert type(result) is expected

    @pytest.mark.parametrize(
        ('payload', 'expected'),
        [
            (
                payloads.lockup_entry(
                    ie_key='Youtube',
                    live_status=None,
                    channel='channel',
                    channel_id='channel-id',
                    channel_url=payloads.URL,
                    uploader='uploader',
                    uploader_id='@handle',
                    uploader_url=payloads.URL,
                ),
                playlist_info.LockupEntry,
            ),
            (
                payloads.lockup_entry(
                    ie_key='Youtube',
                    live_status=None,
                    channel='channel',
                    channel_id='channel-id',
                    channel_url=payloads.URL,
                    uploader='uploader',
                    uploader_url=None,
                ),
                playlist_info.LockupEntryWithoutHandle,
            ),
            (
                payloads.lockup_entry(
                    ie_key='Youtube',
                    live_status=None,
                    creators=['creator'],
                    channel='channel',
                    channel_url=None,
                    uploader='uploader',
                    uploader_url=None,
                ),
                playlist_info.LockupEntryWithCollaborators,
            ),
            (
                payloads.lockup_entry(ie_key='Youtube', live_status='was_live', channel_url=None, uploader_url=None),
                playlist_info.LockupEntryWithoutOwner,
            ),
            (
                payloads.lockup_entry(
                    ie_key='YoutubeTab',
                    live_status=None,
                    duration=None,
                    view_count=None,
                    channel='channel',
                    channel_url=None,
                    uploader='uploader',
                    uploader_url=None,
                ),
                playlist_info.LockupEntryWithOwnerName,
            ),
            (
                payloads.lockup_entry(
                    ie_key='Youtube',
                    title=None,
                    duration=None,
                    view_count=None,
                    live_status=None,
                    channel_url=None,
                    uploader_url=None,
                ),
                playlist_info.UntitledLockupEntry,
            ),
        ],
        ids=lambda value: value.__name__ if isinstance(value, type) else '',
    )
    def from_a_lockup_becomes_the_lockup_class_matching_its_owner_fields(self, payload: dict[str, Any], expected: type) -> None:
        result = PlaylistEntry.validate_python(payload)

        assert type(result) is expected

    @pytest.mark.parametrize(
        ('payload', 'expected'),
        [
            (
                payloads.video_renderer_entry(
                    description='description',
                    duration=1,
                    live_status=None,
                    view_count=1,
                    channel_id='channel-id',
                    channel_url=payloads.URL,
                ),
                playlist_info.VideoRendererEntry,
            ),
            (
                payloads.video_renderer_entry(
                    description=None,
                    duration=None,
                    live_status='is_live',
                    concurrent_view_count=1,
                    channel_id='channel-id',
                    channel_url=payloads.URL,
                ),
                playlist_info.LiveVideoRendererEntry,
            ),
        ],
        ids=lambda value: value.__name__ if isinstance(value, type) else '',
    )
    def from_a_video_renderer_becomes_the_renderer_class_matching_its_live_status(
        self, payload: dict[str, Any], expected: type
    ) -> None:
        result = PlaylistEntry.validate_python(payload)

        assert type(result) is expected

    @pytest.mark.parametrize('title', ['[Private video]', '[Deleted video]'])
    def becomes_UnavailableVideoRendererEntry_when_it_is_a_private_or_deleted_placeholder(self, title: str) -> None:
        payload = payloads.entry(
            id='video-id',
            ie_key='Youtube',
            title=title,
            thumbnails=[payloads.THUMBNAIL],
            **dict.fromkeys(
                [
                    'description',
                    'duration',
                    'view_count',
                    'timestamp',
                    'release_timestamp',
                    'availability',
                    'live_status',
                    'channel',
                    'channel_id',
                    'channel_url',
                    'channel_is_verified',
                    'uploader',
                    'uploader_id',
                    'uploader_url',
                ]
            ),
        )

        result = PlaylistEntry.validate_python(payload)

        assert type(result) is playlist_info.UnavailableVideoRendererEntry

    @pytest.mark.parametrize(
        ('standalone_video', 'expected'),
        [
            (payloads.video(), video_info.VideoInfoInPlaylist),
            (payloads.livestream_video(), video_info.LivestreamVideoInfoInPlaylist),
            (payloads.live_now_video(), video_info.LiveNowVideoInfoInPlaylist),
            (payloads.premiere_video(), video_info.PremiereVideoInfoInPlaylist),
            (payloads.collab_video(), video_info.CollabVideoInfoInPlaylist),
            (payloads.location_video(), video_info.LocationVideoInfoInPlaylist),
            (payloads.music_video(), video_info.MusicVideoInfoInPlaylist),
        ],
        ids=lambda value: value.__name__ if isinstance(value, type) else '',
    )
    def from_full_extraction_becomes_the_in_playlist_video_class_of_its_shape(
        self, standalone_video: dict[str, Any], expected: type
    ) -> None:
        payload = payloads.in_playlist(standalone_video)

        result = PlaylistEntry.validate_python(payload)

        assert type(result) is expected

    @pytest.mark.parametrize(
        ('parts', 'playlist_count', 'expected'),
        [
            ((payloads.TOP_LEVEL, payloads.OWNER_METADATA), 1, playlist_info.PlaylistInfo),
            ((payloads.TOP_LEVEL, payloads.OWNER_METADATA, payloads.TRUNCATED), None, playlist_info.TruncatedPlaylistInfo),
            ((payloads.TOP_LEVEL, payloads.VERIFIED_OWNER_METADATA), 1, playlist_info.VerifiedPlaylistInfo),
            (
                (payloads.TOP_LEVEL, payloads.VERIFIED_OWNER_METADATA, payloads.TRUNCATED),
                None,
                playlist_info.TruncatedVerifiedPlaylistInfo,
            ),
            ((payloads.TOP_LEVEL,), 1, playlist_info.BarePlaylistInfo),
            ((payloads.TOP_LEVEL, payloads.TRUNCATED), None, playlist_info.TruncatedBarePlaylistInfo),
        ],
        ids=lambda value: value.__name__ if isinstance(value, type) else '',
    )
    def from_full_extraction_becomes_the_playlist_class_it_would_be_at_top_level(
        self, parts: tuple[dict[str, Any], ...], playlist_count: int | None, expected: type
    ) -> None:
        payload = payloads.playlist(*parts, playlist_count=playlist_count)

        result = PlaylistEntry.validate_python(payload)

        assert type(result) is expected

    def becomes_TabPlaylistEntry_when_it_is_a_channel_tab_with_all_entries(self) -> None:
        payload = payloads.playlist(payloads.NESTED, payloads.VERIFIED_OWNER_METADATA, playlist_count=1)

        result = PlaylistEntry.validate_python(payload)

        assert type(result) is playlist_info.TabPlaylistEntry

    def becomes_TruncatedTabPlaylistEntry_when_it_is_a_channel_tab_with_entries_cut_off(self) -> None:
        payload = payloads.playlist(
            payloads.NESTED, payloads.VERIFIED_OWNER_METADATA, payloads.TRUNCATED, playlist_count=None
        )

        result = PlaylistEntry.validate_python(payload)

        assert type(result) is playlist_info.TruncatedTabPlaylistEntry
