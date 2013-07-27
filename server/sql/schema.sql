CREATE TABLE user (
	id integer primary key AUTOINCREMENT,
	username varchar(16) not null,
	name varchar(16) not null,
	balance decimal(10,5) not null default 0,
	is_active boolean not null default false,
	UNIQUE(username)
);
CREATE TABLE credit_card (
	id integer primary key AUTOINCREMENT,
	user_id integer not null,
	card_number varchar(19) not null,
	is_validated boolean not null default false,
	is_active boolean not null default false,
	UNIQUE(card_number),
	FOREIGN KEY(user_id) REFERENCES user(id)
);
CREATE TABLE user_payment (
	id integer primary key AUTOINCREMENT,
	date datetime not null default CURRENT_TIMESTAMP, 
	actor_user_id integer not null,
	target_user_id integer not null,
	amount decimal(10,5) not null, 
	note text,
	FOREIGN KEY(actor_user_id) REFERENCES user(id),
	FOREIGN KEY(target_user_id) REFERENCES user(id)
);
CREATE TABLE credit_card_transaction (
	id integer primary key AUTOINCREMENT,
	date datetime not null default CURRENT_TIMESTAMP,
	user_id integer not null,
	credit_card_id integer not null,
	amount decimal(10,5) not null,
	is_success boolean not null default false,
	transaction_id varchar(256) not null,
	boolean is_successful not null default false,
	FOREIGN KEY(user_id) REFERENCES user(id),
	FOREIGN KEY(credit_card_id) REFERENCES credit_card(id)
);
