import { createBrowserRouter } from "react-router";

import RootLayout from "./layouts/RootLayout";
import { withSuspense } from "./utils/withSuspense";
import { Dashboard, Landing, NotePage, Profile } from "./routeComponents";

const router = createBrowserRouter([
    {
        path: "/",
        Component: RootLayout,
        children: [
            { index: true, element: withSuspense(<Landing />) },
            { path: "dashboard", element: withSuspense(<Dashboard />) },
            { path: "note/:id", element: withSuspense(<NotePage />) },
            { path: "profile/:userId", element: withSuspense(<Profile />) },
        ],
    },
]);

export default router;
