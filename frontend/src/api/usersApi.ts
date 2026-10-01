import { apiClient } from "../utils/axiosConfig";
import type { Note, User } from "../types";

export async function getMe(): Promise<User> {
    const res = await apiClient.get<User>("/users/me");
    return res.data;
}

export async function getUser(id: string): Promise<User> {
    const res = await apiClient.get<User>(`/users/${id}`);
    return res.data;
}

export async function getUsersByIds(ids: string[]): Promise<User[]> {
    if (ids.length === 0) return [];
    const res = await apiClient.get<User[]>("/users/", {
        params: { ids },
        // FastAPI expects repeated `ids=a&ids=b`, not axios's default `ids[]=a&ids[]=b`.
        paramsSerializer: { indexes: null },
    });
    return res.data;
}

export async function updateUsername(id: string, username: string): Promise<User> {
    const res = await apiClient.patch<User>(`/users/${id}`, { username });
    return res.data;
}

export async function getUserNotes(id: string): Promise<Note[]> {
    const res = await apiClient.get<Note[]>(`/users/${id}/notes`);
    return res.data;
}
