from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class UrlReference(BaseModel):
    model_config = ConfigDict(extra='forbid')

    ie_key: str
    id: str
    type_: Literal['url'] = Field(..., alias='_type')
    url: str
    webpage_url: str
    original_url: str
    webpage_url_basename: str
    webpage_url_domain: str
    extractor: str
    extractor_key: str
