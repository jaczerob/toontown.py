from datetime import datetime
from typing import Iterator, Tuple

from .base import BaseAPIModel


__all__ = ['Population']


class Population(BaseAPIModel):
    def __init__(self, **payload) -> None:
        self.total = payload.get('totalPopulation')
        self.last_updated = datetime.fromtimestamp(payload.get('lastUpdated'))
        self._population_by_district: dict = payload.get('populationByDistrict')

    def districts(self) -> Iterator[Tuple[str, int]]:
        yield from self._population_by_district.items()

    def __getitem__(self, key: str) -> int:
        return self._population_by_district.__getitem__(key)
