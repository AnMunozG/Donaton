import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { AuthProvider } from "../componentes/AuthContext";
import Footer from "../componentes/Footer";

function TestWrapper({ children }) {
  return <MemoryRouter><AuthProvider>{children}</AuthProvider></MemoryRouter>;
}

describe("Footer", () => {
  it("renderiza enlaces de navegación", () => {
    render(<TestWrapper><Footer /></TestWrapper>);
    expect(screen.getByText("Navegación")).toBeInTheDocument();
    expect(screen.getByText("Inicio")).toBeInTheDocument();
  });

  it("renderiza información de contacto", () => {
    render(<TestWrapper><Footer /></TestWrapper>);
    expect(screen.getByText("Contacto")).toBeInTheDocument();
  });

  it("renderiza enlace a Duoc", () => {
    render(<TestWrapper><Footer /></TestWrapper>);
    expect(screen.getByText("Duoc UC")).toBeInTheDocument();
  });

  it("renderiza sección de redes sociales", () => {
    render(<TestWrapper><Footer /></TestWrapper>);
    expect(screen.getByText("Síguenos")).toBeInTheDocument();
  });
});
