import { useState, type FormEvent } from "react";
import { useNavigate } from "react-router-dom";
import { useTheme } from "../hooks/useTheme";

import { apiClient } from "../api/client";

type LoginResponse = {
  access_token: string;
  token_type: string;
};

export default function LoginPage() {
  const navigate = useNavigate();
  const { theme, toggleTheme } = useTheme();

  const [email, setEmail] = useState(() => {
    return localStorage.getItem("saved_email") ?? "";
  });

  const [password, setPassword] = useState("");

  const [rememberEmail, setRememberEmail] = useState(() => {
    return localStorage.getItem("saved_email") !== null;
  });

const [errorMessage, setErrorMessage] = useState("");

  const handleSubmit = async ( event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setErrorMessage("");

  try {
    const response = await apiClient.post<LoginResponse>(
      "/api/auth/login",
      {
        email,
        password,
      }
    );

    // JWT 저장
    localStorage.setItem(
      "access_token",
      response.data.access_token
    );

    // 아이디 저장 처리
    if (rememberEmail) {
      localStorage.setItem("saved_email", email);
    } else {
      localStorage.removeItem("saved_email");
    }

    // 로그인 성공 후 이동
    navigate("/");
  } catch {
    setErrorMessage("로그인에 실패했습니다.");
  }
};

  return (
    <div className="login-container">
      <div className="login-brand">

        <img
          src={
            theme === "dark"
              ? "/branding/relay-logo-light.png"
              : "/branding/relay-logo-dark.png"
          }
          alt="Relay"
          width={160}
        />

        <p>사람을 잇고, 업무를 흐르게</p>
    </div>

      <form className="login-form" onSubmit={handleSubmit}>
        <div>
          <label>이메일</label>
          <input
            value={email}
            onChange={(event) => setEmail(event.target.value)}
          />
        </div>

        <div>
          <label>비밀번호</label>
          <input
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
          />
        </div>

        <div>
          <label>
          <input
            type="checkbox"
            checked={rememberEmail}
            onChange={(event) =>
            setRememberEmail(event.target.checked)
            }
          />
            아이디 저장
          </label>
        </div>

        <button type="submit">로그인</button>

        {errorMessage && <p>{errorMessage}</p>}
      </form>

      <button
        type="button"
        className="theme-button"
        onClick={toggleTheme}
        style={{ marginTop: "20px" }}
      >
        {theme === "light" ? "🌙 Dark Mode" : "☀️ Light Mode"}
      </button>
    </div>
  );
}