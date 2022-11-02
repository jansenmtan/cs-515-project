/* TURNS OUT THE ORIGINAL IS IN MSSQL!!!!! NOT MYSQL!!!!!!!! */

DROP DATABASE IF EXISTS cs_515_project;

CREATE DATABASE cs_515_project;

USE cs_515_project;

/* The following four SQL queries are used to initialize the database tables: */
CREATE TABLE Customer
(cid INTEGER NOT NULL AUTO_INCREMENT
		PRIMARY KEY,
	cname CHAR(80) NOT NULL,
	email CHAR(40) NOT NULL, UNIQUE (email),
	address CHAR(200),
	password CHAR(16) NOT NULL
) AUTO_INCREMENT = 1;

CREATE TABLE City
(cityid INTEGER NOT NULL AUTO_INCREMENT
		PRIMARY KEY,
	title CHAR(50) NOT NULL,
	state CHAR(2) NOT NULL
) AUTO_INCREMENT = 0;

CREATE TABLE Flight
(fid INTEGER NOT NULL AUTO_INCREMENT
		PRIMARY KEY,
	fnumber INTEGER,
	fdate DATE NOT NULL,
	ftime TIME NOT NULL,
	price REAL NOT NULL,
	class INTEGER NOT NULL,
	capacity INTEGER NOT NULL,
	available INTEGER NOT NULL,
	orig INTEGER NOT NULL,
	dest INTEGER NOT NULL,
	FOREIGN KEY (orig) REFERENCES City (cityid) ON DELETE CASCADE,
	FOREIGN KEY (dest) REFERENCES City (cityid) ON DELETE CASCADE
) AUTO_INCREMENT = 0;

CREATE TABLE Reservation
(ordernum INTEGER NOT NULL AUTO_INCREMENT
		PRIMARY KEY,
	cid INTEGER NOT NULL,
	dfid INTEGER NOT NULL,
	rfid INTEGER,
	qty INTEGER NOT NULL,
	cardnum CHAR(16) NOT NULL,
	cardmonth INTEGER NOT NULL,
	cardyear INTEGER NOT NULL,
	order_date DATE,
	FOREIGN KEY (cid) REFERENCES Customer (cid) ON DELETE CASCADE,
	FOREIGN KEY (dfid) REFERENCES Flight (fid) ON DELETE CASCADE,
	FOREIGN KEY (rfid) REFERENCES Flight (fid) ON DELETE CASCADE
) AUTO_INCREMENT = 1;


/* The following three SQL queries are used to initialize the database triggers: */
/* // After a reservation is created, this trigger sets the order date */
CREATE TRIGGER reservation_date
   	AFTER INSERT ON Reservation
   	FOR EACH ROW
   		UPDATE Reservation
   		SET order_date = CURRENT_DATE
   		WHERE ordernum=NEW.ordernum;

/* // After an reservation is created, update the number
   // of tickets available for the departure flight */
CREATE TRIGGER reservation_davail
   	AFTER INSERT ON Reservation
   	FOR EACH ROW
   		UPDATE Flight X
   		SET available = ((SELECT available
   			FROM Flight F
   			WHERE F.fid=NEW.dfid)-NEW.qty)
   		WHERE X.fid=NEW.dfid;

/* // After an reservation is created, update the number
   // of tickets available for the return flight */
CREATE TRIGGER reservation_ravail
   	AFTER INSERT ON Reservation
   	FOR EACH ROW
   		UPDATE Flight X
   		SET available = ((SELECT available
   			FROM Flight F
   			WHERE F.fid=NEW.rfid)-NEW.qty)
   		WHERE X.fid=NEW.rfid;

