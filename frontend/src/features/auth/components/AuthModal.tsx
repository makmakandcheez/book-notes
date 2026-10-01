import { isAxiosError } from "axios";
import { useEffect, useRef, useState } from "react";
import { useAuth } from "../context/useAuth";

const inputStyle = {
    background: "var(--muted)",
    border: "1px solid var(--border)",
    color: "var(--foreground)",
    borderRadius: "var(--radius)",
    outline: "none",
    fontSize: "14px",
    width: "100%",
    padding: "10px 12px",
    transition: "border-color 0.15s",
} as const;

function extractErrorMessage(err: unknown): string {
    if (isAxiosError(err) && typeof err.response?.data?.detail === "string") {
        return err.response.data.detail;
    }
    return "Something went wrong. Please try again.";
}

export function AuthModal() {
    const { authModal, setAuthModal, login, signup } = useAuth();
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);
    const mouseDownOnBackdrop = useRef(false);

    const mode = authModal;

    useEffect(() => {
        setError(null);
        setUsername("");
        setEmail("");
        setPassword("");
    }, [mode]);

    useEffect(() => {
        const handler = (e: KeyboardEvent) => {
            if (e.key === "Escape") setAuthModal(null);
        };
        window.addEventListener("keydown", handler);
        return () => window.removeEventListener("keydown", handler);
    }, [setAuthModal]);

    if (!mode) return null;

    async function handleSubmit(e: React.FormEvent) {
        e.preventDefault();
        setError(null);
        setLoading(true);
        try {
            if (mode === "login") {
                await login(username, password);
            } else {
                await signup(email, username, password);
            }
        } catch (err) {
            setError(extractErrorMessage(err));
        } finally {
            setLoading(false);
        }
    }

    return (
        <div
            data-testid="auth-modal-backdrop"
            className="fixed inset-0 z-50 flex items-center justify-center"
            style={{ background: "rgba(0,0,0,0.75)" }}
            onMouseDown={(e) => {
                mouseDownOnBackdrop.current = e.target === e.currentTarget;
            }}
            onClick={(e) => {
                if (mouseDownOnBackdrop.current && e.target === e.currentTarget) setAuthModal(null);
            }}
        >
            <div
                className="w-full max-w-sm mx-4 rounded-lg overflow-hidden"
                style={{ background: "var(--card)", border: "1px solid var(--border)" }}
            >
                <div className="px-6 pt-6 pb-5">
                    <div className="flex items-start justify-between mb-6">
                        <div>
                            <h2
                                className="text-2xl"
                                style={{ fontFamily: "var(--font-display)", color: "var(--foreground)", lineHeight: 1.2 }}
                            >
                                {mode === "login" ? "Welcome back." : "Join Book Notes."}
                            </h2>
                            <p className="text-sm mt-1" style={{ color: "var(--muted-foreground)" }}>
                                {mode === "login" ? "Sign in to your account." : "Start writing and sharing."}
                            </p>
                        </div>
                        <button onClick={() => setAuthModal(null)} style={{ color: "var(--muted-foreground)", fontSize: "18px", lineHeight: 1 }}>
                            ×
                        </button>
                    </div>

                    <form onSubmit={handleSubmit} className="space-y-3">
                        {mode === "signup" && (
                            <div>
                                <label className="block text-xs font-medium mb-1.5" style={{ color: "var(--muted-foreground)" }}>
                                    Email
                                </label>
                                <input
                                    type="email"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    placeholder="you@example.com"
                                    required
                                    style={inputStyle}
                                    onFocus={(e) => (e.currentTarget.style.borderColor = "var(--accent)")}
                                    onBlur={(e) => (e.currentTarget.style.borderColor = "var(--border)")}
                                />
                            </div>
                        )}
                        <div>
                            <label className="block text-xs font-medium mb-1.5" style={{ color: "var(--muted-foreground)" }}>
                                Username
                            </label>
                            <input
                                type="text"
                                value={username}
                                onChange={(e) => setUsername(e.target.value)}
                                placeholder="mara"
                                required
                                style={inputStyle}
                                onFocus={(e) => (e.currentTarget.style.borderColor = "var(--accent)")}
                                onBlur={(e) => (e.currentTarget.style.borderColor = "var(--border)")}
                            />
                        </div>
                        <div>
                            <label className="block text-xs font-medium mb-1.5" style={{ color: "var(--muted-foreground)" }}>
                                Password
                            </label>
                            <input
                                type="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                placeholder="••••••••"
                                required
                                style={inputStyle}
                                onFocus={(e) => (e.currentTarget.style.borderColor = "var(--accent)")}
                                onBlur={(e) => (e.currentTarget.style.borderColor = "var(--border)")}
                            />
                        </div>
                        {error && (
                            <p className="text-xs py-2 px-3 rounded" style={{ color: "#f87171", background: "#ef444411", border: "1px solid #ef444422" }}>
                                {error}
                            </p>
                        )}
                        <button
                            type="submit"
                            disabled={loading}
                            className="w-full py-2.5 rounded font-medium text-sm mt-1"
                            style={{ background: "var(--accent)", color: "white", opacity: loading ? 0.6 : 1, cursor: loading ? "not-allowed" : "pointer" }}
                        >
                            {loading ? "…" : mode === "login" ? "Sign in" : "Create account"}
                        </button>
                    </form>

                    <p className="text-xs text-center mt-4" style={{ color: "var(--muted-foreground)" }}>
                        {mode === "login" ? "No account? " : "Already have one? "}
                        <button
                            onClick={() => setAuthModal(mode === "login" ? "signup" : "login")}
                            className="underline"
                            style={{ color: "var(--accent)" }}
                        >
                            {mode === "login" ? "Sign up" : "Sign in"}
                        </button>
                    </p>
                </div>
            </div>
        </div>
    );
}
