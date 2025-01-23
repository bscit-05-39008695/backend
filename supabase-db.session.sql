
CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL PRIMARY KEY,
    email VARCHAR(555) NOT NULL,
    password VARCHAR(255) NOT NULL
);

INSERT INTO users (email, password) VALUES ('J2QlS@example.com', 'password');
