from pydantic import BaseModel

from datemite import datetime
from typing import Optional
from enum import StrEnum


class FileModeEnum(StrEnum):
    SOURCE = "source"
    RENDER = "render"

class FileVisibilityEnum(StrEnum):
    PUBLIC = "public"
    HIDDEN = "hidden"
    ONEC = "once"


class FileBase(BaseModel):
    id : int
    user_id : int 
    title : str
    path : str
    views : int
    blob_hash : str
    mode : int 
    visibility : int 
    password : Optional[str]
    as_guest : bool 
    modified : datetime 

class FileRead(FileBase):
    content: Optional[bytes | str] = None

class FileCreate(FileBase):
    path: Optional[str]
    content: str | bytes
    user: str
    mode: FileModeEnum
    visibility: FileVisibilityEnum
    password: Optional[str]

class FlieUpdate(FileBase):
    path: Optional[str]
    content: Optional[str | bytes]
    mode: Optional[FileModeEnum]
    visibility: Optional[FileVisibilityEnum]


