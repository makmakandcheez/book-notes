import axios from "axios";

if (!import.meta.env.VITE_API_URL) {
    throw new Error("VITE_API_URL is not set. Copy frontend/.env.example to frontend/.env.local and set it.");
}

export const apiClient = axios.create({
    baseURL: import.meta.env.VITE_API_URL,
});

let accessToken: string | null = null;
let onUnauthorized: (() => void) | null = null;

export function setAccessToken(token: string | null): void {
    accessToken = token;
}

export function setUnauthorizedHandler(handler: (() => void) | null): void {
    onUnauthorized = handler;
}

apiClient.interceptors.request.use((config) => {
    if (accessToken) {
        config.headers.Authorization = `Bearer ${accessToken}`;
    }
    return config;
});

apiClient.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            onUnauthorized?.();
        }
        return Promise.reject(error);
    },
);
