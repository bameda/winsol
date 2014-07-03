
-- ROOT USER
CREATE DATABASE winsol;

GRANT ALL ON winsol.* TO user_winsol@localhost IDENTIFIED BY 'pass_winsol';


-- WINSOL USER
USE winsol;

CREATE TABLE _users (
	nick			VARCHAR(20)	NOT NULL,
	password		VARCHAR(40)	NOT NULL,
	mail   			VARCHAR(100)	NOT NULL,
	name			VARCHAR(20),
	surname			VARCHAR(60),
	is_admin   		BOOLEAN   NOT NULL   DEFAULT false,
	PRIMARY KEY (nick)
);

CREATE TABLE _stadistic_app (
	name			VARCHAR(50)	NOT NULL,
	download_number		INT		DEFAULT 0,
	PRIMARY KEY (name)
);

INSERT INTO _users VALUES ("admin", "pass_admin", "admin@email.com", "admin_name", "admin_surname", true);
