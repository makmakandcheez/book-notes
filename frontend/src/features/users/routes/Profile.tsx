import { isAxiosError } from "axios";
import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router";
import { getUser, getUserNotes, updateUsername } from "../../../api/usersApi";
import { Avatar } from "../../../components/Avatar";
import { NoteListItem } from "../../notes/components/NoteListItem";
import { useAuth } from "../../auth/context/useAuth";
import type { Note, User } from "../../../types";

export default function Profile() {
    const { userId } = useParams<{ userId: string }>();
    const { currentUser } = useAuth();
    const navigate = useNavigate();

    const [profile, setProfile] = useState<User | null>(null);
    const [publicNotes, setPublicNotes] = useState<Note[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [isEditingUsername, setIsEditingUsername] = useState(false);
    const [usernameDraft, setUsernameDraft] = useState("");
    const [usernameError, setUsernameError] = useState<string | null>(null);

    useEffect(() => {
        if (!userId) return;
        setIsLoading(true);
        Promise.all([getUser(userId), getUserNotes(userId)])
            .then(([user, notes]) => {
                setProfile(user);
                setPublicNotes(notes);
            })
            .catch(() => setProfile(null))
            .finally(() => setIsLoading(false));
    }, [userId]);

    if (isLoading) return null;

    if (!profile) {
        return (
            <div className="min-h-screen flex items-center justify-center" style={{ background: "var(--background)" }}>
                <p style={{ color: "var(--muted-foreground)" }}>User not found.</p>
            </div>
        );
    }

    const isOwn = currentUser?.id === profile.id;

    async function handleSaveUsername() {
        if (!profile || !usernameDraft.trim()) return;
        setUsernameError(null);
        try {
            const updated = await updateUsername(profile.id, usernameDraft.trim());
            setProfile(updated);
            setIsEditingUsername(false);
        } catch (err) {
            setUsernameError(isAxiosError(err) && typeof err.response?.data?.detail === "string" ? err.response.data.detail : "Couldn't update username.");
        }
    }

    return (
        <div className="min-h-screen" style={{ background: "var(--background)" }}>
            <div className="max-w-3xl mx-auto px-6 pt-24 pb-24">
                <div className="flex items-start justify-between gap-6 mb-10 pb-8" style={{ borderBottom: "1px solid var(--border)" }}>
                    <div className="flex items-start gap-5">
                        <Avatar user={profile} size="lg" />
                        <div>
                            {isEditingUsername ? (
                                <div className="flex items-center gap-2 mb-1">
                                    <input
                                        type="text"
                                        value={usernameDraft}
                                        onChange={(e) => setUsernameDraft(e.target.value)}
                                        className="text-2xl bg-transparent outline-none"
                                        style={{ fontFamily: "var(--font-display)", color: "var(--foreground)", borderBottom: "1px solid var(--border)" }}
                                    />
                                    <button onClick={handleSaveUsername} className="text-xs px-2 py-1 rounded" style={{ background: "var(--accent)", color: "white" }}>
                                        Save
                                    </button>
                                    <button onClick={() => setIsEditingUsername(false)} className="text-xs" style={{ color: "var(--muted-foreground)" }}>
                                        Cancel
                                    </button>
                                </div>
                            ) : (
                                <h1 className="text-2xl mb-1" style={{ fontFamily: "var(--font-display)", color: "var(--foreground)" }}>
                                    {profile.username}
                                    {isOwn && (
                                        <button
                                            onClick={() => {
                                                setUsernameDraft(profile.username);
                                                setIsEditingUsername(true);
                                            }}
                                            className="text-xs ml-3 align-middle"
                                            style={{ color: "var(--accent)" }}
                                        >
                                            Edit
                                        </button>
                                    )}
                                </h1>
                            )}
                            {usernameError && (
                                <p className="text-xs mb-1" style={{ color: "#f87171" }}>
                                    {usernameError}
                                </p>
                            )}
                            <span className="text-xs" style={{ color: "var(--muted-foreground)" }}>
                                <span className="font-semibold" style={{ color: "var(--foreground)" }}>
                                    {publicNotes.length}
                                </span>{" "}
                                public notes
                            </span>
                        </div>
                    </div>
                    {isOwn && (
                        <button
                            onClick={() => navigate("/dashboard")}
                            className="text-sm px-4 py-2 rounded font-medium shrink-0"
                            style={{ background: "var(--muted)", color: "var(--muted-foreground)", border: "1px solid var(--border)" }}
                        >
                            My notes →
                        </button>
                    )}
                </div>

                <h2 className="text-sm font-semibold mb-4" style={{ color: "var(--foreground)" }}>
                    {isOwn ? "Public notes" : "Notes"}
                </h2>
                {publicNotes.length === 0 ? (
                    <p className="text-sm mb-10" style={{ color: "var(--muted-foreground)" }}>
                        {isOwn ? "You haven't published any notes yet." : "No public notes yet."}
                    </p>
                ) : (
                    <div className="mb-10 space-y-px" style={{ border: "1px solid var(--border)", borderRadius: "var(--radius)", overflow: "hidden" }}>
                        {publicNotes.map((note) => (
                            <NoteListItem key={note.id} note={note} />
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
}
