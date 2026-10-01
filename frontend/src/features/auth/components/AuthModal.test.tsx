import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { AuthContext, type AuthContextValue } from "../context/authContext";
import { AuthModal } from "./AuthModal";

function renderModal(overrides: Partial<AuthContextValue> = {}) {
    const value: AuthContextValue = {
        currentUser: null,
        isLoading: false,
        authModal: "signup",
        setAuthModal: vi.fn(),
        login: vi.fn().mockResolvedValue(undefined),
        signup: vi.fn().mockResolvedValue(undefined),
        logout: vi.fn(),
        ...overrides,
    };
    render(
        <AuthContext.Provider value={value}>
            <AuthModal />
        </AuthContext.Provider>,
    );
    return value;
}

describe("AuthModal", () => {
    it("does not close when a drag started inside the modal ends on the backdrop", () => {
        const { setAuthModal } = renderModal();
        const backdrop = screen.getByTestId("auth-modal-backdrop");
        const heading = screen.getByText("Join Book Notes.");

        // Simulate selecting text inside the modal and dragging the mouse out
        // past the backdrop before releasing.
        fireEvent.mouseDown(heading);
        fireEvent.click(backdrop);

        expect(setAuthModal).not.toHaveBeenCalled();
    });

    it("closes on a genuine click on the backdrop (mousedown and mouseup both outside)", () => {
        const { setAuthModal } = renderModal();
        const backdrop = screen.getByTestId("auth-modal-backdrop");

        fireEvent.mouseDown(backdrop);
        fireEvent.click(backdrop);

        expect(setAuthModal).toHaveBeenCalledWith(null);
    });

    it("does not close when clicking inside the modal card", () => {
        const { setAuthModal } = renderModal();
        const heading = screen.getByText("Join Book Notes.");

        fireEvent.mouseDown(heading);
        fireEvent.click(heading);

        expect(setAuthModal).not.toHaveBeenCalled();
    });

    it("closes on Escape", () => {
        const { setAuthModal } = renderModal();
        fireEvent.keyDown(window, { key: "Escape" });
        expect(setAuthModal).toHaveBeenCalledWith(null);
    });
});
