create table uploadfiles (
    id int NOT NULL AUTO_INCREMENT primary key,
    boardId varchar(256) not null DEFAULT '',
    FOREIGN KEY (boardId) REFERENCES webboard(id) ON UPDATE CASCADE,
    writer varchar(256) not null DEFAULT '',
    FOREIGN KEY (writer) REFERENCES user(username) ON UPDATE CASCADE,
    regdate datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    content text not null
)