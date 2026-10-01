import { useCallback, useEffect, useState } from "react";
import { getNote } from "../../../api/notesApi";
import type { Note } from "../../../types";

export function useNote(id: string | undefined) {
    const [note, setNote] = useState<Note | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const refresh = useCallback(async () => {
        if (!id) return;
        setIsLoading(true);
        setError(null);
        try {
            setNote(await getNote(id));
        } catch {
            setError("Note not found.");
        } finally {
            setIsLoading(false);
        }
    }, [id]);

    useEffect(() => {
        refresh();
    }, [refresh]);

    return { note, isLoading, error, refresh };
}
