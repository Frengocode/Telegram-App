from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class User(_message.Message):
    __slots__ = ("id", "username", "profile_picture", "name", "surname", "age", "email")
    ID_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PROFILE_PICTURE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SURNAME_FIELD_NUMBER: _ClassVar[int]
    AGE_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    id: int
    username: str
    profile_picture: str
    name: str
    surname: str
    age: int
    email: str
    def __init__(self, id: _Optional[int] = ..., username: _Optional[str] = ..., profile_picture: _Optional[str] = ..., name: _Optional[str] = ..., surname: _Optional[str] = ..., age: _Optional[int] = ..., email: _Optional[str] = ...) -> None: ...

class CreateUserRequest(_message.Message):
    __slots__ = ("username", "password", "name", "email")
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    username: str
    password: str
    name: str
    email: str
    def __init__(self, username: _Optional[str] = ..., password: _Optional[str] = ..., name: _Optional[str] = ..., email: _Optional[str] = ...) -> None: ...

class CreateUserResponse(_message.Message):
    __slots__ = ("user",)
    USER_FIELD_NUMBER: _ClassVar[int]
    user: User
    def __init__(self, user: _Optional[_Union[User, _Mapping]] = ...) -> None: ...

class GetUserByUsernamePasswordRequest(_message.Message):
    __slots__ = ("username", "password")
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    username: str
    password: str
    def __init__(self, username: _Optional[str] = ..., password: _Optional[str] = ...) -> None: ...

class GetUserByUsernamePasswordResponse(_message.Message):
    __slots__ = ("user",)
    USER_FIELD_NUMBER: _ClassVar[int]
    user: User
    def __init__(self, user: _Optional[_Union[User, _Mapping]] = ...) -> None: ...

class GetUserResponse(_message.Message):
    __slots__ = ("id", "username", "profile_picture", "name", "surname", "age", "email")
    ID_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PROFILE_PICTURE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SURNAME_FIELD_NUMBER: _ClassVar[int]
    AGE_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    id: int
    username: str
    profile_picture: str
    name: str
    surname: str
    age: int
    email: str
    def __init__(self, id: _Optional[int] = ..., username: _Optional[str] = ..., profile_picture: _Optional[str] = ..., name: _Optional[str] = ..., surname: _Optional[str] = ..., age: _Optional[int] = ..., email: _Optional[str] = ...) -> None: ...

class GetUserRequest(_message.Message):
    __slots__ = ("username",)
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    username: str
    def __init__(self, username: _Optional[str] = ...) -> None: ...

class GetUserByIdRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class GetUserByIdResponse(_message.Message):
    __slots__ = ("user",)
    USER_FIELD_NUMBER: _ClassVar[int]
    user: User
    def __init__(self, user: _Optional[_Union[User, _Mapping]] = ...) -> None: ...
