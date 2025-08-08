
-- Step 1: Create Floor table
CREATE TABLE IF NOT EXISTS cis2368summerdb.floor (
    id INT AUTO_INCREMENT PRIMARY KEY,
    level INT NOT NULL,
    name VARCHAR(100) NOT NULL
);

-- Step 2: Create Room table AFTER Floor
CREATE TABLE IF NOT EXISTS cis2368summerdb.room (
    id INT AUTO_INCREMENT PRIMARY KEY,
    capacity INT NOT NULL,
    number INT NOT NULL,
    floor INT NOT NULL,
    FOREIGN KEY (floor) REFERENCES floor(id) ON DELETE CASCADE
);

-- Step 3: Create Resident table AFTER Room
CREATE TABLE IF NOT EXISTS cis2368summerdb.resident (
    id INT AUTO_INCREMENT PRIMARY KEY,
    firstname VARCHAR(100) NOT NULL,
    lastname VARCHAR(100) NOT NULL,
    age INT NOT NULL,
    room INT NOT NULL,
    FOREIGN KEY (room) REFERENCES cis2368summerdb.room(id) ON DELETE CASCADE
);