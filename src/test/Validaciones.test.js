import { describe, it, expect } from "vitest";
import {
  validarRut, validarRequerido, validarEnteroPositivo,
  validarEmail, validarPassword, validarConfirmacion,
  formatearRut, limpiarRut, validarForm,
} from "../componentes/Validaciones.js";

describe("validarRut", () => {
  it("rechaza RUT vacío", () => expect(validarRut("")).toBe("RUT requerido"));
  it("rechaza RUT inválido", () => expect(validarRut("1")).toBe("RUT inválido"));
  it("acepta RUT válido 111111111", () => expect(validarRut("111111111")).toBe(""));
  it("acepta RUT con K 222222222", () => expect(validarRut("222222222")).toBe(""));
});

describe("validarRequerido", () => {
  it("rechaza vacío", () => expect(validarRequerido("", "Campo")).toBe("Campo requerido"));
  it("rechaza solo espacios", () => expect(validarRequerido("   ", "Campo")).toBe("Campo requerido"));
  it("acepta valor", () => expect(validarRequerido("hola", "Campo")).toBe(""));
});

describe("validarEnteroPositivo", () => {
  it("acepta vacío", () => expect(validarEnteroPositivo("", "Cant")).toBe(""));
  it("rechaza decimal", () => expect(validarEnteroPositivo("1.5", "Cant")).toBe("Cant debe ser un número entero positivo"));
  it("acepta entero", () => expect(validarEnteroPositivo("10", "Cant")).toBe(""));
});

describe("validarEmail", () => {
  it("rechaza vacío", () => expect(validarEmail("")).toBe("Correo requerido"));
  it("rechaza sin @", () => expect(validarEmail("hola")).toBe("Correo electrónico inválido"));
  it("acepta válido", () => expect(validarEmail("a@b.cl")).toBe(""));
});

describe("validarPassword", () => {
  it("rechaza vacío", () => expect(validarPassword("")).toBe("Contraseña requerida"));
  it("rechaza corta", () => expect(validarPassword("1234567")).toBe("La contraseña debe tener al menos 8 caracteres"));
  it("acepta 8+", () => expect(validarPassword("12345678")).toBe(""));
});

describe("validarConfirmacion", () => {
  it("rechaza vacío", () => expect(validarConfirmacion("pass", "")).toBe("Confirma tu contraseña"));
  it("rechaza distinto", () => expect(validarConfirmacion("pass", "other")).toBe("Las contraseñas no coinciden"));
  it("acepta igual", () => expect(validarConfirmacion("pass", "pass")).toBe(""));
});

describe("formatearRut / limpiarRut", () => {
  it("formatea RUT", () => expect(formatearRut("111111111")).toBe("11.111.111-1"));
  it("limpia RUT", () => expect(limpiarRut("11.111.111-1")).toBe("111111111"));
});

describe("validarForm", () => {
  const reglas = [
    { campo: "nombre", nombre: "Nombre", validaciones: [validarRequerido] },
    { campo: "edad", nombre: "Edad", validaciones: [validarEnteroPositivo] },
  ];
  it("retorna errores", () => {
    const err = validarForm({ nombre: "", edad: "1.5" }, reglas);
    expect(err.nombre).toBe("Nombre requerido");
    expect(err.edad).toBe("Edad debe ser un número entero positivo");
  });
  it("retorna vacío si ok", () => expect(validarForm({ nombre: "a", edad: "10" }, reglas)).toEqual({}));
});
