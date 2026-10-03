import {
  useEffect,
  useState,
  type ReactNode,
} from "react";

import {
  ThemeContext,
  type Theme,
} from "./ThemeContext";

type ThemeProviderProps = {
  children: ReactNode;
};

export default function ThemeProvider({
  children,
}: ThemeProviderProps) {

  // 브라우저에 저장된 테마 불러오기
  const [theme, setTheme] = useState<Theme>(() => {
    const savedTheme = localStorage.getItem("relay_theme");

    return savedTheme === "dark" ? "dark" : "light";
  });

  // 테마가 변경될 때마다 실행
  useEffect(() => {
    document.documentElement.dataset.theme = theme;

    localStorage.setItem("relay_theme", theme);
  }, [theme]);

  // Light ↔ Dark 전환
  const toggleTheme = () => {
    setTheme((prev) =>
      prev === "light" ? "dark" : "light"
    );
  };

  return (
    <ThemeContext.Provider
      value={{
        theme,
        toggleTheme,
      }}
    >
      {children}
    </ThemeContext.Provider>
  );
}