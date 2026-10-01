import { Link } from "react-router";
import { Avatar } from "../../../components/Avatar";
import { formatDate, readingTime, stripMarkdown } from "../../../utils/format";
import type { Note, User } from "../../../types";

export function NoteListItem({ note, author }: { note: Note; author?: User }) {
    return (
        <Link
            to={`/note/${note.id}`}
            className="flex items-start gap-5 px-6 py-5 block transition-colors"
            style={{ background: "var(--card)", textDecoration: "none", display: "flex" }}
        >
            {author && <Avatar user={author} size="md" />}
            <div className="flex-1 min-w-0">
                <div className="flex items-start justify-between gap-4 mb-1">
                    <h3 className="text-base font-medium leading-snug" style={{ color: "var(--foreground)", fontFamily: "var(--font-display)" }}>
                        {note.title || "Untitled"}
                    </h3>
                    <span className="text-xs shrink-0 mt-0.5" style={{ color: "var(--muted-foreground)", fontFamily: "var(--font-mono-face)" }}>
                        {formatDate(note.date_created)}
                    </span>
                </div>
                <p className="text-sm mb-2 line-clamp-2" style={{ color: "var(--muted-foreground)", lineHeight: 1.6 }}>
                    {stripMarkdown(note.body).slice(0, 160)}
                </p>
                {author && (
                    <span className="text-xs" style={{ color: "var(--muted-foreground)" }}>
                        {author.username} &middot; {readingTime(note.body)} min read
                    </span>
                )}
            </div>
        </Link>
    );
}
