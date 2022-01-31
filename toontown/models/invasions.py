from datetime import datetime
from typing import List

from .base import BaseAPIModel


__all__ = ['Invasion', 'Invasions']


class Invasion:
    def __init__(self, district, **payload) -> None:
        self.district: str = district
        self.as_of = datetime.fromtimestamp(payload.pop('asOf'))
        self.type: str = payload.pop('type')
        self.progress: str = payload.pop('progress')

    @property
    def is_mega_invasion(self) -> bool:
        cogs_defeated, invasion_amount = tuple(map(int, self.progress.split('/')))
        return invasion_amount == 1000000


class Invasions(BaseAPIModel):
    def __init__(self, **payload) -> None:
        self.last_updated = datetime.fromtimestamp(payload.pop('lastUpdated'))
        
        invasions = payload.pop('invasions')
        self.invasions: List[Invasion] = [Invasion(district, **props) for district, props in invasions.items()]