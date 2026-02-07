from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse

from app.AO3.users import User
from app.AO3 import utils

router = APIRouter()


def load_user(username: str) -> User:
    try:
        return User(username)
    except utils.InvalidIdError:
        raise HTTPException(status_code=404, detail="User not found")
    except utils.HTTPError as e:
        raise HTTPException(status_code=429, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{username}")
def get_user_metadata(username: str):
    # get username, url, avatar, bio,pseuds,join date,userid,bio
    user = load_user(username)
    return {
        "username": user.username,
        "url": user.url,
        "avatar": user.get_avatar(),
        "bio": user.bio,
        "id": user.id,
        "pseuds": user.pseuds,
        "join_date": user.join_date,
    }


@router.get("/{username}/works")
def get_user_works(username: str):
    user = load_user(username)
    works = user.get_works()
    works_details = [work.metadata for work in works]
    return {"username": user.username, 
            "nworks": user.works, 
            "works": works_details}


@router.get("/{username}/bookmarks")
def get_user_bookmarks(username: str):
    user = load_user(username)
    return [bm.metadata for bm in user.get_bookmarks()]  