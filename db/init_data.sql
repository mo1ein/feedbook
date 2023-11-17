CREATE TABLE users
(
    user_id    UUID                                    DEFAULT gen_random_uuid() primary key NOT NULL,
    email      VARCHAR                        NOT NULL,
    password   VARCHAR                        NOT NULL,
    is_active  BOOL                           NOT NULL,
    created_at TIMESTAMP(6) WITHOUT TIME ZONE NOT NULL DEFAULT transaction_timestamp()
);

CREATE TABLE source
(
    source_id  UUID                                    DEFAULT gen_random_uuid() primary key NOT NULL,
    user_id    UUID                           NOT NULL,
    link       VARCHAR                        NOT NULL,
    created_at TIMESTAMP(6) WITHOUT TIME ZONE NOT NULL DEFAULT transaction_timestamp()
);

CREATE TABLE feed
(
    feed_id    UUID                                    DEFAULT gen_random_uuid() primary key,
    title      VARCHAR                        NOT NULL,
    link       VARCHAR                        NOT NULL,
    summary    VARCHAR                        NOT NULL,
    author     VARCHAR                        NOT NULL,
-- published type can be datetime or sth...
    published  VARCHAR                        NOT NULL,
    created_at TIMESTAMP(6) WITHOUT TIME ZONE NOT NULL DEFAULT transaction_timestamp()
);

CREATE TABLE bookmark
(
    bookmark_id UUID                                    DEFAULT gen_random_uuid() primary key,
    feed_id     UUID                           NOT NULL,
    user_id     UUID                           NOT NULL,
    created_at  TIMESTAMP(6) WITHOUT TIME ZONE NOT NULL DEFAULT transaction_timestamp(),
    updated_at  TIMESTAMP(6) WITHOUT TIME ZONE
);
