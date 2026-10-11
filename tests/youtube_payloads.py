# synthetic yt-dlp info dicts with placeholder values, one builder per shape

from __future__ import annotations

from typing import Any

URL = 'https://example.com/url'

HTTP_HEADERS = {'User-Agent': 'agent', 'Accept': 'accept', 'Accept-Language': 'lang', 'Sec-Fetch-Mode': 'mode'}

THUMBNAIL = {'url': URL, 'height': 1, 'width': 1}


def without(payload: dict[str, Any], *keys: str) -> dict[str, Any]:
    return {key: value for key, value in payload.items() if key not in keys}


def video(**overrides: Any) -> dict[str, Any]:
    return {
        'id': 'video-id',
        'title': 'title',
        'thumbnails': [],
        'thumbnail': URL,
        'description': 'description',
        'channel_id': 'channel-id',
        'channel_url': URL,
        'view_count': 1,
        'average_rating': None,
        'age_limit': 0,
        'webpage_url': URL,
        'categories': [],
        'tags': [],
        'playable_in_embed': True,
        '_format_sort_fields': [],
        'automatic_captions': {},
        'subtitles': {},
        'comment_count': None,
        'chapters': None,
        'heatmap': None,
        'like_count': None,
        'channel': 'channel',
        'channel_follower_count': None,
        'uploader': 'uploader',
        'upload_date': '20000101',
        'timestamp': 1,
        'availability': 'public',
        'original_url': URL,
        'webpage_url_basename': 'watch',
        'webpage_url_domain': 'youtube.com',
        'extractor': 'youtube',
        'extractor_key': 'Youtube',
        'display_id': 'video-id',
        'fulltitle': 'title',
        'is_live': False,
        'requested_subtitles': None,
        '_has_drm': None,
        'epoch': 1,
        'format': 'format',
        'format_id': 'format-id',
        'ext': 'ext',
        'protocol': 'https',
        'language': None,
        'format_note': 'note',
        'tbr': 1.0,
        'width': 1,
        'height': 1,
        'resolution': '1x1',
        'dynamic_range': 'SDR',
        'vcodec': 'vcodec',
        'vbr': 1.0,
        'aspect_ratio': 1.0,
        # on demand
        'formats': [],
        'requested_formats': [],
        'duration': 1,
        'duration_string': '1',
        'filesize_approx': 1,
        'fps': 1,
        'acodec': 'acodec',
        'abr': 1.0,
        'asr': 1,
        'audio_channels': 1,
        # standalone
        'playlist': None,
        'playlist_index': None,
        # not live, no broadcast, no creators, with handle, unstretched
        'live_status': 'not_live',
        'was_live': False,
        'release_timestamp': None,
        'creators': None,
        'uploader_id': '@handle',
        'uploader_url': URL,
        'stretched_ratio': None,
        'media_type': 'video',
        'release_year': None,
    } | overrides


BROADCAST = {'release_timestamp': 1, 'release_date': '20000101', 'release_year': 2000}

CREATORS = {'creators': ['creator'], 'creator': 'creator'}

NO_HANDLE = {'uploader_id': None, 'uploader_url': None}


def livestream_video() -> dict[str, Any]:
    return video(live_status='was_live', was_live=True, media_type='livestream', **BROADCAST)


def live_now_video() -> dict[str, Any]:
    return without(video(), 'duration', 'duration_string') | {
        'live_status': 'is_live',
        'media_type': 'livestream',
        'filesize_approx': None,
        'fps': 1.0,
        'acodec': None,
        'abr': None,
        'asr': None,
        'audio_channels': None,
        'concurrent_view_count': 1,
        **BROADCAST,
    }


def premiere_video() -> dict[str, Any]:
    return video(**BROADCAST)


def premiere_collab_video() -> dict[str, Any]:
    return video(**BROADCAST, **CREATORS)


def collab_video() -> dict[str, Any]:
    return video(**CREATORS)


def location_video() -> dict[str, Any]:
    return video(location='location')


def stretched_video() -> dict[str, Any]:
    return video(stretched_ratio=1.0)


