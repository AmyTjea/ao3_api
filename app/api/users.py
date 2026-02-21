from typing import Union
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from datetime import date

from app.AO3.users import User
from app.AO3 import utils

router = APIRouter()

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

# TODO: Define Series api endpoint and put in series metadata
#TODO: MANAGE BASE MODELS
# class Bookmark(BaseModel):

#     id:int
#     bookmarker: Union[str, UserMetadata]
#     bookmark: Union[WorkMetadata]#,SeriesMetadata]



def load_user(username: str) -> User:
    try:
        return User(username)
    except utils.InvalidIdError:
        raise HTTPException(status_code=404, detail="User not found")
    except utils.HTTPError as e:
        raise HTTPException(status_code=429, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{username}",response_model=UserMetadata)
def get_user_metadata(username: str):
    # get username, url, avatar, bio,pseuds,join date,userid,bio
    user = User(username)
    return UserMetadata.from_orm(user)


@router.get("/{username}/works")
def get_user_works(username: str,include:str|None = Query(default=None),):
    user = load_user(username)
    works = user.get_works()
    works_details = [work.metadata for work in works]
    return {"username": user.username, 
            "n_works": user.nworks, 
            "works": works_details}


@router.get("/{username}/bookmarks")
def get_user_bookmarks(username: str):
    user = load_user(username)
    return [bm.metadata for bm in user.get_bookmarks()]  