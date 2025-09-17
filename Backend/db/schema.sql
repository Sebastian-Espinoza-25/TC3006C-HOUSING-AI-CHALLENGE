Schema for HouseLink Database
CREATE DATABASE houselink;

-- 1) Clients
CREATE TABLE clients (
    client_id      BIGSERIAL PRIMARY KEY,
    email          VARCHAR(255) NOT NULL UNIQUE,
    username       VARCHAR(100) NOT NULL UNIQUE,
    password       VARCHAR(255) NOT NULL
);

-- 2) Vendors
CREATE TABLE vendors (
    vendor_id      BIGSERIAL PRIMARY KEY,
    email          VARCHAR(255) NOT NULL UNIQUE,
    username       VARCHAR(100) NOT NULL UNIQUE,
    password       VARCHAR(255) NOT NULL
);

-- 3) Client Preferences
-- Each column is a preference related to a house characteristic.
CREATE TABLE client_preferences (
    preference_id  BIGSERIAL PRIMARY KEY,
    client_id      BIGINT NOT NULL REFERENCES clients(client_id) ON DELETE CASCADE
    -- More columns
);

-- 4) Vendor Houses
-- Each column is a characteristic of the house.
CREATE TABLE vendor_houses (
    house_id       BIGSERIAL PRIMARY KEY,
    vendor_id      BIGINT NOT NULL REFERENCES vendors(vendor_id) ON DELETE CASCADE
    -- More columns
);
