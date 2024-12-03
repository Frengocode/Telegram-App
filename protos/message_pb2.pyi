from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Message(_message.Message):
    __slots__ = ("id", "user_id", "chat_id", "message", "user")
    ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    CHAT_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    id: int
    user_id: int
    chat_id: int
    message: str
    user: MessageUser
    def __init__(self, id: _Optional[int] = ..., user_id: _Optional[int] = ..., chat_id: _Optional[int] = ..., message: _Optional[str] = ..., user: _Optional[_Union[MessageUser, _Mapping]] = ...) -> None: ...

class CreateMessageRequest(_message.Message):
    __slots__ = ("chat_id", "message", "user_id", "token", "username", "profile_picture", "name")
    CHAT_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PROFILE_PICTURE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    chat_id: int
    message: str
    user_id: int
    token: str
    username: str
    profile_picture: str
    name: str
    def __init__(self, chat_id: _Optional[int] = ..., message: _Optional[str] = ..., user_id: _Optional[int] = ..., token: _Optional[str] = ..., username: _Optional[str] = ..., profile_picture: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class CreateMessageResponse(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: Message
    def __init__(self, message: _Optional[_Union[Message, _Mapping]] = ...) -> None: ...

class GetMessagesResponse(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: _containers.RepeatedCompositeFieldContainer[Message]
    def __init__(self, message: _Optional[_Iterable[_Union[Message, _Mapping]]] = ...) -> None: ...

class GetMessagesRequest(_message.Message):
    __slots__ = ("chat_id", "user_id", "token")
    CHAT_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    chat_id: int
    user_id: int
    token: str
    def __init__(self, chat_id: _Optional[int] = ..., user_id: _Optional[int] = ..., token: _Optional[str] = ...) -> None: ...

class MessageUser(_message.Message):
    __slots__ = ("id", "username", "profile_picture", "name", "surname")
    ID_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PROFILE_PICTURE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SURNAME_FIELD_NUMBER: _ClassVar[int]
    id: int
    username: str
    profile_picture: str
    name: str
    surname: str
    def __init__(self, id: _Optional[int] = ..., username: _Optional[str] = ..., profile_picture: _Optional[str] = ..., name: _Optional[str] = ..., surname: _Optional[str] = ...) -> None: ...

class DeleteMessageRequest(_message.Message):
    __slots__ = ("id", "user_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    user_id: int
    def __init__(self, id: _Optional[int] = ..., user_id: _Optional[int] = ...) -> None: ...

class UpdateMessageRequest(_message.Message):
    __slots__ = ("message", "user_id", "id")
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    message: str
    user_id: int
    id: int
    def __init__(self, message: _Optional[str] = ..., user_id: _Optional[int] = ..., id: _Optional[int] = ...) -> None: ...
