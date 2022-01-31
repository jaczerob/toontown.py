import asyncio
import time
from abc import ABC, abstractmethod
from urllib.parse import quote
from typing import (
    Any,
    Dict,
    Union
)

import aiohttp
import requests

from . import config


Session = Union[aiohttp.ClientSession, requests.Session]

BASE: str = config.get('http', 'base')
BASE_HEADERS: Dict[str, Any] = config.get('http', 'base_headers')
LOGIN_HEADERS: Dict[str, Any] = config.get('http', 'login_headers')


class Route:
    def __init__(self, method: str, path: str, **parameters: Any) -> None:
        self.method = method
        self.path = path
        self.parameters = parameters
        self.url = BASE + path

    @property
    def headers(self) -> Dict[str, Any]:
        return LOGIN_HEADERS if self.path == '/login' else BASE_HEADERS


class BaseHTTPClient(ABC):
    @abstractmethod
    def __init__(self) -> None:
        self._session: Session = None

    @abstractmethod
    def connect(self) -> None: ...

    @abstractmethod
    def close(self) -> None: ...

    @abstractmethod
    def request(self, route: Route) -> Any: ...


class SyncHTTPClient(BaseHTTPClient):
    def __init__(self) -> None:
        self._session: requests.Session = None
        self._is_closed = True

    @property
    def is_closed(self) -> bool:
        return self._is_closed

    @is_closed.setter
    def is_closed(self, value: bool) -> None:
        self._is_closed = bool(value)

    def connect(self) -> None:
        self._session = requests.Session()
        self._is_closed = False

    def close(self) -> None:
        self._session.close()
        self._is_closed = True

    def request(self, route: Route) -> Any:
        if self.is_closed:
            raise Exception('HTTPClient not connected')

        method = route.method
        url = route.url
        headers = route.headers
        params = route.parameters

        for tries in range(5):
            try:
                with self._session.request(method, url, params=params, headers=headers) as response:
                    data = response.json()
                    status = response.status_code

                    if 300 > status >= 200:
                        return data

                    if status in {500, 502, 504}:
                        time.sleep(1 + tries * 2)
                        continue

                    response.raise_for_status()
            except OSError as e:
                if tries < 4 and e.errno in {54, 10054}:
                    time.sleep(1 + tries * 2)
                    continue


class AsyncHTTPClient(BaseHTTPClient):
    def __init__(self) -> None:
        self._session: aiohttp.ClientSession = None

    async def connect(self) -> None:
        self._session = aiohttp.ClientSession()

    async def close(self) -> None:
        self._session.close()

    async def request(self, route: Route) -> Any:
        if self._session.closed:
            raise Exception('HTTPClient not connected')

        method = route.method
        url = route.url
        headers = route.headers
        params = route.parameters

        for tries in range(5):
            try:
                async with self._session.request(method, url, params=params, headers=headers) as response:
                    data = await response.json()
                    status = response.status

                    if 300 > status >= 200:
                        return data

                    if status in {500, 502, 504}:
                        await asyncio.sleep(1 + tries * 2)
                        continue

                    response.raise_for_status()
            except OSError as e:
                if tries < 4 and e.errno in {54, 10054}:
                    await asyncio.sleep(1 + tries * 2)
                    continue


if __name__ == '__main__':
    AsyncHTTPClient()
