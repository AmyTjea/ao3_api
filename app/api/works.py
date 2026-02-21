from typing import Literal, Optional, Union
from app.api.users import UserMetadata
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, HttpUrl

from app.AO3.works import Work
from app.AO3 import utils

router = APIRouter()

ExpandField = Literal[
    "authors",
    "series",
    "collections",
]


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


def load_work(work_id: int, load_chapters: bool = True) -> Work:
    try:
        return Work(work_id, load=True, load_chapters=load_chapters)
    except utils.InvalidIdError:
        raise HTTPException(status_code=404, detail="Work not found")
    except utils.HTTPError as e:
        raise HTTPException(status_code=429, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{work_id}", response_model=WorkMetadata)
def get_work_metadata(
    work_id: int,
    expand: list[ExpandField] = Query(default=[]),
):
    work = load_work(work_id, load_chapters=False)

    res = WorkMetadata.model_validate(work)

    if "authors" not in expand:
        res.authors = [a.username for a in work.authors]

    return res


# get subdetails for only minimal datat


@router.get("/{work_id}/text", response_model=WorkText)
def get_work_text(work_id: int):
    work = load_work(work_id, load_chapters=True)
    return WorkText.model_validate(work)


@router.get("/{work_id}/chapters", response_model=WorkChapter)
def get_work_chapters(work_id: int):
    work = load_work(work_id, load_chapters=True)
    res = WorkChapter.model_validate(work)

    return res


@router.get("/{work_id}/comments", response_model=WorkComments)
def get_work_comments(
    work_id: int,
    maximum: int | None = Query(default=50, ge=1, le=500),
):
    work = load_work(work_id, load_chapters=False)
    work.get_comments(maximum=maximum)
    res = WorkComments.model_validate(work)

    return res


# test with 74300936
@router.get("/{work_id}/images", response_model=WorkImages)
def get_work_images(work_id: int):
    work = load_work(work_id, load_chapters=True)
    print(work.get_images())

    res = WorkImages.model_validate(work)

    return res


@router.get("/{work_id}/download")
def download_work(
    work_id: int,
    filetype: str = Query(default="PDF", regex="^(PDF|EPUB|HTML|MOBI|AZW3)$"),
):
    work = load_work(work_id, load_chapters=False)

    try:
        content = work.download(filetype=filetype)
    except utils.UnexpectedResponseError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except utils.DownloadError as e:
        raise HTTPException(status_code=500, detail=str(e))

    filename = f"ao3_{work_id}.{filetype.lower()}"

    return StreamingResponse(
        iter([content]),
        media_type="application/octet-stream",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.get(
    "/{work_id}/bookmarks", response_model=WorkBookmarks
)  # get users who bookmark
def get_work_bookmarks(
    work_id: int,
    expand: list[Literal["authors"]] = Query(default=[]),
):
    work = load_work(work_id, load_chapters=False)

    bookmarkers = work.get_bookmarkers()

    
    
    if "authors" not in expand:
        bookmarkers= [a.username for a in bookmarkers]

    return WorkBookmarks(
        id=work_id,
        bookmarkers=bookmarkers,
    )


# @router.get("/{work_id}/kudos") #return usernames + number kudos
