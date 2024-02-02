USE dinosaurs;

CREATE TABLE IF NOT EXISTS Name (
    name VARCHAR(100) UNIQUE,
    pronunciation VARCHAR(100), 
    meaning VARCHAR(255),
    PRIMARY KEY (name)
);

CREATE TABLE IF NOT EXISTS Type (
    type_id INTEGER AUTO_INCREMENT,
    type_name VARCHAR(255) UNIQUE,
    PRIMARY KEY (type_id)
);

CREATE TABLE IF NOT EXISTS Diet (
    diet_id INTEGER AUTO_INCREMENT,
    diet_name VARCHAR(255) UNIQUE,
    PRIMARY KEY (diet_id)
);

CREATE TABLE IF NOT EXISTS Era (
    era_id INTEGER AUTO_INCREMENT,
    era_name VARCHAR(255) UNIQUE,
    PRIMARY KEY (era_id)
);

CREATE TABLE IF NOT EXISTS Country (
    country_id INTEGER AUTO_INCREMENT,
    country_name VARCHAR(255) UNIQUE,
    PRIMARY KEY (country_id)
);

CREATE TABLE IF NOT EXISTS Dinosaur (
    id INTEGER AUTO_INCREMENT,
    size DOUBLE,
    image VARCHAR(255),
    discovered INTEGER,
    description VARCHAR(1000),
    name VARCHAR(100) UNIQUE,
    type_id INTEGER,
    diet_id INTEGER,
    era_id INTEGER,
    country_id INTEGER,
    created_at TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (name) REFERENCES Name(name),
    FOREIGN KEY (type_id) REFERENCES Type(type_id),
    FOREIGN KEY (diet_id) REFERENCES Diet(diet_id),
    FOREIGN KEY (era_id) REFERENCES Era(era_id),
    FOREIGN KEY (country_id) REFERENCES Country(country_id)
);