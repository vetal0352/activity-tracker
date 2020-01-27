DROP TABLE if exists 'activity';

CREATE TABLE 'activity' (
	'id' integer PRIMARY KEY AUTOINCREMENT NOT NULL, 
	'start_time' time NOT NULL, 
	'finish_time' time NOT NULL, 
	'distance' real NOT NULL, 
	'activity_type' varchar(4) NOT NULL, 
	'activity_date' date NOT NULL DEFAULT CURRENT_DATE
);
