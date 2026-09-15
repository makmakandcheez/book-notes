import { createBrowserRouter } from "react-router";
import { lazy, Suspense } from "react";

import RootLayout from "./layouts/RootLayout";

const Landing = lazy(() => import("./features/landing/routes/Landing"));

function withSuspense(page: React.ReactNode) {
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

const router = createBrowserRouter([
    {
        element: <RootLayout />,
        children: [
            { path: "/", element: withSuspense(<Landing />) },
        ],
    },
]);

export default router;