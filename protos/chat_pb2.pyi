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

class Chat(_message.Message):
    __slots__ = ("id", "chat_author_id", "chat_member_id", "chat_author", "chat_member")
    ID_FIELD_NUMBER: _ClassVar[int]
    CHAT_AUTHOR_ID_FIELD_NUMBER: _ClassVar[int]
    CHAT_MEMBER_ID_FIELD_NUMBER: _ClassVar[int]
    CHAT_AUTHOR_FIELD_NUMBER: _ClassVar[int]
    CHAT_MEMBER_FIELD_NUMBER: _ClassVar[int]
    id: int
    chat_author_id: int
    chat_member_id: int
    chat_author: ChatUser
    chat_member: ChatUser
    def __init__(
        self,
        id: _Optional[int] = ...,
        chat_author_id: _Optional[int] = ...,
        chat_member_id: _Optional[int] = ...,
        chat_author: _Optional[_Union[ChatUser, _Mapping]] = ...,
        chat_member: _Optional[_Union[ChatUser, _Mapping]] = ...,
    ) -> None: ...

class CreateChatRequest(_message.Message):
    __slots__ = ("member_id", "author_id")
    MEMBER_ID_FIELD_NUMBER: _ClassVar[int]
    AUTHOR_ID_FIELD_NUMBER: _ClassVar[int]
    member_id: int
    author_id: int
    def __init__(
        self, member_id: _Optional[int] = ..., author_id: _Optional[int] = ...
    ) -> None: ...

class ChatUser(_message.Message):
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

class CreateChatResponse(_message.Message):
    __slots__ = ("chat",)
    CHAT_FIELD_NUMBER: _ClassVar[int]
    chat: Chat
    def __init__(self, chat: _Optional[_Union[Chat, _Mapping]] = ...) -> None: ...

class GetUserChatsResponse(_message.Message):
    __slots__ = ("chat",)
    CHAT_FIELD_NUMBER: _ClassVar[int]
    chat: _containers.RepeatedCompositeFieldContainer[Chat]
    def __init__(
        self, chat: _Optional[_Iterable[_Union[Chat, _Mapping]]] = ...
    ) -> None: ...

class GetUserChatsRequest(_message.Message):
    __slots__ = ("author_id",)
    AUTHOR_ID_FIELD_NUMBER: _ClassVar[int]
    author_id: int
    def __init__(self, author_id: _Optional[int] = ...) -> None: ...

class GetUserChatResponse(_message.Message):
    __slots__ = ("chat",)
    CHAT_FIELD_NUMBER: _ClassVar[int]
    chat: Chat
    def __init__(self, chat: _Optional[_Union[Chat, _Mapping]] = ...) -> None: ...

class GetUserChatRequest(_message.Message):
    __slots__ = ("author_id", "id")
    AUTHOR_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    author_id: int
    id: int
    def __init__(
        self, author_id: _Optional[int] = ..., id: _Optional[int] = ...
    ) -> None: ...

class DeleteChatRequest(_message.Message):
    __slots__ = ("id", "author_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    AUTHOR_ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    author_id: int
    def __init__(
        self, id: _Optional[int] = ..., author_id: _Optional[int] = ...
    ) -> None: ...

class DeleteChatResponse(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...
