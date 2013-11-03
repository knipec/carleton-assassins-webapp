CREATE TABLE allkills (
killed int,
killer int,
time int,
deathcause int,
term int,
round int,
location int,
winner int
);

CREATE TABLE players (
id int,
player text
);

CREATE TABLE deathcauses (
id int,
deathcause text
);

CREATE TABLE terms (
id int,
term text
);

CREATE TABLE rounds (
id int,
round text
);

CREATE TABLE locations (
id int,
location text
);


