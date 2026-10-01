import { apiClient } from "../utils/axiosConfig";
import type { Note, NoteInput } from "../types";

export async function listNotes(params?: {
    title?: string;
    user_id?: string;
    is_public?: boolean;
}): Promise<Note[]> {
    const res = await apiClient.get<Note[]>("/notes/", { params });
    return res.data;
}

export async function getNote(id: string): Promise<Note> {
    const res = await apiClient.get<Note>(`/notes/${id}`);
    return res.data;
}

export async function createNote(data: NoteInput): Promise<Note> {
    const res = await apiClient.post<Note>("/notes/", data);
    return res.data;
}

export async function updateNote(id: string, data: Partial<NoteInput>): Promise<Note> {
    const res = await apiClient.patch<Note>(`/notes/${id}`, data);
    return res.data;
}

export async function deleteNote(id: string): Promise<Note> {
    const res = await apiClient.delete<Note>(`/notes/${id}`);
    return res.data;
}
