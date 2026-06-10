import { describe, it, expect, beforeEach } from "vitest";
import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { AuthProvider } from "../componentes/AuthContext";
import Nosotros from "../paginas/Nosotros";
function TestWrapper({ children }) {
  return <MemoryRouter><AuthProvider>{children}</AuthProvider></MemoryRouter>;
}

describe("Nosotros", () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it("renderiza el título del hero", async () => {
    render(<TestWrapper><Nosotros /></TestWrapper>);
    expect(await screen.findByText("Acerca de Donatón")).toBeInTheDocument();
  });

  it("renderiza la sección de misión", async () => {
    render(<TestWrapper><Nosotros /></TestWrapper>);
    expect(await screen.findByText("Nuestra misión")).toBeInTheDocument();
  });

  it("renderiza la sección de historia", async () => {
    render(<TestWrapper><Nosotros /></TestWrapper>);
    expect(await screen.findByText("Nuestra historia")).toBeInTheDocument();
  });

  it("renderiza la sección de principios", async () => {
    render(<TestWrapper><Nosotros /></TestWrapper>);
    expect(await screen.findByText("Nuestros principios")).toBeInTheDocument();
  });
});
