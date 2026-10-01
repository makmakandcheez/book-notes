
import { RouterProvider } from "react-router";
import { AuthProvider } from "./features/auth/context/AuthProvider";
import router from "./router";
import './App.css'

function App() {
  return (
    <AuthProvider>
      <RouterProvider router={router} />
    </AuthProvider>
  );
}

export default App
