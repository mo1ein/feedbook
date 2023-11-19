import feedparser
from fastapi import HTTPException

from src.configs.runtime_config import RuntimeConfig
from src.models.feed_model import GetUserSourcesModel, SourceModel, FeedModel, GetUserFeedsModel, BookmarkModel, \
    GetUserBookmarksModel
from src.models.user_model import UserModel
from src.repositories.repository import Repository
import asyncio

from src.utils.configs import Configuration
from src.utils.decorators.atomic import atomic


class FeedLogic:
    def __init__(self) -> None:
        self.repository = Repository()

    @atomic
    def get_user_sources(self, input_model: UserModel) -> GetUserSourcesModel:
        return self.repository.get_user_sources(input_model)

    @atomic
    async def _gen_feeds(self, url: str):
        return feedparser.parse(url)['entries']


    async def _get_data(self, input_model: UserModel) -> list:
        sources = self.get_user_sources(input_model)
        sources = sources.user_sources
        urls = [s.link for s in sources]
        tasks = [asyncio.create_task(self._gen_feeds(url)) for url in urls]
        results = await asyncio.gather(*tasks)
        return results

    @atomic
    def get_user_feeds(self, input_model: UserModel) -> GetUserFeedsModel:
        results = asyncio.run(self._get_data(input_model))
        feeds = []
        # last 5 feeds
        for feed in results[0][:5]:
            feed_model = FeedModel(
                user_id=input_model.user_id,
                title=feed['title'],
                link=feed['link'],
                summary=feed['summary'],
                author=feed['author'],
                published=feed['published'],
            )
            if (feed_response := self.repository.is_exist_feed(feed_model)) is None:
                created_feed = self.repository.create_feed(feed_model)
                feeds.append(created_feed)
            else:
                feeds.append(feed_response)
        return GetUserFeedsModel(user_feeds=feeds)

    @atomic
    def bookmark_feed(self, input_model: BookmarkModel):
        if self.repository.get_bookmark(input_model) is not None:
            raise HTTPException(status_code=409, detail="this feed is bookmarked!")
        if self.repository.get_user_by_id(input_model) is None:
            raise HTTPException(status_code=409, detail="this user_id does not exist")
        if self.repository.get_feed(input_model) is None:
            raise HTTPException(status_code=409, detail="this feed_id does not exist")
        bookmark = self.repository.create_bookmark(input_model)
        return {"bookmark_id": bookmark.bookmark_id}

    @atomic
    def add_user_source(self, input_model: SourceModel) -> SourceModel:
        return self.repository.add_user_source(input_model)


    def get_user_bookmarks(self, input_model: UserModel) -> GetUserFeedsModel:
        return self.repository.get_user_bookmarks(input_model)


if __name__ == "__main__":
    f = FeedLogic()
    # Configuration.apply(RuntimeConfig, alternative_env_search_dir=__file__)
    user = UserModel(user_id='4d43e0a5-2bec-439e-bdf1-bfb1239b767a')
    f.get_user_feeds(user)
    # urls = [
    #     'https://waylonwalker.com/rss.xml',
    #     'https://joelhooks.com/rss.xml',
    #     'https://swyx.io/rss.xml',
    #     'http://feeds.arstechnica.com/arstechnica/index/'
    # ]
