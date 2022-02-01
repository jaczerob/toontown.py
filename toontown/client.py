from abc import abstractmethod, ABC
from typing import Optional

from .models import *
from .httpclient import BaseHTTPClient, SyncHTTPClient, AsyncHTTPClient, Route


class BaseToontownClient(ABC):
    @abstractmethod
    def __init__(self, httpclient: BaseHTTPClient) -> None:
        self.http = httpclient

    @abstractmethod
    def connect(self) -> None: ...

    @abstractmethod
    def close(self) -> None: ...

    @abstractmethod
    def doodles(self) -> Doodles: ...

    @abstractmethod
    def field_offices(self) -> FieldOffices: ...

    @abstractmethod
    def invasions(self) -> Invasions: ...

    @abstractmethod
    def login(
        self, 
        *, 
        username: Optional[str] = None, 
        password: Optional[str] = None,
        response_token: Optional[str] = None,
        queue_token: Optional[str] = None,
    ) -> Login: ...

    @abstractmethod
    def population(self) -> Population: ...

    @abstractmethod
    def silly_meter(self) -> None: ...


class SyncToontownClient(BaseToontownClient):
    """Synchronous client to interact with the Toontown Rewritten API"""

    def __init__(self) -> None:
        super().__init__(SyncHTTPClient())

    def connect(self) -> None:
        self.http.connect()

    def close(self) -> None:
        self.http.close()

    def doodles(self) -> Doodles:
        data = self.http.request(Route(
            'GET',
            '/doodles'
        ))

        return Doodles(**data)

    def field_offices(self) -> FieldOffices:
        data = self.http.request(Route(
            'GET',
            '/fieldoffices'
        ))

        return FieldOffices(**data)

    def invasions(self) -> Invasions:
        data = self.http.request(Route(
            'GET',
            '/invasions'
        ))

        return Invasions(**data)

    def login(
        self, 
        *, 
        username: Optional[str] = None, 
        password: Optional[str] = None,
        response_token: Optional[str] = None,
        queue_token: Optional[str] = None,
    ) -> Login:
        params = {'format': 'json'}

        if response_token is not None:
            params['responseToken'] = response_token
        elif queue_token is not None:
            params['queueToken'] = queue_token
        elif username is not None and password is not None:
            params['username'] = username
            params['password'] = password
        else:
            raise Exception('Please provide either a username and password, a queue token, or a response token to log in')

        data = self.http.request(Route(
            'POST',
            '/login',
            **params
        ))
        
        return Login(**data)

    def population(self) -> Population:
        data = self.http.request(Route(
            'GET',
            '/population'
        ))

        return Population(**data)

    def silly_meter(self) -> None:
        data = self.http.request(Route(
            'GET',
            '/sillymeter'
        ))

        return SillyMeter(**data)

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, *args):
        self.close()


class AsyncToontownClient(BaseToontownClient):
    """Asynchronous client to interact with the Toontown Rewritten API"""

    def __init__(self) -> None:
        super().__init__(AsyncHTTPClient())

    async def connect(self) -> None:
        await self.http.connect()

    async def close(self) -> None:
        await self.http.close()

    async def doodles(self) -> Doodles:
        data = await self.http.request(Route(
            'GET',
            '/doodles'
        ))

        return Doodles(**data)

    async def field_offices(self) -> FieldOffices:
        data = await self.http.request(Route(
            'GET',
            '/fieldoffices'
        ))

        return FieldOffices(**data)

    async def invasions(self) -> Invasions:
        data = self.http.request(Route(
            'GET',
            '/invasions'
        ))

        return Invasions(**data)

    async def login(
        self, 
        *, 
        username: Optional[str] = None, 
        password: Optional[str] = None,
        response_token: Optional[str] = None,
        queue_token: Optional[str] = None,
    ) -> Login:
        params = {'format': 'json'}

        if response_token is not None:
            params['responseToken'] = response_token
        elif queue_token is not None:
            params['queueToken'] = queue_token
        elif username is not None and password is not None:
            params['username'] = username
            params['password'] = password
        else:
            raise Exception('Please provide either a username and password, a queue token, or a response token to log in')

        data = await self.http.request(Route(
            'POST',
            '/login',
            **params
        ))
        
        return Login(**data)

    async def population(self) -> Population:
        data = await self.http.request(Route(
            'GET',
            '/population'
        ))

        return Population(**data)

    async def silly_meter(self) -> None:
        data = await self.http.request(Route(
            'GET',
            '/sillymeter'
        ))

        return SillyMeter(**data)

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, *args):
        await self.close()
