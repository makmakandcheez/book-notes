import { Link } from "react-router";
import { Avatar } from "../../../components/Avatar";
import { formatDate, readingTime, stripMarkdown } from "../../../utils/format";
import type { Note, User } from "../../../types";

export function FeaturedNote({ note, author }: { note: Note; author: User }) {
    return (
        <div className="mb-12">
            <p
                className="text-xs font-medium mb-4 tracking-widest uppercase"
                style={{ color: "var(--muted-foreground)", fontFamily: "var(--font-mono-face)" }}
            >
                Featured
            </p>
            <Link to={`/note/${note.id}`} className="block group" style={{ textDecoration: "none" }}>
                <div className="p-8 rounded-lg transition-all" style={{ background: "var(--card)", border: "1px solid var(--border)" }}>
                    <h2
                        className="mb-3"
                        style={{ fontFamily: "var(--font-display)", fontSize: "clamp(20px, 3vw, 28px)", color: "var(--foreground)", lineHeight: 1.2 }}
                    >
                        {note.title}
                    </h2>
                    <p className="text-sm mb-6 line-clamp-3" style={{ color: "var(--muted-foreground)", lineHeight: 1.75 }}>
                        {stripMarkdown(note.body)}
                    </p>
                    <div className="flex items-center gap-2.5">
                        <Avatar user={author} size="md" />
                        <div>
                            <p className="text-sm font-medium" style={{ color: "var(--foreground)" }}>
                                {author.username}
                            </p>
                            <p className="text-xs" style={{ color: "var(--muted-foreground)", fontFamily: "var(--font-mono-face)" }}>
                                {formatDate(note.date_created)} &middot; {readingTime(note.body)} min read
                            </p>
                        </div>
                    </div>
                </div>
            </Link>
        </div>
    );
}
