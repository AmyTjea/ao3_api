from typing import Union
from fastapi import APIRouter, HTTPException, Query


from app.AO3.users import User
from app.AO3 import utils
from app.api.schemas.users import *
from app.api.schemas.works import WorkMetadata

UserWorks.model_rebuild()

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


@router.get("/{username}", response_model=UserMetadata)
def get_user_metadata(username: str):
    # get username, url, avatar, bio,pseuds,join date,userid,bio
    user = User(username)
    return UserMetadata.model_validate(user)


@router.get("/{username}/works", response_model=UserWorks)
def get_user_works(
    username: str,
    expand: bool = Query(default=False),
):
    user = load_user(username)
    user_works = user.get_works()
    if not expand:
        returned_works = [work.id for work in user_works]
    else:
        returned_works = [
            WorkMetadata.model_validate(work).model_copy(
                update={"authors": [a.username for a in work.authors]}
            )
            for work in user_works
        ]

    return UserWorks(username=user.username, n_works=user.n_works, works=returned_works)


@router.get("/{username}/bookmarks")
def get_user_bookmarks(username: str):
    user = load_user(username)
    return [bm.metadata for bm in user.get_bookmarks()]  