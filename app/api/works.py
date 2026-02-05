from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse

from app.AO3.works import Work
from app.AO3 import utils

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

@router.get("/{work_id}")
def get_work_metadata(work_id: int):
    work = load_work(work_id, load_chapters=False)
    return work.metadata

# get subdetails for only minimal datat

@router.get("/{work_id}/text")
def get_work_text(work_id: int):
    work = load_work(work_id, load_chapters=True)
    return {
        "id": work.id,
        "title": work.title,
        "text": work.text,
    }

@router.get("/{work_id}/chapters")
def get_work_chapters(work_id: int):
    work = load_work(work_id, load_chapters=True)

    return {
        "id": work.id,
        "chapters": [
            {
                "number": chapter.number,
                "title": chapter.title,
                "text": chapter.text,
            }
            for chapter in work.chapters
        ],
    }

@router.get("/{work_id}/comments")
def get_work_comments(
    work_id: int,
    maximum: int | None = Query(default=50, ge=1, le=500),
):
    work = load_work(work_id, load_chapters=False)

    comments = work.get_comments(maximum=maximum)

    return [
        {
            "id": c.id,
            "author": c.author.username if c.author else None,
            "text": c.text,
        }
        for c in comments
    ]

@router.get("/{work_id}/images")
def get_work_images(work_id: int):
    work = load_work(work_id, load_chapters=True)
    return work.get_images()


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
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"'
        },
    )


@router.get("/{work_id}/bookmarks") #get users who bookmark
def get_work_bookmarks(
    work_id: int,
):
    work = load_work(work_id, load_chapters=False)

    bookmarks = work.get_bookmarkers()

    return [
        {
            "username": c.username 
        }
        for c in bookmarks
    ]
#@router.get("/{work_id}/kudos") #return user ids + number kudos


