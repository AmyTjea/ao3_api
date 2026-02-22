from typing import Optional, Union
from app.api.schemas.users import UserMetadata
from pydantic import BaseModel, HttpUrl


# TODO: add in collections + series involved in into metadata
class WorkMetadata(BaseModel):
    id: int
    title: str
    url: str
    authors: list[Union[str, UserMetadata]]
    fandoms: list[str]
    rating: str
    n_chapters: int
    complete: bool
    n_hits: int
    n_kudos: int
    n_bookmarks: int
    word_count: int

    model_config = {"from_attributes": True}


class WorkText(BaseModel):
    id: int
    title: str
    text: str

    model_config = {"from_attributes": True}


class Chapter(BaseModel):
    id: int
    number: int
    words: int
    summary: str
    start_notes: str
    end_notes: str
    url: str
    title: str
    text: str

    model_config = {"from_attributes": True}


class WorkChapter(BaseModel):
    id: int
    title: str
    text: str
    chapters: list[Chapter]

    model_config = {"from_attributes": True}


# TODO: allow for expanding author + add link to chapters
class Comment(BaseModel):
    id: int
    author: Union[str, UserMetadata]
    parent_comment: Optional["Comment"] = None
    text: str

    model_config = {"from_attributes": True}


Comment.model_rebuild()


class WorkComments(BaseModel):
    id: int
    n_comments: int
    comments: list[Comment]

    model_config = {"from_attributes": True}


class Image(BaseModel):
    paragraph_num: int
    src: HttpUrl

    model_config = {"from_attributes": True}


class ChapterImage(BaseModel):
    chapter_number: int  # mb have chapter model? probs not tho
    images: list[Image]
    model_config = {"from_attributes": True}


class WorkImages(BaseModel):
    id: int
    images: list[ChapterImage]

    model_config = {"from_attributes": True}


# have list of
class WorkBookmarks(BaseModel):
    id: int
    bookmarkers: list[Union[UserMetadata, str]]

    model_config = {"from_attributes": True}


# TODO: MOVE TO UTILS OR SOMEWHERE BETTER
# helper function to collapse authors
def collapse_authors(work_model: WorkMetadata, work_obj):
    return work_model.model_copy(
        update={"authors": [a.username for a in work_obj.authors]}
    )