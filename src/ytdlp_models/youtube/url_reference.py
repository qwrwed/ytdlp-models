from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class _UrlReferenceBase(BaseModel):
    model_config = ConfigDict(extra='forbid')

    ie_key: Literal['Youtube', 'YoutubeTab']
    type_: Literal['url'] = Field(..., alias='_type')
    url: str
    webpage_url: str
    original_url: str
    webpage_url_basename: str
    webpage_url_domain: str
    extractor: str
    extractor_key: str


class UrlReference(_UrlReferenceBase):
    id: str


class TitledUrlReference(UrlReference):
    title: str


class UrlReferenceWithoutId(_UrlReferenceBase):
    pass
