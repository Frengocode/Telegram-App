from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Auth(_message.Message):
    __slots__ = ("access_token", "token_type")
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TOKEN_TYPE_FIELD_NUMBER: _ClassVar[int]
    access_token: str
    token_type: str
    def __init__(self, access_token: _Optional[str] = ..., token_type: _Optional[str] = ...) -> None: ...

class LoginRequest(_message.Message):
    __slots__ = ("username", "password")
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    username: str
    password: str
    def __init__(self, username: _Optional[str] = ..., password: _Optional[str] = ...) -> None: ...

class LoginResponse(_message.Message):
    __slots__ = ("access_token", "token_type")
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TOKEN_TYPE_FIELD_NUMBER: _ClassVar[int]
    access_token: str
    token_type: str
    def __init__(self, access_token: _Optional[str] = ..., token_type: _Optional[str] = ...) -> None: ...
