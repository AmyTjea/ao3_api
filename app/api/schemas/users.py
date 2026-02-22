from typing import Union
from pydantic import BaseModel
from datetime import date

class UserMetadata(BaseModel):
    username: str
    url: str
    avatar: str
    bio: str
    join_date: date
    id: int
    pseuds: list[str]
    n_works: int
    n_bookmarks: int
    n_series: int
    n_collections: int
    n_gifts: int

    model_config = {"from_attributes": True}


class UserWorks(BaseModel):
    username: str
    n_works: int
    works: list[Union[int, "WorkMetadata"]]
    model_config = {"from_attributes": True}

class Bookmark(BaseModel):
    type:Literal["Series","Work"]
    bookmark: Union[Union["WorkMetadata","SeriesMetadata"],int] # either give entire metadata or just id


class UserBookmarks(BaseModel):
    bookmarks:list[Bookmark]

# TODO: Define Series api endpoint and put in series metadata
# TODO: MANAGE BASE MODELS
# class Bookmark(BaseModel):

#     id:int
#     bookmarker: Union[str, UserMetadata]
#     bookmark: Union[WorkMetadata]#,SeriesMetadata]