import { Link } from "react-router";
import { useAuth } from "../../auth/context/useAuth";
import { NoteListItem } from "../../notes/components/NoteListItem";
import { useNotes } from "../../notes/hooks/useNotes";
import { useUserDirectory } from "../../users/hooks/useUserDirectory";
import { FeaturedNote } from "../components/FeaturedNote";

export default function Landing() {
    const { currentUser, setAuthModal } = useAuth();
    const { notes, isLoading } = useNotes({ isPublic: true });

    const publicNotes = [...notes].sort(
        (a, b) => new Date(b.date_created).getTime() - new Date(a.date_created).getTime(),
    );

    const usersById = useUserDirectory(publicNotes.map((n) => n.user_id));

    const featured = publicNotes[0];
    const feedNotes = publicNotes.slice(1);
    const featuredAuthor = featured ? usersById[featured.user_id] : undefined;

    return (
        <div className="min-h-screen" style={{ background: "var(--background)" }}>
            <section className="px-6 pt-32 pb-20 max-w-4xl mx-auto">
                <p
                    className="text-xs font-medium mb-4 tracking-widest uppercase"
                    style={{ color: "var(--accent)", fontFamily: "var(--font-mono-face)" }}
                >
                    A place for ideas
                </p>
                <h1
                    className="mb-6"
                    style={{
                        fontFamily: "var(--font-display)",
                        fontSize: "clamp(40px, 6vw, 72px)",
                        color: "var(--foreground)",
                        lineHeight: 1.1,
                        letterSpacing: "-0.02em",
                    }}
                >
                    Write, share,
                    <br />
                    and keep your notes.
                </h1>
                <p className="text-lg mb-8 max-w-xl" style={{ color: "var(--muted-foreground)", lineHeight: 1.7 }}>
                    Book Notes is a minimalist space for notes on what you're reading — keep them private, or publish them for others.
                </p>
                {!currentUser && (
                    <div className="flex items-center gap-3">
                        <button
                            onClick={() => setAuthModal("signup")}
                            className="text-sm px-6 py-3 rounded font-medium"
                            style={{ background: "var(--accent)", color: "white" }}
                        >
                            Start writing
                        </button>
                        <button
                            onClick={() => setAuthModal("login")}
                            className="text-sm px-6 py-3 rounded font-medium"
                            style={{ color: "var(--muted-foreground)", background: "var(--muted)", border: "1px solid var(--border)" }}
                        >
                            Sign in
                        </button>
                    </div>
                )}
            </section>

            <div className="max-w-4xl mx-auto px-6 pb-24">
                {featured && featuredAuthor && <FeaturedNote note={featured} author={featuredAuthor} />}

                <div className="flex items-center justify-between mb-6" style={{ borderBottom: "1px solid var(--border)", paddingBottom: "16px" }}>
                    <h2 className="text-sm font-semibold" style={{ color: "var(--foreground)" }}>
                        Latest
                    </h2>
                    {currentUser && (
                        <Link to="/dashboard" className="text-xs" style={{ color: "var(--accent)", textDecoration: "none" }}>
                            + Write a note
                        </Link>
                    )}
                </div>

                <div className="space-y-px" style={{ border: "1px solid var(--border)", borderRadius: "var(--radius)", overflow: "hidden" }}>
                    {!isLoading && feedNotes.length === 0 && (
                        <div className="py-12 text-center" style={{ color: "var(--muted-foreground)" }}>
                            <p className="text-sm">No public notes yet.</p>
                        </div>
                    )}
                    {feedNotes.map((note) => (
                        <NoteListItem key={note.id} note={note} author={usersById[note.user_id]} />
                    ))}
                </div>
            </div>
        </div>
    );
}
