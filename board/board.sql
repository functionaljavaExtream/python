create table webboard (
    id int NOT NULL AUTO_INCREMENT primary key,
    title varchar(200) not null DEFAULT '',
    writer varchar(256) not null DEFAULT '',
    FOREIGN KEY (writer) REFERENCES user(username) ON UPDATE CASCADE,
    regdate datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    content text not null
)