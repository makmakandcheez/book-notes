import { useState } from "react";
import { Link, useNavigate } from "react-router";
import { createNote } from "../api/notesApi";
import { useAuth } from "../features/auth/context/useAuth";
import { Avatar } from "./Avatar";

export default function Header() {
    const { currentUser, setAuthModal, logout } = useAuth();
    const navigate = useNavigate();
    const [creatingNote, setCreatingNote] = useState(false);

    async function handleNewNote() {
        if (creatingNote) return;
        setCreatingNote(true);
        try {
            const note = await createNote({ title: "", body: "", is_public: false });
            navigate("/dashboard", { state: { newNoteId: note.id } });
        } finally {
            setCreatingNote(false);
        }
    }

    return (
        <header
            className="fixed top-0 left-0 right-0 z-40 flex items-center justify-between px-6 h-14"
            style={{ background: "rgba(12,12,12,0.92)", backdropFilter: "blur(12px)", borderBottom: "1px solid var(--border)" }}
        >
            <Link
                to="/"
                className="text-xl tracking-tight"
                style={{ fontFamily: "var(--font-display)", color: "var(--foreground)", textDecoration: "none" }}
            >
                Book Notes
            </Link>

            <nav className="flex items-center gap-1">
                <Link to="/" className="text-sm px-3 py-1.5 rounded transition-colors" style={{ color: "var(--muted-foreground)", textDecoration: "none" }}>
                    Feed
                </Link>
                {currentUser && (
                    <Link
                        to="/dashboard"
                        className="text-sm px-3 py-1.5 rounded transition-colors"
                        style={{ color: "var(--muted-foreground)", textDecoration: "none" }}
                    >
                        My Notes
                    </Link>
                )}
            </nav>

            <div className="flex items-center gap-2">
                {currentUser ? (
                    <>
                        <button
                            onClick={handleNewNote}
                            disabled={creatingNote}
                            className="text-sm px-3 py-1.5 rounded font-medium transition-opacity"
                            style={{ background: "var(--accent)", color: "white", opacity: creatingNote ? 0.6 : 1, cursor: creatingNote ? "not-allowed" : "pointer" }}
                        >
                            + New note
                        </button>
                        <button
                            onClick={() => navigate(`/profile/${currentUser.id}`)}
                            className="flex items-center gap-2 px-2 py-1.5 rounded transition-colors ml-1"
                            style={{ background: "transparent", border: "none" }}
                        >
                            <Avatar user={currentUser} size="sm" />
                            <span className="text-sm" style={{ color: "var(--foreground)" }}>
                                {currentUser.username}
                            </span>
                        </button>
                        <button
                            onClick={logout}
                            className="text-xs px-3 py-1.5 rounded transition-all"
                            style={{ color: "var(--muted-foreground)", background: "var(--muted)", border: "1px solid var(--border)" }}
                        >
                            Sign out
                        </button>
                    </>
                ) : (
                    <>
                        <button
                            onClick={() => setAuthModal("login")}
                            className="text-sm px-4 py-2 rounded font-medium transition-all"
                            style={{ color: "var(--muted-foreground)", background: "var(--muted)", border: "1px solid var(--border)" }}
                        >
                            Sign in
                        </button>
                        <button
                            onClick={() => setAuthModal("signup")}
                            className="text-sm px-4 py-2 rounded font-medium"
                            style={{ background: "var(--accent)", color: "white" }}
                        >
                            Sign up
                        </button>
                    </>
                )}
            </div>
        </header>
    );
}
