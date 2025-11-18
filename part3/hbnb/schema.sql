-- ================================
-- HBnB DATABASE SCHEMA
-- ================================

-- Enable foreign keys (SQLite compatibility)
PRAGMA foreign_keys = ON;

-- Drop tables if re-running
DROP TABLE IF EXISTS place_amenity;
DROP TABLE IF EXISTS review;
DROP TABLE IF EXISTS amenity;
DROP TABLE IF EXISTS place;
DROP TABLE IF EXISTS user;

-- ================================
-- USER TABLE
-- ================================
CREATE TABLE user (
    id CHAR(36) PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE
);

-- ================================
-- PLACE TABLE
-- ================================
CREATE TABLE place (
    id CHAR(36) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2),
    latitude FLOAT,
    longitude FLOAT,
    owner_id CHAR(36),

    FOREIGN KEY (owner_id) REFERENCES user(id)
);

-- ================================
-- REVIEW TABLE
-- ================================
CREATE TABLE review (
    id CHAR(36) PRIMARY KEY,
    text TEXT,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    user_id CHAR(36) NOT NULL,
    place_id CHAR(36) NOT NULL,

    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (place_id) REFERENCES place(id),

    -- User can review a place only once:
    UNIQUE (user_id, place_id)
);

-- ================================
-- AMENITY TABLE
-- ================================
CREATE TABLE amenity (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL
);

-- ================================
-- PLACE_AMENITY JOIN TABLE
-- ================================
CREATE TABLE place_amenity (
    place_id CHAR(36) NOT NULL,
    amenity_id CHAR(36) NOT NULL,

    PRIMARY KEY (place_id, amenity_id),

    FOREIGN KEY (place_id) REFERENCES place(id)
        ON DELETE CASCADE,

    FOREIGN KEY (amenity_id) REFERENCES amenity(id)
        ON DELETE CASCADE
);
