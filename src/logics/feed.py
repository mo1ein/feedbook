import feedparser

from src.models.feed_model import GetUserSourcesModel, SourceModel, FeedModel, GetUserFeedsModel, BookmarkModel, \
    GetUserBookmarksModel
from src.models.user_model import UserModel
from src.repositories.repository import Repository
import asyncio

from src.utils.decorators.atomic import atomic


class FeedLogic:
    def __init__(self) -> None:
        self.repository = Repository()

    def get_user_sources(self, input_model: UserModel) -> GetUserSourcesModel:
        return self.repository.get_user_sources(input_model)

    async def _gen_feeds(self, url: str):
        return feedparser.parse(url)['entries']

    async def _get_data(self, input_model: UserModel) -> list:
        sources = self.get_user_sources(input_model)
        sources = sources.user_sources
        urls = [s.link for s in sources]
        tasks = [asyncio.create_task(self._gen_feeds(url)) for url in urls]
        results = await asyncio.gather(*tasks)
        return results

    # @atomic
    def get_user_feeds(self, input_model: UserModel) -> GetUserFeedsModel:
        results = asyncio.run(self._get_data(input_model))
        feeds = []
        feed = results[0][0]
        # for feed in results[0][:1]:
        feed_model = FeedModel(
            user_id=input_model.user_id,
            title=feed['title'],
            link=feed['link'],
            summary=feed['summary'],
            author=feed['author'],
            published=feed['published'],
        )
        # TODO: if not in db??
        created_feed = self.repository.create_feed(feed_model)
        feeds.append(created_feed)
        return GetUserFeedsModel(user_feeds=feeds)

    # Run the main coroutine in the asyncio event loop

    @atomic
    def bookmark_feed(self, input_model: BookmarkModel):
        if self.repository.get_bookmark(input_model) is not None:
            raise ValueError("this feed is bookmarked!")
        if self.repository.get_user_by_id(input_model) is None:
            raise ValueError("this user_id does not exist")
        if self.repository.get_feed(input_model) is None:
            # TODO: better error handling
            raise ValueError("this feed_id does not exist")
        bookmark = self.repository.create_bookmark(input_model)
        return {"bookmark_id": bookmark.bookmark_id}

    @atomic
    def add_user_source(self, input_model: SourceModel) -> SourceModel:
        return self.repository.add_user_source(input_model)


    def get_user_bookmarks(self, input_model: UserModel) -> GetUserFeedsModel:
        return self.repository.get_user_bookmarks(input_model)


if __name__ == "__main__":
    f = FeedLogic()
    user = UserModel(user_id='cf31bd04-f005-4718-9e4c-6119b3014ea5')
    f.get_user_feeds(user)
    # urls = [
    #     'https://waylonwalker.com/rss.xml',
    #     'https://joelhooks.com/rss.xml',
    #     'https://swyx.io/rss.xml',
    #     'http://feeds.arstechnica.com/arstechnica/index/'
    # ]
