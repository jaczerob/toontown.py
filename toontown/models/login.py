from typing import Literal, Optional


__all__ = ['Login']


class Login:
    """"Wrapper class for /login response
    
    Attributes
    ----------
    success : Literal['false', 'partial', 'true', 'delayed']
        what type of response the login gave

    banner : Optional[str]
        an optional reason from the server if `false` or `partial` was given for success

    response_token : Optional[str]
        if success is `partial`, a token to verify a ToonGuard response to the server

    gameserver : Optional[str]
        if success is `true`, Toontown Rewritten's gameserver IP

    cookie : Optional[str]
        if success is `true`, your Toontown Rewritten session identifier

    eta : Optional[int]
        if success is `delayed`, how many seconds you are estimated to be able to play

    position : Optional[int]
        if success is `delayed`, how many toons are ahead of you in queue

    queue_token : Optional[str]
        if success is `delayed`, this identifier holds your position in queue
    """

    __slots__ = ['success', 'banner', 'response_token', 'gameserver', 'cookie', 'eta', 'position', 'queue_token']

    def __init__(self, **payload) -> None:
        self.success: Literal['false', 'partial', 'true', 'delayed'] = payload.get('success')
        self.banner: Optional[str] = payload.get('banner', None)
        self.response_token: Optional[str] = payload.get('responseToken', None)
        self.gameserver: Optional[str] = payload.get('gameserver', None)
        self.cookie: Optional[str] = payload.get('cookie', None)
        self.eta: Optional[int] = payload.get('eta', None)
        self.position: Optional[int] = payload.get('position', None)
        self.queue_token: Optional[str] = payload.get('queue_token', None)
