create table fileupload (
    id int NOT NULL AUTO_INCREMENT primary key,
    boardId varchar(256) not null DEFAULT '',
    FOREIGN KEY (boardId) REFERENCES webboard(id) ON UPDATE CASCADE,

)