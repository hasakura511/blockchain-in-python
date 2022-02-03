from fastapi import HTTPException, status


class TitleException(Exception):
    def __init__(self, name: str):
        self.name = name


class HTTPExceptions:
    @staticmethod
    def user_not_found(detail):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

    @staticmethod
    def unprocessable(detail):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail
        )

