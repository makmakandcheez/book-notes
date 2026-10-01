import { useCallback, useEffect, useMemo, useState, type ReactNode } from "react";
import { login as loginRequest, refreshTokens, signup as signupRequest } from "../../../api/authApi";
import { getMe } from "../../../api/usersApi";
import { setAccessToken, setUnauthorizedHandler } from "../../../utils/axiosConfig";
import { clearStoredRefreshToken, getStoredRefreshToken, setStoredRefreshToken } from "../../../utils/tokenStorage";
import type { User } from "../../../types";
import { AuthContext, type AuthContextValue, type AuthModalMode } from "./authContext";

export function AuthProvider({ children }: { children: ReactNode }) {
    const [currentUser, setCurrentUser] = useState<User | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const [authModal, setAuthModal] = useState<AuthModalMode>(null);

    const applyTokens = useCallback((accessToken: string, refreshToken: string) => {
        setAccessToken(accessToken);
        setStoredRefreshToken(refreshToken);
    }, []);

    const logout = useCallback(() => {
        setAccessToken(null);
        clearStoredRefreshToken();
        setCurrentUser(null);
    }, []);

    useEffect(() => {
        setUnauthorizedHandler(logout);
        return () => setUnauthorizedHandler(null);
    }, [logout]);

    useEffect(() => {
        const storedRefreshToken = getStoredRefreshToken();
        if (!storedRefreshToken) {
            setIsLoading(false);
            return;
        }
        (async () => {
            try {
                const tokens = await refreshTokens(storedRefreshToken);
                applyTokens(tokens.access_token, tokens.refresh_token);
                setCurrentUser(await getMe());
            } catch {
                logout();
            } finally {
                setIsLoading(false);
            }
        })();
    }, [applyTokens, logout]);

    const login = useCallback(
        async (username: string, password: string) => {
            const tokens = await loginRequest(username, password);
            applyTokens(tokens.access_token, tokens.refresh_token);
            setCurrentUser(await getMe());
            setAuthModal(null);
        },
        [applyTokens],
    );

    const signup = useCallback(
        async (email: string, username: string, password: string) => {
            await signupRequest({ email, username, password });
            await login(username, password);
        },
        [login],
    );

    const value = useMemo<AuthContextValue>(
        () => ({ currentUser, isLoading, authModal, setAuthModal, login, signup, logout }),
        [currentUser, isLoading, authModal, login, signup, logout],
    );

    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
