import { useNavigate } from "react-router-dom";

export default function Header() {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    navigate("/login");
  };

  return (
    <header>
      <span>Relay</span>

      <button onClick={handleLogout}>
        로그아웃
      </button>
    </header>
  );
}