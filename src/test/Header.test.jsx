import { describe, it, expect, beforeEach } from "vitest";
import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { AuthProvider } from "../componentes/AuthContext";
import Header from "../componentes/Header";

function TestWrapper({ children }) {
  return <MemoryRouter><AuthProvider>{children}</AuthProvider></MemoryRouter>;
}

describe("Header", () => {
  beforeEach(() => localStorage.clear());

  it("renderiza enlaces de navegación", () => {
    render(<TestWrapper><Header /></TestWrapper>);
    expect(screen.getByText("Inicio")).toBeInTheDocument();
    expect(screen.getByText("Donar")).toBeInTheDocument();
  });

  it("muestra botón de registro si no hay sesión", () => {
    render(<TestWrapper><Header /></TestWrapper>);
    expect(screen.getByText("Hacerse socio")).toBeInTheDocument();
  });

  it("muestra menú de usuario si hay sesión", () => {
    localStorage.setItem("donaton_user", JSON.stringify({ rut: "1", nombre: "Test", rol: "user" }));
    render(<TestWrapper><Header /></TestWrapper>);
    expect(screen.getByText("Test")).toBeInTheDocument();
  });

  it("no muestra Dashboard a usuario normal", () => {
    localStorage.setItem("donaton_user", JSON.stringify({ rut: "1", nombre: "Test", rol: "user" }));
    render(<TestWrapper><Header /></TestWrapper>);
    expect(screen.queryByText("Dashboard")).not.toBeInTheDocument();
  });
});
