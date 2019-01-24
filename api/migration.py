import os
from passlib.handlers.pbkdf2 import pbkdf2_sha256

LATEST_VERSION = 2

SCHEMA = {
    2: {
        'up': [
            ["""
                CREATE TABLE users(
                 id BIGSERIAL PRIMARY KEY,
                 email VARCHAR (64) UNIQUE NOT NULL,
                 password TEXT NOT NULL                 
                );"""
             ],
            ["INSERT INTO users (email, password) values ($1, $2)",
                os.getenv('API_ADMIN_EMAIL'),
                pbkdf2_sha256.hash(os.getenv('API_ADMIN_PASSWORD'))
             ],
            ["CREATE INDEX idx_users_email ON users(email);"],
        ],
        'down': [
            ["DROP INDEX idx_users_email"],
            ["DROP TABLE users;"],
        ]
    },
    1: {
        'up': [
            ["CREATE TABLE versions( id integer NOT NULL);"],
            ["INSERT INTO versions VALUES ($1);", 1]
        ],
        'down': [
            ["DROP TABLE versions;"],
        ]
    }
}
