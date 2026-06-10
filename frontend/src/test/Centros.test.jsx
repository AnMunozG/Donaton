import { describe, it, expect, beforeEach } from "vitest";
import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { AuthProvider } from "../componentes/AuthContext";
import Centros from "../paginas/Centros";
function TestWrapper({ children }) {
  return <MemoryRouter><AuthProvider>{children}</AuthProvider></MemoryRouter>;
}

describe("Centros", () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it("renderiza el título del banner", async () => {
    render(<TestWrapper><Centros /></TestWrapper>);
    expect(await screen.findByText("Centros de Acopio")).toBeInTheDocument();
  });

  it("renderiza el mensaje de selección cuando no hay centro elegido", async () => {
    render(<TestWrapper><Centros /></TestWrapper>);
    expect(await screen.findByText(/Selecciona un centro/)).toBeInTheDocument();
  });

  it("renderiza el texto de capacidad", async () => {
    render(<TestWrapper><Centros /></TestWrapper>);
    expect(await screen.findByText(/CENTROS ACTIVOS/)).toBeInTheDocument();
  });

  it("muestra botón de filtro Todas las regiones", async () => {
    render(<TestWrapper><Centros /></TestWrapper>);
    expect(await screen.findByText("Todas")).toBeInTheDocument();
  });
});
