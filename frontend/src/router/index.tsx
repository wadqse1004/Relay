import {
  createBrowserRouter,
  Navigate,
} from "react-router-dom";

import MainLayout from "../layouts/MainLayout";
import DashboardPage from "../pages/DashboardPage";
import LoginPage from "../pages/LoginPage";

const isAuthenticated = () => {
  return Boolean(localStorage.getItem("access_token"));
};

export const router = createBrowserRouter([
  {
    path: "/login",
    element: <LoginPage />,
  },
  {
    path: "/",
    element: isAuthenticated() ? (
      <MainLayout />
    ) : (
      <Navigate to="/login" replace />
    ),
    children: [
      {
        index: true,
        element: <DashboardPage />,
      },
    ],
  },
]);