-- BOOKS
-- CREATE TABLE books (
--     bk_id SERIAL PRIMARY KEY,
--     bk_title VARCHAR(255) NOT NULL,
--     bk_author VARCHAR(100) NOT NULL,
--     bk_date_published DATE,
--     bk_rating NUMERIC(3,2),
--     bk_img_url TEXT
-- );
CREATE TABLE users (
    usr_id SERIAL PRIMARY KEY,
    usr_username VARCHAR(255) UNIQUE NOT NULL,
    usr_email  VARCHAR(255) UNIQUE NOT NULL,
    usr_hashed_password VARCHAR(255)
);


CREATE TABLE books (
    bk_id SERIAL PRIMARY KEY,
    bk_title VARCHAR(255) NOT NULL,
    bk_author VARCHAR(100) NOT NULL,
    bk_rating NUMERIC(3,2)
);


-- NOTES
CREATE TABLE notes (
    nt_id SERIAL PRIMARY KEY,
    nt_title VARCHAR(100) NOT NULL,
    nt_body TEXT NOT NULL,
    nt_date_created TIMESTAMP NOT NULL DEFAULT NOW(),
    nt_date_updated TIMESTAMP NOT NULL DEFAULT NOW()
);


-- BOOKSNOTES (Join Table)
CREATE TABLE books_notes (
    bk_id INTEGER NOT NULL,
    nt_id INTEGER NOT NULL,
    PRIMARY KEY (bk_id, nt_id),

    FOREIGN KEY (bk_id)
        REFERENCES books(bk_id)
        ON DELETE CASCADE,

    FOREIGN KEY (nt_id)
        REFERENCES notes(nt_id)
        ON DELETE CASCADE
);


-- INDEXES
-- USERS indexes
CREATE INDEX IF NOT EXISTS idx_users_email ON users (usr_email);
CREATE INDEX IF NOT EXISTS idx_users_username ON users (usr_username);

-- BOOKS indexes
CREATE INDEX IF NOT EXISTS idx_books_title ON books (bk_title);
CREATE INDEX IF NOT EXISTS idx_books_author ON books (bk_author);
-- CREATE INDEX IF NOT EXISTS idx_books_date_published ON books (bk_date_published);
CREATE INDEX IF NOT EXISTS idx_books_rating ON books (bk_rating);

-- NOTES indexes
CREATE INDEX idx_notes_title ON notes (nt_title);
CREATE INDEX idx_notes_date_created ON notes (nt_date_created);
CREATE INDEX idx_notes_date_updated ON notes (nt_date_updated);

-- BOOKSNOTES indexes
CREATE INDEX idx_booksnotes_book_id ON books_notes (bk_id);
CREATE INDEX idx_booksnotes_note_id ON books_notes (nt_id);