import { Link } from "react-router-dom";

export default function Sidebar() {

  const logoSrc = "/branding/relay-logo-light.png";

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