import { Outlet } from "react-router-dom";

import Header from "../components/Header";
import Sidebar from "../components/Sidebar";

export default function MainLayout() {
  return (
    <div>
      <Header />

      <div>
        <Sidebar />

        <main>
          <Outlet />
        </main>
      </div>
    </div>
  );
}