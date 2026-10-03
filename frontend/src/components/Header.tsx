import { useNavigate } from "react-router-dom";
import { useTheme } from "../hooks/useTheme";

export default function Header() {
  const navigate = useNavigate();

  const { theme, toggleTheme } = useTheme();

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    navigate("/login");
  };

  return (
    <header className="main-header">
      <div>
      <img
        src="/branding/relay-symbol.png"
        alt="Relay Symbol"
        width={64}
      />

      <span>Relay</span>
      </div>

      <div style={{ display: "flex", gap: "12px" }}>
        <button
          className="theme-button"
          onClick={toggleTheme}
        >
          {theme === "light" ? "🌙 Dark" : "☀️ Light"}
        </button>

        <button
          className="theme-button"
          onClick={handleLogout}
        >
          로그아웃
        </button>
      </div>
    </header>
  );
}