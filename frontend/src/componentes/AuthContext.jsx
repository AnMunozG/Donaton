import { createContext, useContext, useState } from "react";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    const saved = localStorage.getItem("donaton_user");
    return saved ? JSON.parse(saved) : null;
  });

  const login = (rut, nombre, rol, email, token) => {
    const u = { rut, nombre, rol, email: email || "" };
    setUser(u);
    localStorage.setItem("donaton_user", JSON.stringify(u));
    if (token) localStorage.setItem("donaton_token", token);
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem("donaton_user");
    localStorage.removeItem("donaton_token");
  };

  const updateUser = (data) => {
    const updated = { ...user, ...data };
    setUser(updated);
    localStorage.setItem("donaton_user", JSON.stringify(updated));
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, updateUser, isAuth: !!user }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
