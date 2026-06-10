import { describe, it, expect, beforeEach } from "vitest";
import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { AuthProvider } from "../componentes/AuthContext";
import Necesidades from "../paginas/Necesidades";
function TestWrapper({ children }) {
  return <MemoryRouter><AuthProvider>{children}</AuthProvider></MemoryRouter>;
}

describe("Necesidades", () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it("renderiza el título de la página", async () => {
    render(<TestWrapper><Necesidades /></TestWrapper>);
    expect(await screen.findByText("Necesidades en Terreno")).toBeInTheDocument();
  });

  it("renderiza campo de reportado por", async () => {
    render(<TestWrapper><Necesidades /></TestWrapper>);
    expect(await screen.findByText("Reportado por")).toBeInTheDocument();
  });

  it("renderiza campo de cantidad", async () => {
    render(<TestWrapper><Necesidades /></TestWrapper>);
    expect(await screen.findByText("Cantidad requerida")).toBeInTheDocument();
  });

  it("renderiza botón de enviar reporte", async () => {
    render(<TestWrapper><Necesidades /></TestWrapper>);
    expect(await screen.findByText("Enviar reporte")).toBeInTheDocument();
  });
});
