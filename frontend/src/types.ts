// Mirrors app/schemas/note.py NoteResponse
export type Note = {
    id: string;
    title: string;
    body: string;
    is_public: boolean;
    date_created: string;
    date_updated: string;
    user_id: string;
};

// Mirrors app/schemas/note.py NoteCreate/NoteUpdate
export type NoteInput = {
    title: string;
    body: string;
    is_public?: boolean;
};

// Mirrors app/schemas/user.py UserPublic
export type User = {
    id: string;
    username: string;
};

export type SignupInput = {
    email: string;
    username: string;
    password: string;
};

// Mirrors app/schemas/auth.py TokenResponse
export type TokenResponse = {
    access_token: string;
    refresh_token: string;
    token_type: string;
};