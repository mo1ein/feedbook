import feedparser

from src.models.feed_model import GetUserSourcesModel, SourceModel
from src.models.user_model import UserModel
from src.repositories.repository import Repository
import asyncio

from src.utils.decorators.atomic import atomic


# urls = [
#     'https://waylonwalker.com/rss.xml',
#     'https://joelhooks.com/rss.xml',
#     'https://swyx.io/rss.xml',
#     'http://feeds.arstechnica.com/arstechnica/index/'
# ]


class FeedLogic:
    def __init__(self) -> None:
        self.repository = Repository()

    def get_user_sources(self, input_model: UserModel) -> GetUserSourcesModel:
        return self.repository.get_user_sources(input_model)

    async def _gen_feeds(self, url: str):
        return feedparser.parse(url)['entries']

    async def get_user_feeds(self, input_model: UserModel):
        sources = self.get_user_sources(input_model)
        sources = sources.user_sources
        urls = [s.link for s in sources]
        tasks = [asyncio.create_task(self._gen_feeds(url)) for url in urls]
        results = await asyncio.gather(*tasks)
        print(results)

    # Run the main coroutine in the asyncio event loop

    def bookmark_feed(self):
        ...

    @atomic
    def add_user_source(self, input_model: SourceModel) -> None:
        self.repository.add_user_source(input_model)


if __name__ == "__main__":
    # a = feeds[0][0]
    # print(a['title'], a['link'], a['summary'], a['author'], a['published'])
    f = FeedLogic()
    user = UserModel(user_id='92b32fdd-8dd9-492c-91f4-593e6cf793b7')
    # f.get_feeds(user)
    asyncio.run(f.get_user_feeds(user))
