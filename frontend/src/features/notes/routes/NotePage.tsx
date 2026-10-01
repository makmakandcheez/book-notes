import { Link, useNavigate, useParams } from "react-router";
import { Avatar } from "../../../components/Avatar";
import { formatDate, readingTime } from "../../../utils/format";
import { useAuth } from "../../auth/context/useAuth";
import { useUserDirectory } from "../../users/hooks/useUserDirectory";
import { useNote } from "../hooks/useNote";

function renderBody(body: string) {
    return body.split("\n").map((line, i) => {
        if (line.startsWith("## "))
            return (
                <h2 key={i} style={{ fontFamily: "var(--font-display)", fontSize: "22px", color: "var(--foreground)", margin: "1.5em 0 0.5em" }}>
                    {line.slice(3)}
                </h2>
            );
        if (line.startsWith("# "))
            return (
                <h1 key={i} style={{ fontFamily: "var(--font-display)", fontSize: "28px", color: "var(--foreground)", margin: "1.5em 0 0.5em" }}>
                    {line.slice(2)}
                </h1>
            );
        if (line.trim() === "") return <div key={i} style={{ height: "1em" }} />;
        return (
            <p key={i} style={{ color: "var(--foreground)", lineHeight: 1.8, marginBottom: "0.25em", opacity: 0.9 }}>
                {line}
            </p>
        );
    });
}

export default function NotePage() {
    const { id } = useParams<{ id: string }>();
    const { note, isLoading, error } = useNote(id);
    const { currentUser } = useAuth();
    const navigate = useNavigate();
    const usersById = useUserDirectory(note ? [note.user_id] : []);

    if (isLoading) return null;

    if (error || !note) {
        return (
            <div className="min-h-screen flex items-center justify-center" style={{ background: "var(--background)" }}>
                <div className="text-center">
                    <p style={{ color: "var(--muted-foreground)" }}>Note not found.</p>
                    <Link to="/" style={{ color: "var(--accent)", fontSize: "14px" }}>
                        ← Back to feed
                    </Link>
                </div>
            </div>
        );
    }

    const isOwner = currentUser?.id === note.user_id;
    if (!note.is_public && !isOwner) {
        return (
            <div className="min-h-screen flex items-center justify-center" style={{ background: "var(--background)" }}>
                <div className="text-center space-y-3">
                    <p className="text-lg" style={{ fontFamily: "var(--font-display)", color: "var(--foreground)" }}>
                        This note is private.
                    </p>
                    <Link to="/" style={{ color: "var(--accent)", fontSize: "14px" }}>
                        ← Back to feed
                    </Link>
                </div>
            </div>
        );
    }

    const author = usersById[note.user_id];
    const readTime = readingTime(note.body);

    return (
        <div className="min-h-screen" style={{ background: "var(--background)" }}>
            <div className="max-w-2xl mx-auto px-6 pt-24 pb-24">
                <Link to="/" className="inline-flex items-center gap-1.5 text-sm mb-10" style={{ color: "var(--muted-foreground)", textDecoration: "none" }}>
                    ← Feed
                </Link>

                <h1
                    className="mb-6"
                    style={{ fontFamily: "var(--font-display)", fontSize: "clamp(26px, 4vw, 40px)", color: "var(--foreground)", lineHeight: 1.15, letterSpacing: "-0.01em" }}
                >
                    {note.title || "Untitled"}
                </h1>

                <div className="flex items-center justify-between flex-wrap gap-4 mb-10 pb-8" style={{ borderBottom: "1px solid var(--border)" }}>
                    {author && (
                        <div className="flex items-center gap-3">
                            <button onClick={() => navigate(`/profile/${author.id}`)} style={{ background: "none", border: "none", padding: 0, cursor: "pointer" }}>
                                <Avatar user={author} size="md" />
                            </button>
                            <div>
                                <button
                                    onClick={() => navigate(`/profile/${author.id}`)}
                                    className="text-sm font-medium text-left"
                                    style={{ color: "var(--foreground)", background: "none", border: "none", cursor: "pointer", padding: 0 }}
                                >
                                    {author.username}
                                </button>
                                <p className="text-xs" style={{ color: "var(--muted-foreground)", fontFamily: "var(--font-mono-face)" }}>
                                    {formatDate(note.date_created)} &middot; {readTime} min read
                                </p>
                            </div>
                        </div>
                    )}
                    {isOwner && (
                        <Link to="/dashboard" className="text-xs px-3 py-1.5 rounded font-medium" style={{ background: "var(--muted)", color: "var(--foreground)", border: "1px solid var(--border)", textDecoration: "none" }}>
                            Edit in dashboard
                        </Link>
                    )}
                </div>

                <div className="mb-12" style={{ fontSize: "16px", lineHeight: 1.8 }}>
                    {renderBody(note.body)}
                </div>
            </div>
        </div>
    );
}
