import random
import string
from enum import Enum
from typing import Any, Union, Optional, List

try:
    import ujson as json
except ImportError:
    import json


class SimpleBotException(Exception):
    pass


class UpdateType(str, Enum):
    MESSAGE = "message"
    EDITED_MESSAGE = "edited_message"
    CHANNEL_POST = "channel_post"
    EDITED_CHANNEL_POST = "edited_channel_post"
    INLINE_QUERY = "inline_query"
    CHOSEN_INLINE_RESULT = "chosen_inline_result"
    CALLBACK_QUERY = "callback_query"
    SHIPPING_QUERY = "shipping_query"
    PRE_CHECKOUT_QUERY = "pre_checkout_query"
    POLL = "poll"
    POLL_ANSWER = "poll_answer"
    FORCE_REPLY = "force_reply"
    COMMAND = "command"
    ALL = "all"


ALL_UPDATE_TYPES = list(UpdateType)

MESSAGE_LIKED_UPDATE_TYPES = (
    UpdateType.EDITED_MESSAGE,
    UpdateType.CHANNEL_POST,
    UpdateType.EDITED_CHANNEL_POST,
    UpdateType.MESSAGE,
)


class MessageType(str, Enum):
    TEXT = "text"
    AUDIO = "audio"
    ANIMATION = "animation"
    DOCUMENT = "document"
    GAME = "game"
    PHOTO = "photo"
    STICKER = "sticker"
    VIDEO = "video"
    VIDEO_NOTE = "video_note"
    VOICE = "voice"
    CONTACT = "contact"
    LOCATION = "location"
    VENUE = "venue"
    DICE = "dice"
    NEW_CHAT_MEMBERS = "new_chat_members"
    LEFT_CHAT_MEMBER = "left_chat_member"
    NEW_CHAT_TITLE = "new_chat_title"
    NEW_CHAT_PHOTO = "new_chat_photo"
    DELETE_CHAT_PHOTO = "delete_chat_photo"
    GROUP_CHAT_CREATED = "group_chat_created"
    SUPERGROUP_CHAT_CREATED = "supergroup_chat_created"
    CHANNEL_CHAT_CREATED = "channel_chat_created"
    MIGRATE_TO_CHAT_ID = "migrate_to_chat_id"
    MIGRATE_FROM_CHAT_ID = "migrate_from_chat_id"
    PINNED_MESSAGE = "pinned_message"
    INVOICE = "invoice"
    SUCCESSFUL_PAYMENT = "successful_payment"
    CONNECTED_WEBSITE = "connected_website"
    POLL = "poll"
    PASSPORT_DATA = "passport_data"
    ALL = "all"


ALL_MESSAGE_TYPES = list(MessageType)


class ParseMode(str, Enum):
    MARKDOWN_V2 = "MarkdownV2"
    HTML = "html"
    MARKDOWN = "Markdown"


class PollType(str, Enum):
    QUIZ = "quiz"
    REGULAR = "regular"


class Emoji(str, Enum):
    DICE = "🎲"
    BULLSEYE = "🎯"
    BASKETBALL = "🏀"


class ChatAction(str, Enum):
    UPLOAD_PHOTO = "upload_photo"
    RECORD_VIDEO = "record_video"
    UPLOAD_VIDEO = "upload_video"
    RECORD_AUDIO = "record_audio"
    UPLOAD_AUDIO = "upload_audio"
    UPLOAD_DOCUMENT = "upload_document"
    FIND_LOCATION = "find_location"
    RECORD_VIDEO_NOTE = "record_video_note"
    UPLOAD_VIDEO_NOTE = "upload_video_note"


class MaskPoint(str, Enum):
    FOREHEAD = "forehead"
    EYES = "eyes"
    MOUTH = "mouth"
    CHIN = "chin"


class MIMEType(str, Enum):
    IMAGE_JPEG = "image/jpeg"
    IMAGE_GIF = "image/gif"
    VIDEO_MP4 = "video/mp4"


