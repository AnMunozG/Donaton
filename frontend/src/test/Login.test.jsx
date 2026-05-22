import { describe, it, expect, beforeEach } from "vitest";
import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { AuthProvider } from "../componentes/AuthContext";
import Login from "../paginas/Login";
import { seedLocalStorage } from "../componentes/Datos";

function TestWrapper({ children }) {
  return <MemoryRouter><AuthProvider>{children}</AuthProvider></MemoryRouter>;
}

describe("Login", () => {
  beforeEach(() => {
    localStorage.clear();
    seedLocalStorage();
  });

  it("renderiza el título del formulario", () => {
    render(<TestWrapper><Login /></TestWrapper>);
    expect(screen.getByRole("heading", { name: /iniciar sesión/i })).toBeInTheDocument();
  });

  it("renderiza campo de RUT", () => {
    render(<TestWrapper><Login /></TestWrapper>);
    expect(screen.getByPlaceholderText("12.345.678-K")).toBeInTheDocument();
  });

  it("renderiza campo de contraseña", () => {
    render(<TestWrapper><Login /></TestWrapper>);
    expect(screen.getByPlaceholderText("Ingresa tu contraseña")).toBeInTheDocument();
  });

  it("muestra cuentas de prueba", () => {
    render(<TestWrapper><Login /></TestWrapper>);
    expect(screen.getByText(/Admin: 111111111/)).toBeInTheDocument();
  });

  it("tiene enlace a registro", () => {
    render(<TestWrapper><Login /></TestWrapper>);
    expect(screen.getByText("Regístrate aquí")).toBeInTheDocument();
  });
});
