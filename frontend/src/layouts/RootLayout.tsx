import { Outlet } from "react-router"
import Header from "../components/layout/Header"
import Footer from "../components/layout/Footer"

export default function RootLayout() {
    return (
        <>
            <Header />
            <Outlet />
            <Footer />
        </>
    )
}