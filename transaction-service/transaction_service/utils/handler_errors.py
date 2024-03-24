from mongoengine import ValidationError, FieldDoesNotExist, DoesNotExist
from sanic import exceptions


class HandlerError(object):
    def __init__(self, func):
        self.func = func

    async def __call__(self, *args, **kwargs):
        try:
            result = await self.func(*args, **kwargs)
        except (ValidationError, FieldDoesNotExist, AttributeError) as e:
            raise exceptions.BadRequest
        except DoesNotExist as e:
            raise exceptions.NotFound
        except Exception as e:
            raise exceptions.ServerError
        return result
