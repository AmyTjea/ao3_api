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

        metadata = ["works","series","bookmarks","collections","gifts"]

@router.get("/{username}")
def get_user_metadata(username: str):
    # get username, url, avatar, bio,pseuds,join date,userid,bio
    user = User(username)
    return {
        "username": user.username,
        "url": user.url,
        "avatar": user.get_avatar(),
        "bio": user.bio,
        "join_date": user.join_date,
        "id": user.id,
        "pseuds": user.pseuds,
        "n_works":user.nworks,
        "n_bookmarks":user.nbookmarks,
        "n_series":user.nseries,
        "n_collections":user.ncollections,
        "n_gifts":user.ngifts
    }


@router.get("/{username}/works")
def get_user_works(username: str):
    user = load_user(username)
    works = user.get_works()
    works_details = [work.metadata for work in works]
    return {"username": user.username, 
            "nworks": user.nworks, 
            "works": works_details}


@router.get("/{username}/bookmarks")
def get_user_bookmarks(username: str):
    user = load_user(username)
    return [bm.metadata for bm in user.get_bookmarks()]  