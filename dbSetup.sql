DROP DATABASE IF EXISTS bikesdb;
CREATE DATABASE  bikesdb;
\c bikesdb;
CREATE EXTENSION pgcrypto;

DROP TABLE IF EXISTS items;
CREATE TABLE items (    
                    ID serial NOT NULL,
                    name text,
                    UNIQUE(name),
                    description varchar,
                    category varchar,
                    retailPrice float,
                    salesPrice float,
                    specifications varchar,
                    reviews varchar,
                    manufacturer varchar,
                    stock int,
                    rating int,
                    stockLimit int,
                    PRIMARY KEY  (ID)
                    );

DROP TABLE IF EXISTS users;                        
CREATE TABLE users (        
                    email VARCHAR(32) NOT NULL,
                    PRIMARY KEY(email),
                    firstName VARCHAR(32) NOT NULL DEFAULT 'John',
                    lastName VARCHAR(32) NOT NULL DEFAULT 'Doe',
                    password VARCHAR(64) NOT NULL
                    );
                            

 
                            
                            
INSERT INTO users VALUES('ecooper@umw.edu','Gusty', 'Cooper', crypt('1', gen_salt('bf')));                            
INSERT INTO users VALUES('tempEmail@yahoo.com', 'Johnny', 'Boy', crypt('1', gen_salt('bf')));
INSERT INTO items (name, description, category, retailPrice, salesPrice, specifications, reviews, 
    manufacturer, stock, rating, stockLimit) 
    VALUES('Seat', 'Its a seat', 'parts', 10.95, 11.95, 'Fits most butts', 'Feels like heaven', 'ButtsRUs', 4, 3, 6 );