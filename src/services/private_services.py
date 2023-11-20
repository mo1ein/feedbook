from fastapi import status, APIRouter

from src.logics.feed import FeedLogic
from src.models.feed_model import (
    GetUserFeedsModel,
    GetUserSourcesModel,
    SourceModel,
    BookmarkModel
)

from src.models.service_enum import ServiceType
from src.models.user_model import UserModel

private_routes = APIRouter()


@private_routes.get(
    "/users/{user_id}/feeds",
    response_model=GetUserFeedsModel,
    tags=[ServiceType.FEED_API],
    status_code=status.HTTP_200_OK
)
def get_user_feeds(user_id: str) -> GetUserFeedsModel:
    user_model = UserModel(user_id=user_id)
    return FeedLogic().get_user_feeds(user_model)


@private_routes.get(
    "/users/{user_id}/sources",
    response_model=GetUserSourcesModel,
    tags=[ServiceType.FEED_API],
    status_code=status.HTTP_200_OK
)
def get_user_sources(user_id: str) -> GetUserSourcesModel:
    user_model = UserModel(user_id=user_id)
    return FeedLogic().get_user_sources(user_model)


@private_routes.post(
    "/users/{user_id}/sources",
    response_model=SourceModel,
    tags=[ServiceType.FEED_API],
    status_code=status.HTTP_201_CREATED
)
def add_user_source(user_id: str, url: str) -> SourceModel:
    source_model = SourceModel(user_id=user_id, link=url)
    return FeedLogic().add_user_source(source_model)


@private_routes.get(
    "/users/{user_id}/bookmarks",
    response_model=GetUserFeedsModel,
    tags=[ServiceType.FEED_API],
    status_code=status.HTTP_200_OK
)
def get_user_bookmarks(user_id: str) -> GetUserFeedsModel:
    user_model = UserModel(user_id=user_id)
    return FeedLogic().get_user_bookmarks(user_model)


@private_routes.post(
    "/users/{user_id}/bookmark",
    response_model=BookmarkModel,
    tags=[ServiceType.FEED_API],
    status_code=status.HTTP_201_CREATED
)
def bookmark_feed(user_id: str, feed_id: str) -> BookmarkModel:
    bookmark_model = BookmarkModel(user_id=user_id, feed_id=feed_id)
    return FeedLogic().bookmark_feed(bookmark_model)
