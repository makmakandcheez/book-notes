import { lazy } from "react";

export const Landing = lazy(() => import("./features/landing/routes/Landing"));
export const Dashboard = lazy(() => import("./features/notes/routes/Dashboard"));
export const NotePage = lazy(() => import("./features/notes/routes/NotePage"));
export const Profile = lazy(() => import("./features/users/routes/Profile"));
