from typing import Dict, Iterator, List, Tuple

from .base import BaseAPIModel


__all__ = ['Doodle', 'Playground', 'District', 'Doodles']


class Doodle:
    def __init__(self, *, dna, traits, cost) -> None:
        self.dna = dna
        self.rendition: str = f'https://rendition.toontownrewritten.com/render/{dna}/doodle/256x256.png'
        self.traits: List[str] = traits
        self.cost: int = cost


class Playground:
    def __init__(self, name, doodles) -> None:
        self.name: str = name
        self.doodles: List[Doodle] = [Doodle(**doodle) for doodle in doodles]


class District:
    def __init__(self, name, **playgrounds) -> None:
        self.name: str = name
        self._playgrounds: Dict[str, Playground] = {pg: Playground(pg, doodles) for pg, doodles in playgrounds.items()}

    def playgrounds(self) -> Iterator[Tuple[str, Playground]]:
        yield from self._playgrounds.items()

    def __getitem__(self, key: str) -> Playground:
        return self._playgrounds.__getitem__(key)


class Doodles(BaseAPIModel):
    def __init__(self, **payload) -> None:
        self._districts: Dict[str, District] = {district: District(district, **playgrounds) for district, playgrounds in payload.items()}

    def districts(self) -> Iterator[Tuple[str, District]]:
        yield from self._districts.items()

    def __getitem__(self, key: str) -> District:
        return self._districts.__getitem__(key)