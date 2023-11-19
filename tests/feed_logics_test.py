from src.logics.feed import FeedLogic
from src.models.feed_model import GetUserSourcesModel, SourceModel
from src.models.user_model import UserModel

feed_logic = FeedLogic()


def test_get_user_sources():
    user_model = UserModel(user_id='4d43e0a5-2bec-439e-bdf1-bfb1239b767a')
    source_model = SourceModel(
        source_id="9945b97d-facd-4968-a152-f5284e720685",
        user_id="4d43e0a5-2bec-439e-bdf1-bfb1239b767a",
        link="https://waylonwalker.com/rss.xml",
        created_at="2023-11-19 14:43:52.168588"
    )
    expected = GetUserSourcesModel(user_sources=[source_model])
    output = feed_logic.get_user_sources(user_model)
    assert expected == output
    # TODO: write wrong test


def test_get_user_feeds():
    ...


def test_bookmark_feed():
    ...


def test_add_user_source():
    ...
