import { useEffect, useRef, useState } from "react";
import { Link, useLocation, useNavigate } from "react-router";
import { createNote, deleteNote, updateNote as updateNoteApi } from "../../../api/notesApi";
import { useAuth } from "../../auth/context/useAuth";
import { useNotes } from "../hooks/useNotes";

const SAVE_DEBOUNCE_MS = 600;

function formatUpdated(dateString: string): string {
    const date = new Date(dateString);
    const days = Math.floor((Date.now() - date.getTime()) / 86400000);
    if (days === 0) return date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
    if (days === 1) return "Yesterday";
    if (days < 7) return date.toLocaleDateString([], { weekday: "short" });
    return date.toLocaleDateString([], { month: "short", day: "numeric" });
}

export default function Dashboard() {
    const { currentUser } = useAuth();
    const { notes, refresh } = useNotes({ userId: currentUser?.id });
    const [selectedNoteId, setSelectedNoteId] = useState<string | null>(null);
    const [draft, setDraft] = useState<{ title: string; body: string } | null>(null);
    const saveTimeout = useRef<ReturnType<typeof setTimeout> | null>(null);
    const textareaRef = useRef<HTMLTextAreaElement>(null);
    const location = useLocation();
    const navigate = useNavigate();

    const myNotes = [...notes].sort(
        (a, b) => new Date(b.date_updated).getTime() - new Date(a.date_updated).getTime(),
    );

    const selectedNote = myNotes.find((n) => n.id === selectedNoteId) ?? null;

    useEffect(() => {
        setDraft(selectedNote ? { title: selectedNote.title, body: selectedNote.body } : null);
        // Only reset the draft when the selected note changes, not on every
        // background refresh of the same note (which would clobber in-flight edits).
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [selectedNote?.id]);

    // The Header's "+ New note" button creates the note before navigating here
    // and hands off which one to select via location.state (it has no access
    // to this component's selection state).
    useEffect(() => {
        const newNoteId = (location.state as { newNoteId?: string } | null)?.newNoteId;
        if (!newNoteId) return;
        navigate(location.pathname, { replace: true, state: null });
        // Dashboard's own note list may predate this note (it was created from
        // the Header, outside this component), so refresh before selecting it.
        refresh().then(() => {
            setSelectedNoteId(newNoteId);
            setTimeout(() => textareaRef.current?.focus(), 50);
        });
    }, [location.state, location.pathname, navigate, refresh]);

    if (!currentUser) {
        return (
            <div className="min-h-screen flex items-center justify-center" style={{ background: "var(--background)" }}>
                <div className="text-center space-y-3">
                    <p style={{ color: "var(--muted-foreground)" }}>Sign in to access your notes.</p>
                    <Link to="/" style={{ color: "var(--accent)", fontSize: "14px" }}>
                        ← Back to feed
                    </Link>
                </div>
            </div>
        );
    }

    function scheduleSave(id: string, patch: { title?: string; body?: string }) {
        if (saveTimeout.current) clearTimeout(saveTimeout.current);
        saveTimeout.current = setTimeout(() => {
            updateNoteApi(id, patch).then(refresh);
        }, SAVE_DEBOUNCE_MS);
    }

    function handleTitleChange(value: string) {
        if (!selectedNote) return;
        setDraft((d) => (d ? { ...d, title: value } : d));
        scheduleSave(selectedNote.id, { title: value });
    }

    function handleBodyChange(value: string) {
        if (!selectedNote) return;
        setDraft((d) => (d ? { ...d, body: value } : d));
        scheduleSave(selectedNote.id, { body: value });
    }

    async function handleTogglePublic() {
        if (!selectedNote) return;
        await updateNoteApi(selectedNote.id, { is_public: !selectedNote.is_public });
        refresh();
    }

    async function handleCreateNote() {
        const note = await createNote({ title: "", body: "", is_public: false });
        await refresh();
        setSelectedNoteId(note.id);
        setTimeout(() => textareaRef.current?.focus(), 50);
    }

    async function handleDelete(id: string) {
        await deleteNote(id);
        setSelectedNoteId(null);
        refresh();
    }

    return (
        <div className="h-screen flex flex-col pt-14" style={{ background: "var(--background)" }}>
            <div className="flex flex-1 min-h-0">
                <aside className="flex flex-col w-60 shrink-0" style={{ borderRight: "1px solid var(--border)", background: "var(--card)" }}>
                    <div className="px-4 py-3 flex items-center justify-between">
                        <span className="text-xs font-medium" style={{ color: "var(--muted-foreground)" }}>
                            My notes
                        </span>
                        <button onClick={handleCreateNote} className="text-xs" style={{ color: "var(--accent)" }}>
                            + New
                        </button>
                    </div>

                    <div className="flex-1 overflow-y-auto">
                        {myNotes.length === 0 ? (
                            <div className="px-4 py-8 text-center">
                                <p className="text-xs" style={{ color: "var(--muted-foreground)" }}>
                                    No notes yet.
                                </p>
                                <button onClick={handleCreateNote} className="mt-2 text-xs underline" style={{ color: "var(--accent)" }}>
                                    Create one
                                </button>
                            </div>
                        ) : (
                            myNotes.map((note) => {
                                const isSelected = note.id === selectedNoteId;
                                return (
                                    <button
                                        key={note.id}
                                        onClick={() => setSelectedNoteId(note.id)}
                                        className="w-full text-left px-4 py-3 block transition-colors"
                                        style={{
                                            background: isSelected ? "var(--muted)" : "transparent",
                                            borderLeft: isSelected ? "2px solid var(--accent)" : "2px solid transparent",
                                        }}
                                    >
                                        <div className="flex items-start justify-between gap-2 mb-0.5">
                                            <p className="text-sm font-medium truncate leading-snug" style={{ color: "var(--foreground)" }}>
                                                {note.title || "Untitled"}
                                            </p>
                                            <span className="text-[10px] shrink-0 mt-0.5" style={{ color: "var(--muted-foreground)", fontFamily: "var(--font-mono-face)" }}>
                                                {formatUpdated(note.date_updated)}
                                            </span>
                                        </div>
                                        <p className="text-xs truncate mb-1.5" style={{ color: "var(--muted-foreground)" }}>
                                            {note.body.split("\n")[0] || "No content"}
                                        </p>
                                        <span className="text-[10px]" style={{ color: "var(--muted-foreground)" }}>
                                            {note.is_public ? "◎ Public" : "● Private"}
                                        </span>
                                    </button>
                                );
                            })
                        )}
                    </div>
                </aside>

                <main className="flex-1 flex flex-col min-w-0">
                    {selectedNote && draft ? (
                        <>
                            <div className="flex items-center justify-between px-6 py-2.5 shrink-0" style={{ borderBottom: "1px solid var(--border)" }}>
                                <div className="flex items-center gap-3">
                                    {selectedNote.is_public && (
                                        <Link to={`/note/${selectedNote.id}`} className="text-xs" style={{ color: "var(--accent)", textDecoration: "none" }}>
                                            View public →
                                        </Link>
                                    )}
                                </div>
                                <div className="flex items-center gap-2">
                                    <span className="text-xs" style={{ color: "var(--muted-foreground)", fontFamily: "var(--font-mono-face)" }}>
                                        {formatUpdated(selectedNote.date_updated)}
                                    </span>
                                    <button
                                        onClick={handleTogglePublic}
                                        className="flex items-center gap-1.5 text-xs px-2.5 py-1.5 rounded transition-all"
                                        style={{ background: "var(--muted)", color: "var(--muted-foreground)", border: "1px solid var(--border)" }}
                                    >
                                        {selectedNote.is_public ? "◎ Public" : "● Private"}
                                    </button>
                                    <button
                                        onClick={() => handleDelete(selectedNote.id)}
                                        className="text-xs px-2 py-1.5 rounded transition-all"
                                        style={{ color: "var(--muted-foreground)" }}
                                    >
                                        Delete
                                    </button>
                                </div>
                            </div>

                            <div className="flex-1 overflow-y-auto px-10 py-8 max-w-3xl w-full mx-auto">
                                <input
                                    type="text"
                                    value={draft.title}
                                    onChange={(e) => handleTitleChange(e.target.value)}
                                    placeholder="Untitled"
                                    className="w-full bg-transparent border-none outline-none mb-4"
                                    style={{ fontFamily: "var(--font-display)", fontSize: "clamp(22px, 3vw, 32px)", color: "var(--foreground)", lineHeight: 1.2 }}
                                />
                                <textarea
                                    ref={textareaRef}
                                    value={draft.body}
                                    onChange={(e) => handleBodyChange(e.target.value)}
                                    placeholder="Start writing…"
                                    className="w-full bg-transparent border-none outline-none resize-none"
                                    style={{ color: "var(--foreground)", fontSize: "15px", minHeight: "60vh", opacity: 0.9, lineHeight: 1.8 }}
                                />
                            </div>
                        </>
                    ) : (
                        <div className="flex-1 flex flex-col items-center justify-center gap-4">
                            <p className="text-3xl" style={{ fontFamily: "var(--font-display)", color: "var(--muted-foreground)", opacity: 0.3 }}>
                                Select a note
                            </p>
                            <button onClick={handleCreateNote} className="text-sm px-4 py-2 rounded font-medium" style={{ background: "var(--accent)", color: "white" }}>
                                + New note
                            </button>
                        </div>
                    )}
                </main>
            </div>
        </div>
    );
}
