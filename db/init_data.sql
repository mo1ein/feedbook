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
INSERT INTO public.users (user_id, name, last_name, email, password, is_active, created_at) VALUES ('680813d9-ecec-4a60-970d-d34af9e398a6', 'moein', 'halvaei', 'x@x.com', '$pbkdf2-sha256$29000$wPj/XyvFGCOEcE4JAeBcyw$9UYgMqdmkPHATahsA20Eql74Mp6uHGs76F4s3Dy.Syk', true, '2023-11-19 22:07:43.728438');
INSERT INTO public.feed (feed_id, user_id, title, link, summary, published, created_at) VALUES ('0a694362-4d55-4e37-94be-2b6c95507a9b', '680813d9-ecec-4a60-970d-d34af9e398a6', 'Uptime Kuma', 'https://waylonwalker.com//thoughts-160', 'Here Uptime kuma is a fantastic self hosted monitoring tool.  One docker run command and you are up and running.  Once you are in you have full control over che', '2023-11-11', '2023-11-19 22:30:38.248052');
INSERT INTO public.feed (feed_id, user_id, title, link, summary, published, created_at) VALUES ('87e9774e-71d0-4c54-8c12-c07acf396058', '680813d9-ecec-4a60-970d-d34af9e398a6', 'Kv - Command | Vault | Hashicorp Developer', 'https://waylonwalker.com//thoughts-158', 'Here hashi vault lets you manage secrets right from your cli. This post was a thought by', '2023-11-05', '2023-11-19 22:30:38.248052');
INSERT INTO public.feed (feed_id, user_id, title, link, summary, published, created_at) VALUES ('52c3b9d2-83f8-4352-9456-8646d5bacbbc', '680813d9-ecec-4a60-970d-d34af9e398a6', 'Johanhaleby/Kubetail: Bash Script To Tail Kubernetes Logs From Multiple Pods At The Same Time', 'https://waylonwalker.com//thoughts-157', 'Here Kubetail is a pretty sick bash script that allows you to tail logs for multiple pods in one stream.  Very handy when you have more than one replica running', '2023-10-31', '2023-11-19 22:30:38.248052');
INSERT INTO public.feed (feed_id, user_id, title, link, summary, published, created_at) VALUES ('eeea2588-9937-4c1a-9aef-a55c683337d5', '680813d9-ecec-4a60-970d-d34af9e398a6', 'Waylon Walker 🐍 On X: "Which Is More Complicated" / X', 'https://waylonwalker.com//thoughts-155', 'Here Wow, shocked at these results.  All this time I This post was a thought by', '2023-10-30', '2023-11-19 22:30:38.248052');
INSERT INTO public.feed (feed_id, user_id, title, link, summary, published, created_at) VALUES ('12be95b4-dd52-4678-813c-1449dee0876e', '680813d9-ecec-4a60-970d-d34af9e398a6', 'Heroicons', 'https://waylonwalker.com//thoughts-161', 'Here heroicons is a really nice set of many of the basic icons that you will need for building nice ui This post was a thought by', '2023-11-14', '2023-11-20 01:33:09.462111');
INSERT INTO public.source (source_id, user_id, link, created_at) VALUES ('fc9c3efd-cf90-44c8-9b24-cf5e812be080', '680813d9-ecec-4a60-970d-d34af9e398a6', 'https://waylonwalker.com/rss.xml', '2023-11-19 22:09:58.802881');
INSERT INTO public.bookmark (bookmark_id, feed_id, user_id, created_at, updated_at) VALUES ('e7fde5db-c032-425c-9eb0-633690823b64', '0a694362-4d55-4e37-94be-2b6c95507a9b', '680813d9-ecec-4a60-970d-d34af9e398a6', '2023-11-19 22:32:31.986783', null);