class InputFile:
    __slots__ = ("_file_name", "_file", "_mime_type", "_attach_key")

    def __init__(self, file_name: str, file: Union[str, bytes], mime_type: Optional[str] = None):
        self._file_name = file_name
        if not isinstance(file, (str, bytes)):
            raise ValueError("file must be a string or bytes")
        self._file = file
        self._mime_type = mime_type
        self._attach_key = None

    @property
    def file_name(self) -> str:
        return self._file_name

    @property
    def file_data(self) -> Optional[bytes]:
        if isinstance(self._file, str):
            with open(self._file, "rb") as file_obj:
                return file_obj.read()
        return self._file

    @property
    def mime_type(self):
        return self._mime_type

    @property
    def file_tuple(self):
        if self.mime_type is None:
            return self.file_name, self.file_data
        return self.file_name, self.file_data, self.mime_type

    @property
    def attach_key(self):
        if self._attach_key is None:
            self._attach_key = "".join(
                random.choice(string.ascii_letters + string.digits) for _ in range(6)
            )
        return self._attach_key

    @property
    def attach_str(self):
        return "attach://{0}".format(self.attach_key)


class SimpleObject(dict):
    def __init__(self, **kwargs):
        data = {name: self.__recurse_init(value) for name, value in kwargs.items()}
        if "from" in data:
            data["from_user"] = data["from"]
            del data["from"]
        super().__init__(data)

    @classmethod
    def __recurse_init(cls, value) -> Any:
        if isinstance(value, SimpleObject):
            return value
        if isinstance(value, dict):
            return SimpleObject(**value)
        if isinstance(value, list):
            return [cls.__recurse_init(item) for item in value]
        return value

    def __getattr__(self, name: str):
        return self.get(name, None)

    def __getitem__(self, name: str):
        return self.get(name, None)

    def __setattr__(self, name: str, value: Any):
        self[name] = value

    def __delitem__(self, name):
        if name in self:
            return super().__delitem__(name)
        return

    @property
    def param(self):
        return self


Update = (
    Message
) = (
    CallbackQuery
) = (
    ChosenInlineResult
) = (
    InlineQuery
) = (
    MessageEntity
) = (
    File
) = (
    User
) = (
    WebhookInfo
) = (
    PhotoSize
) = (
    StickerSet
) = (
    Location
) = (
    ShippingAddress
) = (
    OrderInfo
) = (
    EncryptedPassportElement
) = (
    EncryptedCredentials
) = (
    PassportFile
) = (
    PassportElementError
) = (
    CallbackGame
) = GameHighScore = VCard = ShippingQuery = PreCheckoutQuery = Poll = PollAnswer = SimpleObject


class MentionEntity(MessageEntity):
    def __init__(self):
        super().__init__(type="mention")


class HashTagEntity(MessageEntity):
    def __init__(self):
        super().__init__(type="hashtag")


class CashTagEntity(MessageEntity):
    def __init__(self):
        super().__init__(type="cashtag")


class BotCommandEntity(MessageEntity):
    def __init__(self):
        super().__init__(type="bot_command")


class URLEntity(MessageEntity):
    def __init__(self):
        super().__init__(type="url")


class EmailEntity(MessageEntity):
    def __init__(self):
        super().__init__(type="email")


class PhoneNumberEntity(MessageEntity):
    def __init__(self):
        super().__init__(type="phone_number")


class BoldEntity(MessageEntity):
    def __init__(self):
        super().__init__(type="bold")


class ItalicEntity(MessageEntity):
    def __init__(self):
        super().__init__(type="italic")


class UnderLineEntity(MessageEntity):
    def __init__(self):
        super().__init__(type="underline")


class StrikeThroughEntity(MessageEntity):
    def __init__(self):
        super().__init__(type="strikethrough")


class CodeEntity(MessageEntity):
    def __init__(self):
        super().__init__(type="code")


