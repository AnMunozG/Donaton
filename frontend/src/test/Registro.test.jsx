import { describe, it, expect, beforeEach } from "vitest";
import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { AuthProvider } from "../componentes/AuthContext";
import Registro from "../paginas/Registro";
import { seedLocalStorage } from "../componentes/Datos";

function TestWrapper({ children }) {
  return <MemoryRouter><AuthProvider>{children}</AuthProvider></MemoryRouter>;
}

describe("Registro", () => {
  beforeEach(() => {
    localStorage.clear();
    seedLocalStorage();
  });

  it("renderiza el título del formulario", () => {
    render(<TestWrapper><Registro /></TestWrapper>);
    expect(screen.getByText("Registro de Socios")).toBeInTheDocument();
  });

  it("renderiza campo de RUT", () => {
    render(<TestWrapper><Registro /></TestWrapper>);
    expect(screen.getByPlaceholderText("12.345.678-K")).toBeInTheDocument();
  });

  it("renderiza campo de nombre", () => {
    render(<TestWrapper><Registro /></TestWrapper>);
    expect(screen.getByPlaceholderText("Juan Pérez")).toBeInTheDocument();
  });

  it("renderiza checkbox de términos", () => {
    render(<TestWrapper><Registro /></TestWrapper>);
    expect(screen.getByText(/términos y condiciones/)).toBeInTheDocument();
  });

  it("renderiza botón de registro", () => {
    render(<TestWrapper><Registro /></TestWrapper>);
    expect(screen.getByText("Registrarse")).toBeInTheDocument();
  });
});
