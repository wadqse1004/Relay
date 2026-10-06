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

      </div>

      <div style={{ display: "flex", gap: "12px" }}>
        <button
  type="button"
  className="relay-login-theme"
  style={{ position: "static" }}
  onClick={toggleTheme}
  aria-label={
    theme === "dark"
      ? "라이트 모드로 전환"
      : "다크 모드로 전환"
  }
  title={
    theme === "dark"
      ? "라이트 모드로 전환"
      : "다크 모드로 전환"
  }
>
  {theme === "dark" ? (
    <svg
      width="18"
      height="18"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.8"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <circle cx="12" cy="12" r="4" />
      <path d="M12 2v2" />
      <path d="M12 20v2" />
      <path d="m4.93 4.93 1.41 1.41" />
      <path d="m17.66 17.66 1.41 1.41" />
      <path d="M2 12h2" />
      <path d="M20 12h2" />
      <path d="m6.34 17.66-1.41 1.41" />
      <path d="m19.07 4.93-1.41 1.41" />
    </svg>
  ) : (
    <svg
      width="18"
      height="18"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.8"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79Z" />
    </svg>
  )}
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