from src.logics.feed import FeedLogic
from src.models.feed_model import GetUserSourcesModel, SourceModel, GetUserFeedsModel, FeedModel, BookmarkModel
from src.models.user_model import UserModel

feed_logic = FeedLogic()


def test_get_user_sources():
    user_model = UserModel(user_id='680813d9-ecec-4a60-970d-d34af9e398a6')
    source_model = SourceModel(
        source_id="fc9c3efd-cf90-44c8-9b24-cf5e812be080",
        user_id="680813d9-ecec-4a60-970d-d34af9e398a6",
        link="https://waylonwalker.com/rss.xml",
        created_at="2023-11-19 22:09:58.802881"
    )
    expected = GetUserSourcesModel(user_sources=[source_model])
    output = feed_logic.get_user_sources(user_model)
    assert expected == output


def test_get_user_feeds():
    user_model = UserModel(user_id='680813d9-ecec-4a60-970d-d34af9e398a6')
    expected = GetUserFeedsModel(
        user_feeds=[
            FeedModel(
                feed_id="12be95b4-dd52-4678-813c-1449dee0876e",
                user_id="680813d9-ecec-4a60-970d-d34af9e398a6",
                title="Heroicons",
                link="https://waylonwalker.com//thoughts-161",
                summary="Here heroicons is a really nice set of many of the basic icons that you will need for building nice ui This post was a thought by",
                published="2023-11-14",
                created_at="2023-11-20 01:33:09.462111"
            ),
            FeedModel(
                feed_id="0a694362-4d55-4e37-94be-2b6c95507a9b",
                user_id="680813d9-ecec-4a60-970d-d34af9e398a6",
                title="Uptime Kuma",
                link="https://waylonwalker.com//thoughts-160",
                summary="Here Uptime kuma is a fantastic self hosted monitoring tool.  One docker run command and you are up and running.  Once you are in you have full control over che",
                published="2023-11-11",
                created_at="2023-11-19 22:30:38.248052"
            ),

        ]
    )
    output = feed_logic.get_user_feeds(user_model, posts_num=2)
    assert expected == output


def test_bookmark_feed():
    bookmark_model = BookmarkModel(
        user_id='680813d9-ecec-4a60-970d-d34af9e398a6',
        feed_id='0a694362-4d55-4e37-94be-2b6c95507a9b'
    )
    expected_user_id = bookmark_model.user_id
    expected_feed_id = bookmark_model.feed_id
    output = feed_logic.bookmark_feed(bookmark_model)
    assert expected_user_id == output.user_id
    assert expected_feed_id == output.feed_id


def test_add_user_source():
    source_model = SourceModel(
        user_id="680813d9-ecec-4a60-970d-d34af9e398a6",
        link="https://news.ycombinator.com/rss",
    )
    expected_link = source_model.link
    expected_user_id = source_model.user_id
    output = feed_logic.add_user_source(source_model)
    assert expected_link == output.link
    assert expected_user_id == output.user_id
