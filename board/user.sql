create table user (
    id int NOT NULL AUTO_INCREMENT primary key,
    username varchar(256) not null UNIQUE,
    userpassword varchar(256) not null,
    usermail varchar(256) not null DEFAULT '',
    regdate datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
)