export function formatDate(dateString: string): string {
    return new Date(dateString).toLocaleDateString([], { month: "short", day: "numeric", year: "numeric" });
}

export function readingTime(body: string): number {
    const words = body.trim().split(/\s+/).filter(Boolean).length;
    return Math.max(1, Math.round(words / 200));
}

export function stripMarkdown(body: string): string {
    return body.replace(/#+\s?/g, "").replace(/\*\*/g, "").replace(/`/g, "");
}
