# -*- coding: utf-8 -*-


class TokenException(Exception):
    pass


class TokenAPIError(TokenException):
    pass


class TokenNotExist(TokenException):
    pass
