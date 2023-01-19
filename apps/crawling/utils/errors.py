from rest_framework import status
from rest_framework.exceptions import APIException
from drf_yasg import openapi


class ErrorResponse(object):
    def __init__(self, code, system_code, system_message, data=None):
        self.code = code
        self.system_code = system_code
        self.system_message = system_message
        self.data = data

    def response(self):
        res = openapi.Response(
            description=f"{self.system_message}",
            examples={
                "application/json": {
                    "data": self.data,
                    "meta": {                        
                        "code": self.code,
                        "systemCode": self.system_code,                        
                        "systemMessage": self.system_message,
                    },
                }
            },
        )
        return res


class UrlNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Input url is not enrolled for crwaling"
    default_code = "URL_NOT_FOUND"


class UrlNotFoundError(ErrorResponse):
    STATUS_CODE = status.HTTP_404_NOT_FOUND
    SYSTEM_CODE = "URL_NOT_FOUND"
    SYSTEM_MSG = "Input url is not enrolled for crwaling"

    def __init__(self):
        super().__init__(
            self.STATUS_CODE,
            self.SYSTEM_CODE,
            self.SYSTEM_MSG,
        )    