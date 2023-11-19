CREATE TABLE users
(
    user_id    UUID                                    DEFAULT gen_random_uuid() primary key NOT NULL,
    name       VARCHAR                        NOT NULL,
    last_name  VARCHAR                        NOT NULL,
    email      VARCHAR                        NOT NULL,
    password   VARCHAR                        NOT NULL,
    is_active  BOOL                           NOT NULL,
    created_at TIMESTAMP(6) WITHOUT TIME ZONE NOT NULL DEFAULT transaction_timestamp()
);

CREATE TABLE source
(
    source_id  UUID                                     DEFAULT gen_random_uuid() primary key NOT NULL,
    user_id    UUID REFERENCES users (user_id) NOT NULL,
    link       VARCHAR                         NOT NULL,
    created_at TIMESTAMP(6) WITHOUT TIME ZONE  NOT NULL DEFAULT transaction_timestamp()
);

CREATE TABLE feed
(
    feed_id    UUID                                     DEFAULT gen_random_uuid() primary key,
    user_id    UUID REFERENCES users (user_id) NOT NULL,
    title      VARCHAR                         NOT NULL,
    link       VARCHAR                         NOT NULL,
    summary    VARCHAR                         NOT NULL,
    author     VARCHAR                         NOT NULL,
-- published type can be datetime or sth...
    published  VARCHAR                         NOT NULL,
    created_at TIMESTAMP(6) WITHOUT TIME ZONE  NOT NULL DEFAULT transaction_timestamp()
);

CREATE TABLE bookmark
(
    bookmark_id UUID                                     DEFAULT gen_random_uuid() primary key,
    feed_id     UUID REFERENCES feed (feed_id)  NOT NULL,
    user_id     UUID REFERENCES users (user_id) NOT NULL,
    created_at  TIMESTAMP(6) WITHOUT TIME ZONE  NOT NULL DEFAULT transaction_timestamp(),
    updated_at  TIMESTAMP(6) WITHOUT TIME ZONE
);

-- test data
INSERT INTO public.source (source_id, user_id, link, created_at)
VALUES ('9945b97d-facd-4968-a152-f5284e720685', '4d43e0a5-2bec-439e-bdf1-bfb1239b767a',
        'https://waylonwalker.com/rss.xml', '2023-11-19 14:43:52.168588');
INSERT INTO public.feed (feed_id, user_id, title, link, summary, author, published, created_at)
VALUES ('09e68633-5866-478a-a973-ab21142fef85', '4d43e0a5-2bec-439e-bdf1-bfb1239b767a', 'Heroicons',
        'https://waylonwalker.com//thoughts-161',
        'Here heroicons is a really nice set of many of the basic icons that you will need for building nice ui This post was a thought by',
        'Waylon Walker', '2023-11-14', '2023-11-19 18:45:31.068979');
