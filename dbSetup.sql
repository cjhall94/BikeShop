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
                    image text DEFAULT 'Default.jpg',
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
INSERT INTO items (name, description, category, retailPrice, salesPrice, specifications, reviews, 
    manufacturer, stock, rating, stockLimit) 
    VALUES('Wheel', 'Its round', 'parts', 14.95, 10.78, 'Circular', 'It goes round and round', 'Infinate Loop', 2, 5, 6 );
INSERT INTO items (name, description, category, retailPrice, salesPrice, specifications, reviews, 
    manufacturer, stock, rating, stockLimit) 
    VALUES('Handle Bars', 'You hold them', 'parts', 56.95, 0.78, 'Handy', 'Handles like a dream', 'Hang On', 15, 78, 6 );
INSERT INTO items (name, description, category, retailPrice, salesPrice, specifications, reviews, 
    manufacturer, stock, rating, stockLimit) 
    VALUES('Gears', 'They are spikey', 'parts', 0.95, 10.78, 'You need them', 'The kept me going.', 'Gears 4 You', 34, 25, 8 );
    
DROP TABLE IF EXISTS blog;
CREATE TABLE blogs (
  blog varchar(1000000)  NOT NULL default '',
  title varchar (1000),
  author varchar(100) NOT NULL);

INSERT INTO blogs (blog, title, author) VALUES ('I bought a Trek Marlin today, after much deliberation and research. I needed a bike I could take anywhere and hoon around with, and I had a budget of ~$650.
I made a post here that helped me decide; Huge thanks to everyone for helping me understand what to look for in a hardtail. Ive only ever ridden cheap walmart bikes my whole life, and this bike is a world away from anything Ive touched before. I chose this bike over the other suggestions because I really wanted to support my local bike shop as much as possible, and the other options werent available there.
Ive left this bike stock as Ive only had it for a day, but Im looking into upgrading the front fork to fox/rockshox in the near future. I do a bit of everything, with a fair amount of my riding occurring on very poorly paved roads, with some off-road shortcuts and exploration rides in between.
One thing that stood out to me with the advice I received was a lot of stay away from x or dont get anything below y, but if youve only ridden cheap, shoddy walmart bikes, anything even at the base of entry-level will blow you away. I wouldnt change anything about this bike at this price point. I love it. Thanks everyone for getting me into the world of nice bikes.', 'New Bike Day! Trek Marlin 6', 'Sam Smith');
