import { describe, it, expect, beforeEach } from "vitest";
import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { AuthProvider } from "../componentes/AuthContext";
import Transparencia from "../paginas/Transparencia";
import { seedLocalStorage } from "../componentes/Datos";

function TestWrapper({ children }) {
  return <MemoryRouter><AuthProvider>{children}</AuthProvider></MemoryRouter>;
}

describe("Transparencia", () => {
  beforeEach(() => {
    localStorage.clear();
    seedLocalStorage();
  });

  it("renderiza el título de la página", async () => {
    render(<TestWrapper><Transparencia /></TestWrapper>);
    expect(await screen.findByText("Transparencia")).toBeInTheDocument();
  });

  it("renderiza el badge de compromiso público", async () => {
    render(<TestWrapper><Transparencia /></TestWrapper>);
    expect(await screen.findByText("COMPROMISO PÚBLICO")).toBeInTheDocument();
  });

  it("renderiza sección de impacto en números", async () => {
    render(<TestWrapper><Transparencia /></TestWrapper>);
    expect(await screen.findByText(/Nuestro impacto en números/)).toBeInTheDocument();
  });

  it("renderiza botones de navegación en hero", async () => {
    render(<TestWrapper><Transparencia /></TestWrapper>);
    expect(await screen.findByText("Ver reportes")).toBeInTheDocument();
    expect(await screen.findByText("Nuestro impacto")).toBeInTheDocument();
  });
});
