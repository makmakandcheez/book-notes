import { render, screen } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router";
import { describe, expect, it, vi } from "vitest";
import * as notesApi from "../../../api/notesApi";
import { AuthContext, type AuthContextValue } from "../../auth/context/authContext";
import type { Note } from "../../../types";
import Dashboard from "./Dashboard";

vi.mock("../../../api/notesApi");

const authValue: AuthContextValue = {
    currentUser: { id: "user-1", username: "mara" },
    isLoading: false,
    authModal: null,
    setAuthModal: vi.fn(),
    login: vi.fn(),
    signup: vi.fn(),
    logout: vi.fn(),
};

function renderDashboard(state?: Record<string, unknown>) {
    render(
        <AuthContext.Provider value={authValue}>
            <MemoryRouter initialEntries={[{ pathname: "/dashboard", state }]}>
                <Routes>
                    <Route path="/dashboard" element={<Dashboard />} />
                </Routes>
            </MemoryRouter>
        </AuthContext.Provider>,
    );
}

describe("Dashboard picking up a note created from the Header", () => {
    it("refreshes its stale note list before selecting a newNoteId passed via navigation state", async () => {
        const newNote: Note = {
            id: "note-123",
            title: "",
            body: "",
            is_public: false,
            date_created: "2026-01-01T00:00:00Z",
            date_updated: "2026-01-01T00:00:00Z",
            user_id: "user-1",
        };

        // First call: Dashboard's own mount-time fetch, predating the note
        // created elsewhere (by the Header). Second call: the refresh this
        // component must trigger once it sees newNoteId in location.state.
        vi.mocked(notesApi.listNotes).mockResolvedValueOnce([]).mockResolvedValueOnce([newNote]);

        renderDashboard({ newNoteId: "note-123" });

        await screen.findByPlaceholderText("Start writing…");
    });
});
