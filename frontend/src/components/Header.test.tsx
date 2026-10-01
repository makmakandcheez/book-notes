import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter, Route, Routes } from "react-router";
import { describe, expect, it, vi } from "vitest";
import * as notesApi from "../api/notesApi";
import { AuthContext, type AuthContextValue } from "../features/auth/context/authContext";
import Header from "./Header";

vi.mock("../api/notesApi");

function renderHeader(overrides: Partial<AuthContextValue> = {}) {
    const value: AuthContextValue = {
        currentUser: { id: "user-1", username: "mara" },
        isLoading: false,
        authModal: null,
        setAuthModal: vi.fn(),
        login: vi.fn(),
        signup: vi.fn(),
        logout: vi.fn(),
        ...overrides,
    };
    render(
        <AuthContext.Provider value={value}>
            <MemoryRouter initialEntries={["/"]}>
                <Routes>
                    <Route path="/" element={<Header />} />
                    <Route path="/dashboard" element={<div>Dashboard page</div>} />
                </Routes>
            </MemoryRouter>
        </AuthContext.Provider>,
    );
}

describe("Header + New note button", () => {
    it("creates a note via the API and navigates to the dashboard with it selected", async () => {
        vi.mocked(notesApi.createNote).mockResolvedValue({
            id: "note-123",
            title: "",
            body: "",
            is_public: false,
            date_created: "2026-01-01T00:00:00Z",
            date_updated: "2026-01-01T00:00:00Z",
            user_id: "user-1",
        });

        renderHeader();
        await userEvent.click(screen.getByRole("button", { name: "+ New note" }));

        await waitFor(() => expect(notesApi.createNote).toHaveBeenCalledWith({ title: "", body: "", is_public: false }));
        await screen.findByText("Dashboard page");
    });
});
