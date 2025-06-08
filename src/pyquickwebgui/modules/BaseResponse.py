

import logging
from typing import Any
from dataclasses import dataclass




logger = logging.getLogger(__name__)

@dataclass
class BaseResponse():

    STATUS_CODES = {
        0: "Success",
        400: "Bad Request",
        401: "Unauthorized",
        403: "Forbidden",
        404: "Not Found",
        500: "Internal Server Error",
    }

    # 状态码
    code: int
    # 状态/错误信息
    message: str
    # 数据
    data: Any = None

    @classmethod
    def success(cls, data = None, message: str = "Success") :
        return cls(code=0, message=message, data=data)

    @classmethod
    def error(cls, code: int, message: str = None) :
        message = message or cls.STATUS_CODES.get(code, "Unknown Error")
        return cls(code=code, message=message)