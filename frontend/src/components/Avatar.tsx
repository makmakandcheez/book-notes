import type { User } from "../types";

const COLORS = ["#8b7cf6", "#f97316", "#10b981", "#ec4899", "#3b82f6", "#f59e0b"];

const SIZES = {
    xs: "w-5 h-5 text-[9px]",
    sm: "w-6 h-6 text-[10px]",
    md: "w-8 h-8 text-xs",
    lg: "w-10 h-10 text-sm",
};

function colorFor(id: string): string {
    let hash = 0;
    for (let i = 0; i < id.length; i++) hash = (hash * 31 + id.charCodeAt(i)) >>> 0;
    return COLORS[hash % COLORS.length];
}

export function Avatar({ user, size = "sm" }: { user: User; size?: keyof typeof SIZES }) {
    const color = colorFor(user.id);
    return (
        <div
            className={`${SIZES[size]} rounded-full flex items-center justify-center font-semibold shrink-0`}
            style={{ background: color + "22", color, border: `1px solid ${color}44` }}
        >
            {user.username.slice(0, 2).toUpperCase()}
        </div>
    );
}
