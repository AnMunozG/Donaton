import { describe, it, expect, beforeEach } from "vitest";
import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { AuthProvider } from "../componentes/AuthContext";
import Perfil from "../paginas/Perfil";
import { seedLocalStorage } from "../componentes/Datos";

function TestWrapper({ children }) {
  return <MemoryRouter><AuthProvider>{children}</AuthProvider></MemoryRouter>;
}

describe("Perfil", () => {
  beforeEach(() => {
    localStorage.clear();
    seedLocalStorage();
  });

  it("no muestra contenido de perfil si no hay sesión", () => {
    render(<TestWrapper><Perfil /></TestWrapper>);
    expect(screen.queryByText("Mi Perfil")).not.toBeInTheDocument();
  });

  it("muestra perfil si hay usuario autenticado", async () => {
    localStorage.setItem("donaton_user", JSON.stringify({ rut: "111111111", nombre: "Admin Donatón", rol: "admin", email: "admin@donaton.cl" }));
    render(<TestWrapper><Perfil /></TestWrapper>);
    expect(await screen.findByText("Mi Perfil")).toBeInTheDocument();
  });

  it("muestra el nombre del usuario en la tarjeta", async () => {
    localStorage.setItem("donaton_user", JSON.stringify({ rut: "111111111", nombre: "Admin Donatón", rol: "admin", email: "admin@donaton.cl" }));
    render(<TestWrapper><Perfil /></TestWrapper>);
    expect(await screen.findByText("Admin Donatón")).toBeInTheDocument();
  });
});
