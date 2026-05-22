import { describe, it, expect, beforeEach } from "vitest";
import { render, screen } from "@testing-library/react";
import { createMemoryRouter, RouterProvider } from "react-router-dom";
import { AuthProvider } from "../componentes/AuthContext";
import Donacion from "../paginas/Donacion";
import { seedLocalStorage } from "../componentes/Datos";

function TestWrapper({ children }) {
  const router = createMemoryRouter([{ path: "*", element: <AuthProvider>{children}</AuthProvider> }]);
  return <RouterProvider router={router} />;
}

describe("Donacion", () => {
  beforeEach(() => {
    localStorage.clear();
    seedLocalStorage();
  });

  it("renderiza el título de gestión de donaciones", async () => {
    render(<TestWrapper><Donacion /></TestWrapper>);
    expect(await screen.findByText("Gestión de Donaciones")).toBeInTheDocument();
  });

  it("renderiza selector de tipo de donante", async () => {
    render(<TestWrapper><Donacion /></TestWrapper>);
    expect(await screen.findByText("Tipo de donante")).toBeInTheDocument();
  });

  it("renderiza campo de RUT", async () => {
    render(<TestWrapper><Donacion /></TestWrapper>);
    expect(await screen.findByPlaceholderText("12.345.678-K")).toBeInTheDocument();
  });

  it("renderiza botón de registrar donación", async () => {
    render(<TestWrapper><Donacion /></TestWrapper>);
    expect(await screen.findByText("Registrar donación")).toBeInTheDocument();
  });
});
