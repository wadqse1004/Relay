import { Link } from "react-router-dom";

export default function Sidebar() {
  return (
    <aside>
      <h2>Relay</h2>

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