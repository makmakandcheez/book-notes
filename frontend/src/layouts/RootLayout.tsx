import { Outlet } from "react-router";
import { AuthModal } from "../features/auth/components/AuthModal";
import Footer from "../components/Footer";
import Header from "../components/Header";

export default function RootLayout() {
    return (
        <>
            <Header />
            <AuthModal />
            <Outlet />
            <Footer />
        </>
    );
}
