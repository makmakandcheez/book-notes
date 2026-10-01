import { apiClient } from "../utils/axiosConfig";
import type { SignupInput, TokenResponse, User } from "../types";

export async function signup(data: SignupInput): Promise<User> {
    const res = await apiClient.post<User>("/auth/signup", data);
    return res.data;
}

export async function login(username: string, password: string): Promise<TokenResponse> {
    const form = new URLSearchParams();
    form.set("username", username);
    form.set("password", password);
    const res = await apiClient.post<TokenResponse>("/auth/token", form, {
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
    });
    return res.data;
}

export async function refreshTokens(refreshToken: string): Promise<TokenResponse> {
    const res = await apiClient.post<TokenResponse>("/auth/refresh-token", {
        refresh_token: refreshToken,
    });
    return res.data;
}
