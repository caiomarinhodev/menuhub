DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS menu;

CREATE TABLE user
(
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    username varchar(255) NOT NULL,
    password varchar(255) NOT NULL,
    email    varchar(255),
    role     varchar(255),
);

CREATE TABLE menu
(
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    author_id   INTEGER      NOT NULL,
    created     TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title       varchar(255) NOT NULL,
    name        varchar(255),
    price       int(11),
    description varchar(255),
    image       varchar(255),
    FOREIGN KEY (author_id) REFERENCES user (id),
);