import { Suspense, type ReactNode } from "react";

export function withSuspense(page: ReactNode) {
    return (
        <Suspense
            fallback={
                <div className="flex min-h-[40vh] items-center justify-center text-sm text-black/60">
                    Loading...
                </div>
            }
        >
            {page}
        </Suspense>
    );
}
