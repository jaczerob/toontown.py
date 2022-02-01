from datetime import datetime
from typing import Iterator, List, Tuple

from .base import BaseAPIModel


__all__ = ['Population']


class Population(BaseAPIModel):
    """"Wrapper class for /population response

    Attributes
    ----------
    total : int
        the total population of Toontown Rewritten

    last_updated : datetime
        the time of the last population update
    """

    def __init__(self, **payload) -> None:
        self.total: int = payload.get('totalPopulation')
        self.last_updated: datetime = datetime.fromtimestamp(payload.get('lastUpdated'))
        self._population_by_district: dict = payload.get('populationByDistrict')

    def iteritems(self) -> Iterator[Tuple[str, int]]:
        """Return an iterator of the districts and their population"""
        yield from self._population_by_district.items()

    def keys(self) -> List[str]:
        """Returns a list of the district names"""
        return list(self._population_by_district.keys())

    def values(self) -> List[str]:
        """Returns a list of the district populations"""
        return list(self._population_by_district.values())

    def __getitem__(self, district: str) -> int:
        """Returns the population of the given district"""
        return self._population_by_district.__getitem__(district)
