export function validarRut(rut) {
  if (!rut) return "RUT requerido";
  const soloDigitos = rut.replace(/[^0-9kK]/g, "");
  if (soloDigitos.length < 2) return "RUT inválido";
  const dv = soloDigitos.slice(-1).toUpperCase();
  const cuerpo = soloDigitos.slice(0, -1);
  if (!/^\d+$/.test(cuerpo)) return "RUT inválido";
  let suma = 0;
  let multiplicador = 2;
  for (let i = cuerpo.length - 1; i >= 0; i--) {
    suma += parseInt(cuerpo[i]) * multiplicador;
    multiplicador = multiplicador === 7 ? 2 : multiplicador + 1;
  }
  const resto = 11 - (suma % 11);
  const dvEsperado = resto === 11 ? "0" : resto === 10 ? "K" : String(resto);
  if (dv !== dvEsperado) return "RUT inválido";
  return "";
}

export function validarRequerido(valor, nombre) {
  if (!valor || (typeof valor === "string" && !valor.trim())) return `${nombre} requerido`;
  return "";
}

export function validarEnteroPositivo(valor, nombre) {
  if (!valor) return "";
  const num = Number(valor);
  if (!Number.isInteger(num) || num < 1) return `${nombre} debe ser un número entero positivo`;
  return "";
}

export function validarEmail(email) {
  if (!email) return "Correo requerido";
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return "Correo electrónico inválido";
  return "";
}

export function validarPassword(password) {
  if (!password) return "Contraseña requerida";
  if (password.length < 8) return "La contraseña debe tener al menos 8 caracteres";
  return "";
}

export function validarConfirmacion(password, confirmacion) {
  if (!confirmacion) return "Confirma tu contraseña";
  if (password !== confirmacion) return "Las contraseñas no coinciden";
  return "";
}

export function formatearRut(valor) {
  const soloDigitos = valor.replace(/[^0-9kK]/g, "").toUpperCase();
  if (!soloDigitos) return "";
  if (soloDigitos.length <= 1) return soloDigitos;
  const dv = soloDigitos.slice(-1);
  const cuerpo = soloDigitos.slice(0, -1);
  const cuerpoFormateado = cuerpo.replace(/\B(?=(\d{3})+(?!\d))/g, ".");
  return `${cuerpoFormateado}-${dv}`;
}

export function limpiarRut(valor) {
  return valor.replace(/[^0-9kK]/g, "").toUpperCase();
}

export function validarForm(form, reglas) {
  const errores = {};
  for (const { campo, nombre, validaciones } of reglas) {
    for (const fn of validaciones) {
      const msg = fn(form[campo], nombre);
      if (msg) {
        errores[campo] = msg;
        break;
      }
    }
  }
  return errores;
}
