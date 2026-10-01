import { useState, type FormEvent } from "react";
import { useNavigate } from "react-router-dom";

import { apiClient } from "../api/client";

type LoginResponse = {
  access_token: string;
  token_type: string;
};

export default function LoginPage() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("developer@relay.local");
  const [password, setPassword] = useState("password123");
  const [errorMessage, setErrorMessage] = useState("");

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
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

      localStorage.setItem(
        "access_token",
        response.data.access_token
      );

      navigate("/");
    } catch {
      setErrorMessage("로그인에 실패했습니다.");
    }
  };

  return (
    <div>
      <h1>Relay Login</h1>

      <form onSubmit={handleSubmit}>
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

        <button type="submit">로그인</button>

        {errorMessage && <p>{errorMessage}</p>}
      </form>
    </div>
  );
}