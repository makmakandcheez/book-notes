import { useCallback, useEffect, useState } from "react";
import { listNotes } from "../../../api/notesApi";
import type { Note } from "../../../types";

type UseNotesParams = {
    /** Fetch this user's own notes (requires that user to be the authenticated caller to see private ones). */
    userId?: string;
    isPublic?: boolean;
};

export function useNotes(params: UseNotesParams = {}) {
    const { userId, isPublic } = params;
    const [notes, setNotes] = useState<Note[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const refresh = useCallback(async () => {
        setIsLoading(true);
        setError(null);
        try {
            setNotes(await listNotes({ user_id: userId, is_public: isPublic }));
        } catch {
            setError("Couldn't load notes.");
        } finally {
            setIsLoading(false);
        }
    }, [userId, isPublic]);

    useEffect(() => {
        refresh();
    }, [refresh]);

    return { notes, isLoading, error, refresh };
}
