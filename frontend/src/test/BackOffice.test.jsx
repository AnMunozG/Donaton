import { describe, it, expect, beforeEach } from "vitest";
import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { AuthProvider } from "../componentes/AuthContext";
import BackOffice from "../paginas/BackOffice";
function TestWrapper({ children }) {
  return <MemoryRouter><AuthProvider>{children}</AuthProvider></MemoryRouter>;
}

describe("BackOffice", () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it("renderiza tabs de navegación del dashboard", async () => {
    render(<TestWrapper><BackOffice /></TestWrapper>);
    expect(await screen.findByText("Admin Panel")).toBeInTheDocument();
    expect(screen.getByText("Donaciones")).toBeInTheDocument();
    expect(screen.getByText("Necesidades")).toBeInTheDocument();
    expect(screen.getByText("Centros")).toBeInTheDocument();
  });

  it("renderiza tab de Necesidades", async () => {
    render(<TestWrapper><BackOffice /></TestWrapper>);
    expect(await screen.findByText("Necesidades")).toBeInTheDocument();
  });

  it("renderiza tab de Centros", async () => {
    render(<TestWrapper><BackOffice /></TestWrapper>);
    expect(await screen.findByText("Centros")).toBeInTheDocument();
  });

  it("Dashboard es el tab activo por defecto", async () => {
    render(<TestWrapper><BackOffice /></TestWrapper>);
    expect(await screen.findByText("Admin Panel")).toBeInTheDocument();
  });
});