class PreEntity(MessageEntity):
    def __init__(self, language: str):
        super().__init__(type="pre", language=language)


class TextLinkEntity(MessageEntity):
    def __init__(self, url: str):
        super().__init__(type="text_link", url=url)


class TextMentionEntity(MessageEntity):
    def __init__(self, user: User):
        super().__init__(type="text_mention", user=user)


class InputMedia(SimpleObject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._attached_files = []
        media = self.get("media", None)
        if media and isinstance(media, InputFile):
            self._attached_files.append((media.attach_key, media.file_tuple))
            self["media"] = media.attach_str
        thumb = self.get("thumb", None)
        if thumb and isinstance(thumb, InputFile):
            self._attached_files.append((thumb.attach_key, thumb.file_tuple))
            self["thumb"] = thumb.attach_str
        self._media_data = {
            name: value for name, value in self.items() if name != "_attached_files"
        }

    @property
    def param(self):
        return json.dumps(self._media_data)

    @property
    def media_data(self):
        return self._media_data

    @property
    def attached_files(self):
        return self._attached_files


class InputMediaPhoto(InputMedia):
    def __init__(self, media: Union[str, InputFile], **kwargs):
        super().__init__(type="photo", media=media, **kwargs)


class InputMediaVideo(InputMedia):
    def __init__(
        self, media: Union[InputFile, str], thumb: Optional[Union[InputFile, str]], **kwargs
    ):
        super().__init__(type="video", media=media, thumb=thumb, **kwargs)


class InputMediaAnimation(InputMedia):
    def __init__(
        self, media: Union[InputFile, str], thumb: Optional[Union[InputFile, str]], **kwargs
    ):
        super().__init__(type="animation", media=media, thumb=thumb, **kwargs)


class InputMediaAudio(InputMedia):
    def __init__(
        self, media: Union[InputFile, str], thumb: Optional[Union[InputFile, str]], **kwargs
    ):
        super().__init__(type="audio", media=media, thumb=thumb, **kwargs)


class InputMediaDocument(InputMedia):
    def __init__(
        self, media: Union[InputFile, str], thumb: Optional[Union[InputFile, str]], **kwargs
    ):
        super().__init__(type="document", media=media, thumb=thumb, **kwargs)


class InlineKeyboardButton(SimpleObject):
    def __init__(self, text: str, **kwargs):
        super().__init__(text=text, **kwargs)


class KeyboardButtonPollType(SimpleObject):
    def __init__(self, poll_type: Union[str, PollType]):
        super().__init__(type=poll_type)


class KeyboardButton(SimpleObject):
    def __init__(self, text: str, **kwargs):
        super().__init__(text=text, **kwargs)


class MarkupObject(SimpleObject):
    @property
    def param(self):
        return json.dumps(self)


class InlineKeyboardMarkup(MarkupObject):
    def __init__(self, inline_keyboard: List[InlineKeyboardButton]):
        super().__init__(inline_keyboard=inline_keyboard)


class ReplyKeyboardMarkup(MarkupObject):
    def __init__(self, keyboard: List[KeyboardButton], **kwargs):
        super().__init__(keyboard=keyboard, **kwargs)


class ReplyKeyboardRemove(MarkupObject):
    def __init__(self, remove_keyboard: bool = True, **kwargs):
        super().__init__(remove_keyboard=remove_keyboard, **kwargs)


class ForceReply(MarkupObject):
    def __init__(self, force_reply: bool = True, **kwargs):
        super().__init__(force_reply=force_reply, **kwargs)


InputMessageContent = SimpleObject


class InputTextMessageContent(InputMessageContent):
    def __init__(self, message_text: str, **kwargs):
        super().__init__(message_text=message_text, **kwargs)


class InputLocationMessageContent(InputMessageContent):
    def __init__(self, latitude: float, longitude: float, **kwargs):
        super().__init__(latitude=latitude, longitude=longitude, **kwargs)


class InputVenueMessageContent(InputMessageContent):
    def __init__(self, latitude: float, longitude: float, title: str, address: str, **kwargs):
        super().__init__(
            latitude=latitude, longitude=longitude, title=title, address=address, **kwargs
        )


class InputContactMessageContent(InputMessageContent):
    def __init__(self, phone_number: str, first_name: str, **kwargs):
        super().__init__(phone_number=phone_number, first_name=first_name, **kwargs)


InlineQueryResult = SimpleObject


class InlineQueryResultArticle(InlineQueryResult):
    def __init__(self, id: str, title: float, input_message_content: InputMessageContent, **kwargs):
        super().__init__(
            type="article",
            id=id,
            title=title,
            input_message_content=input_message_content,
            **kwargs
        )


class InlineQueryResultPhoto(InlineQueryResult):
    def __init__(self, id: str, photo_url: str, thumb_url: str, **kwargs):
        super().__init__(type="photo", id=id, photo_url=photo_url, thumb_url=thumb_url, **kwargs)


class InlineQueryResultGif(InlineQueryResult):
    def __init__(self, id: str, gif_url: str, thumb_url: str, **kwargs):
        super().__init__(type="gif", id=id, gif_url=gif_url, thumb_url=thumb_url, **kwargs)


class InlineQueryResultMpeg4Gif(InlineQueryResult):
    def __init__(self, id: str, mpeg4_url: str, **kwargs):
        super().__init__(type="mpeg4_gif", id=id, mpeg4_url=mpeg4_url, **kwargs)


class InlineQueryResultAudio(SimpleObject):
    def __init__(self, id: str, audio_url: str, file: str, **kwargs):
        super().__init__(type="audio", id=id, audio_url=audio_url, file=file, **kwargs)


class InlineQueryResultVoice(SimpleObject):
    def __init__(self, id: str, voice_url: str, title: str, **kwargs):
        super().__init__(type="voice", id=id, voice_url=voice_url, title=title, **kwargs)


class InlineQueryResultDocument(SimpleObject):
    def __init__(self, id: str, title: str, document_url: str, mime_type: str, **kwargs):
        super().__init__(
            type="document",
            id=id,
            title=title,
            document_url=document_url,
            mime_type=mime_type,
            **kwargs
        )


class InlineQueryResultLocation(SimpleObject):
    def __init__(self, id: str, latitude: float, longitude: float, title: str, **kwargs):
        super().__init__(
            type="location", id=id, latitude=latitude, longitude=longitude, title=title, **kwargs
        )


class InlineQueryResultVenue(InlineQueryResult):
    def __init__(
        self, id: str, latitude: float, longitude: float, title: str, address: str, **kwargs
    ):
        super().__init__(
            type="venue",
            id=id,
            latitude=latitude,
            longitude=longitude,
            title=title,
            address=address,
            **kwargs
        )


class InlineQueryResultContact(SimpleObject):
    def __init__(self, id: str, phone_number: str, first_name: str, **kwargs):
        super().__init__(
            type="contact", id=id, phone_number=phone_number, first_name=first_name, **kwargs
        )


class InlineQueryResultGame(SimpleObject):
    def __init__(self, id: str, game_short_name: str, **kwargs):
        super().__init__(type="game", id=id, game_short_name=game_short_name, **kwargs)


class InlineQueryResultCachedPhoto(SimpleObject):
    def __init__(self, id: str, photo_file_id: str, **kwargs):
        super().__init__(type="photo", id=id, photo_file_id=photo_file_id, **kwargs)


class InlineQueryResultCachedGif(SimpleObject):
    def __init__(self, id: str, gif_file_id: str, **kwargs):
        super().__init__(type="git", id=id, gif_file_id=gif_file_id, **kwargs)


class InlineQueryResultCachedMpeg4Gif(SimpleObject):
    def __init__(self, id: str, mpeg4_file_id: str, **kwargs):
        super().__init__(type="mpeg4_gif", id=id, mpeg4_file_id=mpeg4_file_id, **kwargs)


class InlineQueryResultCachedSticker(SimpleObject):
    def __init__(self, id: str, sticker_file_id: str, **kwargs):
        super().__init__(type="sticker", id=id, sticker_file_id=sticker_file_id, **kwargs)


class InlineQueryResultCachedDocument(SimpleObject):
    def __init__(self, id: str, title: str, document_file_id: str, **kwargs):
        super().__init__(
            type="document", id=id, title=title, document_file_id=document_file_id, **kwargs
        )


class InlineQueryResultCachedVideo(SimpleObject):
    def __init__(self, id: str, title: str, video_file_id: str, **kwargs):
        super().__init__(type="video", id=id, title=title, video_file_id=video_file_id, **kwargs)


class InlineQueryResultCachedVoice(SimpleObject):
    def __init__(self, id: str, title: str, voice_file_id: str, **kwargs):
        super().__init__(type="voice", id=id, title=title, voice_file_id=voice_file_id, **kwargs)


class InlineQueryResultCachedAudio(SimpleObject):
    def __init__(self, id: str, audio_file_id: str, **kwargs):
        super().__init__(type="audio", id=id, audio_file_id=audio_file_id, **kwargs)


class UserProfilePhotos(SimpleObject):
    def __init__(self, total_count: int, photos: List[List[PhotoSize]]):
        super().__init__(total_count=total_count, photos=photos)


class LoginUrl(SimpleObject):
    def __init__(self, url: str, **kwargs):
        super().__init__(url=url, **kwargs)


class BotCommand(SimpleObject):
    def __init__(self, command: str, description: str):
        super().__init__(command=command, description=description)


class Animation(SimpleObject):
    def __init__(
        self, file_id: str, file_unique_id: str, width: int, length: int, duration: int, **kwargs
    ):
        super().__init__(
            file_id=file_id,
            file_unique_id=file_unique_id,
            width=width,
            length=length,
            duration=duration,
            **kwargs
        )


class MaskPosition(SimpleObject):
    def __init__(self, point: str, x_shift: float, y_shift: float, scale: float, **kwargs):
        super().__init__(point=point, x_shift=x_shift, y_shift=y_shift, scale=scale, **kwargs)

    @property
    def param(self):
        return json.dumps(self)


class Sticker(SimpleObject):
    def __init__(self, file_id: str, file_unique_id: str, width: int, length: int, **kwargs):
        super().__init__(
            file_id=file_id, file_unique_id=file_unique_id, width=width, length=length, **kwargs
        )


class LabeledPrice(SimpleObject):
    def __init__(self, label: str, amount: int, **kwargs):
        super().__init__(label=label, amount=amount, **kwargs)

    @property
    def param(self):
        return json.dumps(self)


class ShippingOption(SimpleObject):
    def __init__(self, id: str, title: str, prices: List[LabeledPrice], **kwargs):
        super().__init__(id=id, title=title, prices=prices, **kwargs)


class ChatPermissions(SimpleObject):
    def __init__(
        self,
        can_send_messages: Optional[bool] = None,
        can_send_media_messages: Optional[bool] = None,
        can_send_polls: Optional[bool] = None,
        can_send_other_messages: Optional[bool] = None,
        can_add_web_page_previews: Optional[bool] = None,
        can_change_info: Optional[bool] = None,
        can_invite_users: Optional[bool] = None,
        can_pin_messages: Optional[bool] = None,
    ):
        super().__init__(
            can_send_messages=can_send_messages,
            can_send_media_messages=can_send_media_messages,
            can_send_polls=can_send_polls,
            can_send_other_messages=can_send_other_messages,
            can_add_web_page_previews=can_add_web_page_previews,
            can_change_info=can_change_info,
            can_invite_users=can_invite_users,
            can_pin_messages=can_pin_messages,
        )

    @property
    def param(self):
        return json.dumps(self)
