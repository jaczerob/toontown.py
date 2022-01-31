from dataclasses import dataclass

from .base import BaseAPIModel


__all__ = ['Login', 'FailedLogin', 'PartialLogin', 'DelayedLogin', 'SuccessfulLogin']


class Login(BaseAPIModel):
    def __new__(cls, *args, **kwargs):
        super().__new__(cls, *args, **kwargs)
        
        success = kwargs.get('success')
        if success == 'true':
            return SuccessfulLogin(kwargs.get('gameserver'), kwargs.get('cookie'))
        elif success == 'delayed':
            return DelayedLogin(kwargs.get('eta'), kwargs.get('position'), kwargs.get('queueToken'))

        banner = kwargs.get('banner')

        if success == 'false':
            return FailedLogin(banner)
        elif success == 'partial':
            return PartialLogin(banner, kwargs.get('responseToken'))


@dataclass
class FailedLogin:
    banner: str


@dataclass
class PartialLogin:
    banner: str
    response_token: str


@dataclass
class DelayedLogin:
    eta: int
    position: int
    queue_token: str


@dataclass
class SuccessfulLogin:
    gameserver: str
    cookie: str
