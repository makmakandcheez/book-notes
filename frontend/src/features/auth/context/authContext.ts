import { createContext } from "react";
import type { User } from "../../../types";

export type AuthModalMode = "login" | "signup" | null;

export type AuthContextValue = {
    currentUser: User | null;
    isLoading: boolean;
    authModal: AuthModalMode;
    setAuthModal: (mode: AuthModalMode) => void;
    login: (username: string, password: string) => Promise<void>;
    signup: (email: string, username: string, password: string) => Promise<void>;
    logout: () => void;
};

export const AuthContext = createContext<AuthContextValue | null>(null);
