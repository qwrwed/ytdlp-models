from __future__ import annotations

import json
import tomllib
from pathlib import Path

import yt_dlp
from ytdlp_models.youtube import ExtractResult

URLS: list[str] = tomllib.loads((Path(__file__).parent.parent / "tests" / "youtube_urls.toml").read_text())["urls"]

ydl_opts: yt_dlp._YoutubeDLOptions = {
    "extract_flat": True,
    # caps playlist entries; yt-dlp adds requested_entries whenever this cuts some off
    "playlistend": 3,
}
# without extract_flat, redirects are followed to the target video instead of returning a url stub
no_flat_opts: yt_dlp._YoutubeDLOptions = {**ydl_opts, "extract_flat": False}

for opts, out_path in ((ydl_opts, "out.json"), (no_flat_opts, "out_no_flat.json")):
    with yt_dlp.YoutubeDL(opts) as ydl:
        for url in URLS[-1:]:
            info_dict = ydl.extract_info(url, download=False)

            try:
                info_model = ExtractResult.validate_python(info_dict)
                print(f"OK (extract_flat={opts['extract_flat']}): {url}")
            except Exception as e:
                print(f"FAILED (extract_flat={opts['extract_flat']}): {url}\n{e}")

            info_json = json.dumps(ydl.sanitize_info(info_dict), indent=4)
            Path(out_path).write_text(info_json)
