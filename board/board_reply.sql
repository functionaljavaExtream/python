create table boardreply (
    id int NOT NULL AUTO_INCREMENT primary key,
    boardId int NOT NULL,
    FOREIGN KEY (boardId) REFERENCES webboard(id) ON UPDATE CASCADE,
    replywriter varchar(256) not null DEFAULT '',
    FOREIGN KEY (replywriter) REFERENCES user(username) ON UPDATE CASCADE,
    regdate datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    replycontent text not null
);