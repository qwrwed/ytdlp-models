from __future__ import annotations

import json
from pathlib import Path

import yt_dlp
from yt_dlp_types.models import ExtractResult

URLS = [
    "https://www.youtube.com/watch?v=YE7VzlLtp-4",
    "https://www.youtube.com/watch?v=zaPI8MvL8pg",
    "https://www.youtube.com/watch?v=gVfLd0zydlo",
    "https://www.youtube.com/watch?v=FRhJzUSJbGI",
    "https://www.youtube.com/watch?v=Z4Vy8R84T1U",
    "https://www.youtube.com/watch?v=wsQiKKfKxug",
    "https://www.youtube.com/watch?v=zgdo7-RRjgo",
    "https://www.youtube.com/watch?v=qEJwOuvDf7I",
    "https://www.youtube.com/watch?v=1t24XAntNCY",
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "https://www.youtube.com/shorts/BGQWPY4IigY",
    "https://www.youtube.com/watch?v=i1Ko8UG-Tdo",
    "https://www.youtube.com/watch?v=18NGQq7p3LY",
    "https://www.youtube.com/watch?v=2NUZ8W2llS4",
    "https://www.youtube.com/watch?v=3dHQb2Nhma0",
    "https://www.youtube.com/watch?v=5KLPxDtMqe8",
    "https://www.youtube.com/watch?v=CHqg6qOn4no",
    "https://www.youtube.com/watch?v=FIl7x6_3R5Y",
    "https://www.youtube.com/watch?v=HsUATh_Nc2U",
    "https://www.youtube.com/watch?v=IB3lcPjvWLA",
    "https://www.youtube.com/watch?v=M4gD1WSo5mA",
    "https://www.youtube.com/watch?v=MeJVWBSsPAY",
    "https://www.youtube.com/watch?v=OtqTfy26tG0",
    "https://www.youtube.com/watch?v=YOelRv7fMxY",
    "https://www.youtube.com/watch?v=_A9KsMbWh4E",
    "https://www.youtube.com/watch?v=__2ABJjxzNo",
    "https://www.youtube.com/watch?v=_b-2C3KPAM0",
    "https://www.youtube.com/watch?v=a9LDPn-MO4I",
    "https://www.youtube.com/watch?v=brhfDfLdDZ8",
]

# genuine model failures, still need a fix
PENDING_URLS = []

# can't extract at all, nothing to fix here
UNAVAILABLE_URLS = [
    "https://www.youtube.com/watch?v=s7_qI6_mIXc",  # private video, extract_info raises DownloadError
    "https://www.youtube.com/watch?v=Cr381pDsSsA",  # removed for ToS violation, extract_info raises DownloadError
    "https://www.youtube.com/watch?v=nGC3D_FkCmg",  # age-gated, needs cookies, extract_info raises DownloadError
    "https://www.youtube.com/watch?v=sJL6WA-aGkQ",  # video unavailable, extract_info raises DownloadError
    "https://www.youtube.com/watch?v=WaOKSUlf4TM",  # age-gated, needs cookies, extract_info raises DownloadError
    "https://music.youtube.com/watch?v=XclachpHxis",  # video unavailable, extract_info raises DownloadError
    "https://www.youtube.com/watch?v=6SJNVb0GnPI",  # removed for policy violation, extract_info raises DownloadError
    "https://www.youtube.com/watch?v=BaW_jenozKc",  # video unavailable, extract_info raises DownloadError
    "https://www.youtube.com/watch?v=DJztXj2GPfl",  # video unavailable, extract_info raises DownloadError
    "https://www.youtube.com/watch?v=HtVdAasjOgU",  # age-gated, needs cookies, extract_info raises DownloadError
    "https://www.youtube.com/watch?v=Ms7iBXnlUO8",  # video unavailable, extract_info raises DownloadError
    "https://www.youtube.com/watch?v=Q39EVAstoRM",  # video unavailable, extract_info raises DownloadError
    "https://www.youtube.com/watch?v=SZJvDhaSDnc",  # age-gated, needs cookies, extract_info raises DownloadError
    "https://www.youtube.com/watch?v=Tq92D6wQ1mg",  # age-gated, needs cookies, extract_info raises DownloadError
]

ydl_opts: yt_dlp._YoutubeDLOptions = {
    "extract_flat": True,
}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    for url in URLS[-1:]:
        info_dict = ydl.extract_info(url, download=False)

        try:
            info_model = ExtractResult.validate_python(info_dict)
            print(f"OK: {url}")
        except Exception as e:
            print(f"FAILED: {url}\n{e}")

        info_json = json.dumps(ydl.sanitize_info(info_dict), indent=4)
        Path("out.json").write_text(info_json)
