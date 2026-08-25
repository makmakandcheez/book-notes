-- BOOKS
-- CREATE TABLE books (
--     id SERIAL PRIMARY KEY,
--     title VARCHAR(255) NOT NULL,
--     author VARCHAR(100) NOT NULL,
--     bk_date_published DATE,
--     rating NUMERIC(3,2),
--     bk_img_url TEXT
-- );
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(255) UNIQUE NOT NULL,
    email  VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW() 
);

CREATE INDEX idx_users_username ON users (username);
CREATE INDEX idx_users_email ON users (email);


CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(100) NOT NULL,
    rating NUMERIC(3,2)
);


-- NOTES
CREATE TABLE notes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(100) NOT NULL,
    body VARCHAR NOT NULL,
    is_public BOOLEAN NOT NULL DEFAULT FALSE,
    date_created TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    date_updated TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    user_id UUID NOT NULL,

    FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);


-- REFRESH-TOKENS
CREATE TABLE refresh_tokens (
    jti UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    token_hash VARCHAR NOT NULL,
    expires_at TIMESTAMPTZ NOT NULL,
    revoked BOOLEAN NOT NULL DEFAULT FALSE,

    FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);


-- BOOKSNOTES (Join Table)
-- CREATE TABLE books_notes (
--     book_id INTEGER NOT NULL,
--     note_id INTEGER NOT NULL,
--     PRIMARY KEY (book_id, note_id),

--     FOREIGN KEY (book_id)
--         REFERENCES books(id)
--         ON DELETE CASCADE,

--     FOREIGN KEY (note_id)
--         REFERENCES notes(id)
--         ON DELETE CASCADE
-- );


-- INDEXES
-- USERS indexes
CREATE INDEX IF NOT EXISTS idx_users_email ON users (email);
CREATE INDEX IF NOT EXISTS idx_users_username ON users (username);

-- BOOKS indexes
CREATE INDEX IF NOT EXISTS idx_books_title ON books (title);
CREATE INDEX IF NOT EXISTS idx_books_author ON books (author);
-- CREATE INDEX IF NOT EXISTS idx_books_date_published ON books (bk_date_published);
CREATE INDEX IF NOT EXISTS idx_books_rating ON books (rating);

-- NOTES indexes
CREATE INDEX idx_notes_title ON notes (title);
CREATE INDEX idx_notes_date_created ON notes (date_created);
CREATE INDEX idx_notes_date_updated ON notes (date_updated);

-- BOOKSNOTES indexes
-- CREATE INDEX idx_booksnotes_book_id ON books_notes (book_id);
-- CREATE INDEX idx_booksnotes_note_id ON books_notes (note_id);