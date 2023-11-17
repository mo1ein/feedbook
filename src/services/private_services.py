from fastapi import status, APIRouter

from src.logics.feed import FeedLogic
from src.models.feed_model import GetUserFeedsModel, GetUserSourcesModel, SourceModel
from src.models.user_model import UserModel

private_routes = APIRouter()


# @private_routes.get(
#     "/users/{user_id}/feeds",
#     response_model=...,
#     # fix this
#     tags=["FEED_API"],
#     status_code=status.HTTP_201_CREATED
# )
# def get_user_feeds(input_model: UserModel) -> GetUserFeedsModel:
#     return FeedLogic()
#
#
# @private_routes.get(
#     "/users/{user_id}/bookmarks",
#     response_model=...,
#     # fix this
#     tags=["FEED_API"],
#     status_code=status.HTTP_201_CREATED
# )
# def get_user_bookmarks(input_model: UserModel) -> list:
#     return FeedLogic().register(input_model)
#
#
# @private_routes.post(
#     "/users/{user_id}/bookmark",
#     response_model=...,
#     # fix this
#     tags=["FEED_API"],
#     status_code=status.HTTP_201_CREATED
# )
# def bookmark_feed(input_model: UserModel) -> list:
#     return FeedLogic()


@private_routes.get(
    "/users/{user_id}/sources",
    response_model=GetUserSourcesModel,
    # fix this
    tags=["FEED_API"],
    status_code=status.HTTP_200_OK
)
def get_user_sources(user_id: str) -> GetUserSourcesModel:
    user_model = UserModel(user_id=user_id)
    return FeedLogic().get_user_sources(user_model)


@private_routes.post(
    "/users/{user_id}/sources",
    response_model=SourceModel,
    # fix this
    tags=["FEED_API"],
    status_code=status.HTTP_200_OK
)
def add_user_source(user_id:str, url: str) -> None:
    source_model = SourceModel(user_id=user_id, link=url)
    FeedLogic().add_user_source(source_model)
