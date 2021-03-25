DELIMITER //
CREATE  TRIGGER auto_increse_replycount
AFTER INSERT
ON boardreply
FOR EACH ROW
BEGIN
UPDATE webboard SET replycount = replycount +1 WHERE webboard.id = new.boardId;
END//
DELIMITER ;