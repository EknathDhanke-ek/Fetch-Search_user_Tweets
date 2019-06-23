-- Table: twitter_user_tbl

DROP TABLE IF EXISTS twitter_user_tbl;

CREATE TABLE twitter_user_tbl
(
  tweeter_user_id_pk serial NOT NULL,
  user_nanme text NOT NULL,
  CONSTRAINT twitter_user_tbl_pkey PRIMARY KEY (tweeter_user_id_pk)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE twitter_user_tbl
  OWNER TO postgres;
GRANT ALL ON TABLE twitter_user_tbl TO postgres;

-- Table: user_parking_reservation_tbl

DROP TABLE IF EXISTS user_tweets_tbl;

CREATE TABLE user_tweets_tbl
(
  user_tweet_id_pk serial NOT NULL,
  tweeter_user_id_fk integer NOT NULL,
  tweet_id  bigint NOT NULL,
  language text,
  tweet_text text,
  CONSTRAINT user_tweets_tbl_pkey PRIMARY KEY (user_tweet_id_pk),
  CONSTRAINT user_tweets_tbl_uniqkey UNIQUE (tweet_id),
  CONSTRAINT user_tweets_tbl_parking_tweeter_user_id_fkey FOREIGN KEY (tweeter_user_id_fk)
      REFERENCES twitter_user_tbl (tweeter_user_id_pk) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE user_tweets_tbl
  OWNER TO postgres;
GRANT ALL ON TABLE user_tweets_tbl TO postgres;




