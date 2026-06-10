import { describe, it, expect, beforeEach } from "vitest";
import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { AuthProvider } from "../componentes/AuthContext";
import Inicio from "../paginas/Inicio";
function TestWrapper({ children }) {
  return <MemoryRouter><AuthProvider>{children}</AuthProvider></MemoryRouter>;
}

describe("Inicio", () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it("renderiza el título del banner", async () => {
    render(<TestWrapper><Inicio /></TestWrapper>);
    expect(await screen.findByText(/Coordinando la ayuda/)).toBeInTheDocument();
  });

  it("renderiza botones de acción principales", async () => {
    render(<TestWrapper><Inicio /></TestWrapper>);
    expect(await screen.findByText("Hacer una donación")).toBeInTheDocument();
    expect(await screen.findByText("Reportar una necesidad")).toBeInTheDocument();
  });

  it("renderiza sección de transparencia", async () => {
    render(<TestWrapper><Inicio /></TestWrapper>);
    expect(await screen.findByText(/Transparencia en cada donación/)).toBeInTheDocument();
  });

  it("renderiza sección de cómo funciona", async () => {
    render(<TestWrapper><Inicio /></TestWrapper>);
    expect(await screen.findByText(/¿Cómo funciona Donatón?/)).toBeInTheDocument();
  });
});
