export default function Footer() {
    return (
        <footer className="px-6 py-6 text-center" style={{ borderTop: "1px solid var(--border)" }}>
            <p className="text-xs" style={{ color: "var(--muted-foreground)" }}>
                Book Notes &copy; {new Date().getFullYear()}
            </p>
        </footer>
    );
}
