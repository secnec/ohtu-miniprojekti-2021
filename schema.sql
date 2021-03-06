CREATE TABLE users(id SERIAL PRIMARY KEY, username TEXT UNIQUE, password TEXT);
CREATE TABLE tips(id SERIAL PRIMARY KEY, username TEXT, title TEXT, url TEXT, visible BOOLEAN DEFAULT True, likes INTEGER DEFAULT 0);
CREATE TABLE likes(id SERIAL PRIMARY KEY, user_id INTEGER, tip_id INTEGER);
