from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import (
    ClassVar as _ClassVar,
    Iterable as _Iterable,
    Mapping as _Mapping,
    Optional as _Optional,
    Union as _Union,
)

DESCRIPTOR: _descriptor.FileDescriptor

class HistoryUser(_message.Message):
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
    def __init__(
        self,
        id: _Optional[int] = ...,
        username: _Optional[str] = ...,
        profile_picture: _Optional[str] = ...,
        name: _Optional[str] = ...,
        surname: _Optional[str] = ...,
        age: _Optional[int] = ...,
        email: _Optional[str] = ...,
    ) -> None: ...

class History(_message.Message):
    __slots__ = ("id", "user_id", "content", "content_title", "user")
    ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    CONTENT_TITLE_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    id: int
    user_id: int
    content: str
    content_title: str
    user: HistoryUser
    def __init__(
        self,
        id: _Optional[int] = ...,
        user_id: _Optional[int] = ...,
        content: _Optional[str] = ...,
        content_title: _Optional[str] = ...,
        user: _Optional[_Union[HistoryUser, _Mapping]] = ...,
    ) -> None: ...

class CreateHistoryRequest(_message.Message):
    __slots__ = ("content", "content_title", "user_id")
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    CONTENT_TITLE_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    content: bytes
    content_title: str
    user_id: int
    def __init__(
        self,
        content: _Optional[bytes] = ...,
        content_title: _Optional[str] = ...,
        user_id: _Optional[int] = ...,
    ) -> None: ...

class CreateHistoryResponse(_message.Message):
    __slots__ = ("history",)
    HISTORY_FIELD_NUMBER: _ClassVar[int]
    history: History
    def __init__(self, history: _Optional[_Union[History, _Mapping]] = ...) -> None: ...

class GetHistorysRequest(_message.Message):
    __slots__ = ("user_id",)
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: int
    def __init__(self, user_id: _Optional[int] = ...) -> None: ...

class GetHistorysResponse(_message.Message):
    __slots__ = ("historys",)
    HISTORYS_FIELD_NUMBER: _ClassVar[int]
    historys: _containers.RepeatedCompositeFieldContainer[History]
    def __init__(
        self, historys: _Optional[_Iterable[_Union[History, _Mapping]]] = ...
    ) -> None: ...

class GetHistoryRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class GetHistoryResponse(_message.Message):
    __slots__ = ("history",)
    HISTORY_FIELD_NUMBER: _ClassVar[int]
    history: History
    def __init__(self, history: _Optional[_Union[History, _Mapping]] = ...) -> None: ...

class DeleteHistoryRequest(_message.Message):
    __slots__ = ("id", "user_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    user_id: int
    def __init__(
        self, id: _Optional[int] = ..., user_id: _Optional[int] = ...
    ) -> None: ...

class DeleteHistoryResponse(_message.Message):
    __slots__ = ("response",)
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: str
    def __init__(self, response: _Optional[str] = ...) -> None: ...
