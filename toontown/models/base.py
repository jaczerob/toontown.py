from ..exceptions import FailedResponse


class BaseAPIModel:
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)

        if kwargs.get('error', None):
            raise FailedResponse(kwargs['error'])
            
        return instance