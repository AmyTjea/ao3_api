from typing import Literal
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse

from app.AO3.works import Work
from app.AO3 import utils
from app.api.schemas.works import *

router = APIRouter()


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
    expand: list[
        Literal[
            "authors",
            "series",
            "collections",
        ]
    ] = Query(default=[]),
):
    work = load_work(work_id, load_chapters=False)

    res = WorkMetadata.model_validate(work)

    if "authors" not in expand:
        res = res.model_copy(update={"authors": [a.username for a in work.authors]})

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
        bookmarkers = [a.username for a in bookmarkers]

    return WorkBookmarks(
        id=work_id,
        bookmarkers=bookmarkers,
    )


# @router.get("/{work_id}/kudos") #return usernames + number kudos
