import { Link } from "react-router-dom";
import { useTheme } from "../hooks/useTheme";

export default function Sidebar() {
  const { theme } = useTheme();

  const logoSrc =
    theme === "dark"
      ? "/branding/relay-logo-light.png"
      : "/branding/relay-logo-dark.png";

  return (
    <aside className="sidebar">
      <img
        src={logoSrc}
        alt="Relay"
        style={{
          width: "135px",
          height: "auto",
          objectFit: "contain",
        }}
      />

      <nav>
        <ul>
          <li>
            <Link to="/">Dashboard</Link>
          </li>

          <li>
            <Link to="/users">Users</Link>
          </li>

          <li>
            <Link to="/departments">Departments</Link>
          </li>
        </ul>
      </nav>
    </aside>
  );
}