def no_handle_video() -> dict[str, Any]:
    return video(**NO_HANDLE)


def music_video() -> dict[str, Any]:
    return video(
        **CREATORS,
        **NO_HANDLE,
        release_date='20000101',
        release_year=2000,
        album='album',
        alt_title='alt title',
        artist='artist',
        artists=['artist'],
        track='track',
    )


IN_PLAYLIST = {
    '__last_playlist_index': 1,
    'n_entries': 1,
    'playlist': 'playlist',
    'playlist_autonumber': 1,
    'playlist_channel': None,
    'playlist_channel_id': None,
    'playlist_count': None,
    'playlist_id': 'playlist-id',
    'playlist_index': 1,
    'playlist_title': 'playlist title',
    'playlist_uploader': None,
    'playlist_uploader_id': None,
    'playlist_webpage_url': URL,
}


def in_playlist(standalone_video: dict[str, Any]) -> dict[str, Any]:
    return standalone_video | IN_PLAYLIST


def _playlist_core() -> dict[str, Any]:
    return {
        '_type': 'playlist',
        'id': 'playlist-id',
        'title': 'title',
        'entries': [],
        'epoch': 1,
        'extractor': 'youtube:tab',
        'extractor_key': 'YoutubeTab',
        'release_year': None,
        'webpage_url': URL,
    }


TOP_LEVEL = {'original_url': URL, 'webpage_url_basename': 'playlist', 'webpage_url_domain': 'youtube.com'}

NESTED = {'__x_forwarded_for_ip': None}

TRUNCATED = {'requested_entries': [1]}

OWNER_METADATA: dict[str, Any] = {
    'availability': None,
    'channel': None,
    'channel_follower_count': None,
    'channel_id': None,
    'channel_url': None,
    'description': None,
    'modified_date': None,
    'tags': [],
    'thumbnails': [],
    'uploader': None,
    'uploader_id': None,
    'uploader_url': None,
    'view_count': None,
}

VERIFIED_OWNER_METADATA = {
    'availability': 'public',
    'channel': 'channel',
    'channel_follower_count': 1,
    'channel_id': 'channel-id',
    'channel_is_verified': True,
    'channel_url': URL,
    'description': 'description',
    'modified_date': None,
    'tags': [],
    'thumbnails': [],
    'uploader': 'uploader',
    'uploader_id': '@handle',
    'uploader_url': URL,
    'view_count': None,
}


def playlist(*parts: dict[str, Any], playlist_count: int | None) -> dict[str, Any]:
    payload = _playlist_core()
    for part in parts:
        payload |= part
    return payload | {'playlist_count': playlist_count}


def url_reference(**fields: Any) -> dict[str, Any]:
    return {
        'ie_key': 'Youtube',
        '_type': 'url',
        'url': URL,
        'webpage_url': URL,
        'original_url': URL,
        'webpage_url_basename': 'watch',
        'webpage_url_domain': 'youtube.com',
        'extractor': 'youtube',
        'extractor_key': 'Youtube',
    } | fields


def entry(**fields: Any) -> dict[str, Any]:
    return {'__x_forwarded_for_ip': None, '_type': 'url', 'url': URL} | fields


def shorts_entry(**fields: Any) -> dict[str, Any]:
    return entry(id='video-id', ie_key='Youtube', thumbnails=[THUMBNAIL], **fields)


def lockup_entry(**fields: Any) -> dict[str, Any]:
    return entry(
        id='video-id',
        title='title',
        thumbnails=[THUMBNAIL],
        duration=1,
        view_count=1,
        timestamp=None,
        availability=None,
        creators=None,
    ) | fields


def video_renderer_entry(**fields: Any) -> dict[str, Any]:
    return entry(
        id='video-id',
        ie_key='Youtube',
        title='title',
        thumbnails=[THUMBNAIL],
        timestamp=None,
        release_timestamp=None,
        availability=None,
        channel='channel',
        channel_is_verified=None,
        uploader='uploader',
        uploader_id='@handle',
        uploader_url=URL,
    ) | fields
