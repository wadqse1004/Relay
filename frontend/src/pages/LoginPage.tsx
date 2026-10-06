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
  className="relay-login-theme"
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
    </div>
  );
}