CREATE TABLE users
(
    id         UUID DEFAULT gen_random_uuid() primary key NOT NULL,
    email      VARCHAR                                    NOT NULL,
    password   VARCHAR                                    NOT NULL,
    created_at TIMESTAMP(6) WITHOUT TIME ZONE NOT NULL DEFAULT transaction_timestamp()
);
