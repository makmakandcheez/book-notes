import { useEffect, useRef, useState } from "react";
import { getUsersByIds } from "../../../api/usersApi";
import type { User } from "../../../types";

/** Looks up and caches users by id, for annotating notes with their author. */
export function useUserDirectory(userIds: string[]): Record<string, User> {
    const [usersById, setUsersById] = useState<Record<string, User>>({});
    const fetchedIds = useRef(new Set<string>());

    useEffect(() => {
        const idsToFetch = [...new Set(userIds)].filter((id) => !fetchedIds.current.has(id));
        if (idsToFetch.length === 0) return;
        idsToFetch.forEach((id) => fetchedIds.current.add(id));
        getUsersByIds(idsToFetch)
            .then((users) => {
                setUsersById((prev) => {
                    const next = { ...prev };
                    for (const user of users) next[user.id] = user;
                    return next;
                });
            })
            .catch(() => {});
    }, [userIds]);

    return usersById;
}
