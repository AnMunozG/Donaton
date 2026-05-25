// DATOS DE EJEMPLO 
export const centrosData = [
  {
    id: "CA-001",
    nombre: "Centro de Acopio Santiago Centro",
    region: "Metropolitana",
    direccion: "Av. Libertador Bernardo O'Higgins 1234, Santiago",
    coordenadas: { lat: -33.4489, lng: -70.6693 },
    encargado: "Carolina Méndez",
    telefono: "+56 9 8765 4321",
    capacidadTotal: 5000,
    capacidadUsada: 3200,
    inventario: [
      { tipo: "Alimentos", cantidad: "1.200 kg" },
      { tipo: "Ropa y abrigo", cantidad: "8 cajas" },
      { tipo: "Insumos médicos", cantidad: "45 unidades" },
    ],
    estado: "Activo",
  },
  {
    id: "CA-002",
    nombre: "Centro de Acopio Puente Alto",
    region: "Metropolitana",
    direccion: "Calle Los Quillayes 456, Puente Alto",
    coordenadas: { lat: -33.5929, lng: -70.5759 },
    encargado: "Roberto Soto",
    telefono: "+56 9 7654 3210",
    capacidadTotal: 3000,
    capacidadUsada: 2800,
    inventario: [
      { tipo: "Alimentos", cantidad: "900 kg" },
      { tipo: "Artículos de higiene", cantidad: "120 unidades" },
    ],
    estado: "Capacidad crítica",
  },
  {
    id: "CA-003",
    nombre: "Centro de Acopio Maipú",
    region: "Metropolitana",
    direccion: "Av. Pajaritos 789, Maipú",
    coordenadas: { lat: -33.5113, lng: -70.7567 },
    encargado: "Valentina Rojas",
    telefono: "+56 9 6543 2109",
    capacidadTotal: 4000,
    capacidadUsada: 1500,
    inventario: [
      { tipo: "Ropa y abrigo", cantidad: "15 cajas" },
      { tipo: "Utensilios del hogar", cantidad: "30 unidades" },
    ],
    estado: "Activo",
  },
  {
    id: "CA-004",
    nombre: "Centro de Acopio Valparaíso",
    region: "Valparaíso",
    direccion: "Av. Argentina 321, Valparaíso",
    coordenadas: { lat: -33.0458, lng: -71.6197 },
    encargado: "Felipe Araya",
    telefono: "+56 9 5432 1098",
    capacidadTotal: 3500,
    capacidadUsada: 700,
    inventario: [
      { tipo: "Alimentos", cantidad: "300 kg" },
      { tipo: "Insumos médicos", cantidad: "18 unidades" },
    ],
    estado: "Activo",
  },
  {
    id: "CA-005",
    nombre: "Centro de Acopio Concepción",
    region: "Biobío",
    direccion: "Av. Costanera 555, Concepción",
    coordenadas: { lat: -36.8270, lng: -73.0503 },
    encargado: "Daniela Vergara",
    telefono: "+56 9 4321 0987",
    capacidadTotal: 4500,
    capacidadUsada: 1200,
    inventario: [
      { tipo: "Alimentos", cantidad: "600 kg" },
      { tipo: "Pañales e infantiles", cantidad: "200 unidades" },
    ],
    estado: "Activo",
  },
  {
    id: "CA-006",
    nombre: "Centro de Acopio La Serena",
    region: "Coquimbo",
    direccion: "Av. Juan Bohón 888, La Serena",
    coordenadas: { lat: -29.9027, lng: -71.2520 },
    encargado: "Mauricio Olivares",
    telefono: "+56 9 3210 9876",
    capacidadTotal: 3000,
    capacidadUsada: 1800,
    inventario: [
      { tipo: "Alimentos", cantidad: "750 kg" },
      { tipo: "Ropa y abrigo", cantidad: "12 cajas" },
      { tipo: "Artículos de higiene", cantidad: "80 kits" },
    ],
    estado: "Activo",
  },
];

export const donacionesEjemplo = [
  {
    id: "DON-001",
    tipo: "Alimentos no perecibles",
    cantidad: "50",
    unidad: "kg",
    origen: "Empresa Sodimac",
    centroId: "CA-001",
    centro: "Santiago Centro",
    fecha: "2026-04-01",
    estado: "Entregado",
    detalles: {
      marca: "Marca Propia",
      fechaVencimiento: "2027-12-31",
      tipoAlimento: "Granos y legumbres",
      pesoUnitario: "1 kg",
      condicionesAlmacenamiento: "Lugar seco y fresco"
    }
  },
  {
    id: "DON-011",
    tipo: "Ropa y abrigo",
    cantidad: "30",
    unidad: "prendas",
    origen: "Voluntarios Recoleta",
    centroId: "CA-006",
    centro: "Recoleta",
    fecha: "2026-04-15",
    estado: "En acopio",
    detalles: { categoria: "Abrigo", tallas: ["Única"], genero: "Unisex", estadoPrenda: "Usada en buen estado", material: "Algodón" }
  },
  {
    id: "DON-012",
    tipo: "Alimentos no perecibles",
    cantidad: "10",
    unidad: "kg",
    origen: "222222222",
    centroId: "CA-001",
    centro: "Santiago Centro",
    fecha: "2026-05-01",
    estado: "En acopio",
    detalles: { tipoAlimento: "Granos y legumbres", fechaVencimiento: "2027-12-31", condicionesAlmacenamiento: "Lugar seco", tipoEnvase: "Bolsa sellada" }
  },
  {
    id: "DON-013",
    tipo: "Artículos de higiene",
    cantidad: "5",
    unidad: "kits",
    origen: "222222222",
    centroId: "CA-002",
    centro: "Puente Alto",
    fecha: "2026-04-28",
    estado: "Entregado",
    detalles: { tipoKit: "Higiene personal básico", contenido: ["Jabón", "Shampoo", "Pasta dental"], destinatario: "Adultos mayores", marca: "Varias" }
  },
  {
    id: "DON-014",
    tipo: "Donación Monetaria",
    cantidad: "50000",
    unidad: "$",
    origen: "222222222",
    centroId: "CA-001",
    centro: "Santiago Centro",
    fecha: "2026-04-20",
    estado: "Entregado",
    detalles: {}
  },
];

export const necesidadesEjemplo = [
  {
    id: "NEC-001",
    recurso: "Alimentos no perecibles",
    cantidad: "15",
    donado: "13",
    descripcion: "Las familias damnificadas por incendios perdieron todas sus provisiones y requieren alimentos básicos para cubrir las próximas semanas.",
    unidad: "kg",
    fecha: "2026-04-05",
    urgencia: "Alta",
    estado: "Asignado",
    centroId: "CA-001",
    centro: "Centro de Acopio Santiago Centro",
    reportadoPor: "Municipalidad de Santiago Centro",
    detalles: {
      tipoAlimento: "Granos, legumbres y aceite",
      beneficiarios: "Familias damnificadas por incendios",
      fechaEstimadaEntrega: "2026-04-10"
    }
  },
  {
    id: "NEC-002",
    recurso: "Ropa y abrigo",
    cantidad: "15",
    donado: "5",
    unidad: "prendas",
    descripcion: "Con la llegada del invierno, las personas mayores en el albergue municipal no cuentan con abrigo suficiente para las bajas temperaturas.",
    fecha: "2026-04-04",
    urgencia: "Media",
    estado: "Asignado",
    centroId: "CA-002",
    centro: "Centro de Acopio Puente Alto",
    reportadoPor: "Voluntario en terreno",
    detalles: {
      tallasNecesarias: ["S", "M", "L", "XL"],
      tipoPrenda: "Frazadas y parkas",
      beneficiarios: "Personas mayores en albergue",
      temporada: "Invierno"
    }
  },
  {
    id: "NEC-003",
    recurso: "Insumos médicos",
    cantidad: "30",
    donado: "25",
    unidad: "unidades",
    descripcion: "El centro médico local ha agotado su stock de medicamentos esenciales y requiere reposición urgente para atender a las familias del campamento.",
    fecha: "2026-04-03",
    urgencia: "Alta",
    estado: "Pendiente",
    centroId: "CA-004",
    centro: "Centro de Acopio Valparaíso",
    reportadoPor: "Centro médico local",
    detalles: {
      tipoMedicamento: "Analgésicos, antibióticos y antipiréticos",
      restricciones: "No vencidos, cajas cerradas",
      beneficiarios: "Familias del campamento"
    }
  },
  {
    id: "NEC-004",
    recurso: "Artículos de higiene",
    cantidad: "20",
    donado: "20",
    unidad: "kits",
    descripcion: "Niños y adultos mayores en situación de calle necesitan kits de higiene para mantener condiciones sanitarias dignas.",
    fecha: "2026-04-02",
    urgencia: "Baja",
    estado: "Cubierto",
    centroId: "CA-004",
    centro: "Centro de Acopio Valparaíso",
    reportadoPor: "Voluntario en terreno",
    detalles: {
      contenidoKit: ["Jabón", "Shampoo", "Pasta dental", "Toallas húmedas"],
      destinatario: "Niños y adultos mayores",
      frecuencia: "Entrega única"
    }
  },
  {
    id: "NEC-005",
    recurso: "Alimentos no perecibles",
    cantidad: "20",
    donado: "3",
    unidad: "kg",
    descripcion: "Las familias con niños pequeños del sector necesitan leche en polvo y cereales para asegurar la alimentación infantil diaria.",
    fecha: "2026-04-06",
    urgencia: "Alta",
    estado: "Asignado",
    centroId: "CA-001",
    centro: "Centro de Acopio Santiago Centro",
    reportadoPor: "Junta de vecinos",
    detalles: {
      tipoAlimento: "Leche en polvo, enlatados y cereales",
      beneficiarios: "Familias con niños pequeños",
      fechaEstimadaEntrega: "2026-04-12"
    }
  },
  {
    id: "NEC-006",
    recurso: "Artículos de higiene",
    cantidad: "40",
    donado: "36",
    descripcion: "En los albergues hay bebés y niños pequeños que requieren pañales desechables para mantener condiciones de higiene básicas.",
    unidad: "unidades",
    fecha: "2026-04-08",
    urgencia: "Alta",
    estado: "Pendiente",
    centroId: "CA-005",
    centro: "Centro de Acopio Concepción",
    reportadoPor: "Fundación Crecer",
    detalles: {
      tipoArticulo: "Pañales desechables",
      beneficiarios: "Bebés y niños pequeños en albergues",
      tallasSolicitadas: ["Recién nacido", "S", "M"]
    }
  },
  {
    id: "NEC-007",
    recurso: "Ropa y abrigo",
    cantidad: "25",
    donado: "21",
    unidad: "prendas",
    descripcion: "Las recientes lluvias torrenciales dejaron a cientos de familias damnificadas que necesitan frazadas y ropa de abrigo con urgencia.",
    fecha: "2026-04-09",
    urgencia: "Alta",
    estado: "Pendiente",
    centroId: "CA-006",
    centro: "Centro de Acopio La Serena",
    reportadoPor: "Municipalidad de La Serena",
    detalles: {
      tallasNecesarias: ["M", "L", "XL"],
      tipoPrenda: "Frazadas, chalecos y parkas",
      beneficiarios: "Familias damnificadas por lluvias",
      temporada: "Invierno"
    }
  },
  {
    id: "NEC-008",
    recurso: "Alimentos no perecibles",
    cantidad: "30",
    donado: "15",
    unidad: "kg",
    descripcion: "Los adultos mayores del sector viven solos y requieren alimentos no perecibles para complementar su alimentación diaria.",
    fecha: "2026-04-09",
    urgencia: "Media",
    estado: "Asignado",
    centroId: "CA-006",
    centro: "Centro de Acopio La Serena",
    reportadoPor: "Junta de vecinos Cerro Grande",
    detalles: {
      tipoAlimento: "Enlatados, pastas y aceite",
      beneficiarios: "Adultos mayores del sector",
      fechaEstimadaEntrega: "2026-04-15"
    }
  },
  {
    id: "NEC-009",
    recurso: "Artículos de higiene",
    cantidad: "15",
    donado: "5",
    unidad: "kits",
    descripcion: "Las familias realojadas tras los desbordes necesitan kits de higiene para restablecer sus condiciones sanitarias básicas.",
    fecha: "2026-04-10",
    urgencia: "Baja",
    estado: "Pendiente",
    centroId: "CA-006",
    centro: "Centro de Acopio La Serena",
    reportadoPor: "Voluntario en terreno",
    detalles: {
      contenidoKit: ["Jabón", "Shampoo", "Pasta dental", "Toalla", "Pañales"],
      destinatario: "Familias realojadas",
      frecuencia: "Entrega única"
    }
  },
];



export const tiposRecurso = [
  "Alimentos no perecibles",
  "Insumos médicos",
  "Artículos de higiene",
  "Ropa y abrigo",
  "Donación Monetaria",
  "Utensilios del hogar",
];

export const unidadesPorTipo = {
  "Alimentos no perecibles": ["kg", "unidades", "cajas"],
  "Insumos médicos": ["unidades", "cajas", "sobres"],
  "Artículos de higiene": ["unidades", "kits", "cajas"],
  "Ropa y abrigo": ["prendas", "cajas", "kits"],
  "Donación Monetaria": ["CLP", "USD"],
  "Utensilios del hogar": ["unidades", "juegos", "cajas"],
};

// Campos adicionales por tipo de donación (más relevantes para la organización)
export const camposPorTipo = {
  "Alimentos no perecibles": [
    { name: "tipoAlimento", label: "Tipo de alimento", type: "select", options: ["Granos y legumbres", "Enlatados", "Aceites y condimentos", "Harinas y cereales", "Alimento infantil", "Otros"] },
    { name: "fechaVencimiento", label: "Fecha de vencimiento", type: "date" },
    { name: "condicionesAlmacenamiento", label: "Condiciones de almacenamiento", type: "select", options: ["Temperatura ambiente", "Refrigerado", "Lugar seco", "No aplica"] },
    { name: "tipoEnvase", label: "Tipo de envase", type: "select", options: ["Bolsa sellada", "Lata", "Caja", "Botella", "Otro"] },
  ],
  "Insumos médicos": [
    { name: "tipoInsumo", label: "Tipo de insumo", type: "select", options: ["Medicamentos", "Material de curación", "Equipos médicos", "Insumos de protección", "Oxígeno y respiración"] },
    { name: "fechaVencimiento", label: "Fecha de vencimiento", type: "date" },
    { name: "registroISP", label: "Registro ISP (si aplica)", type: "text", placeholder: "Ej: ISP-XXXXX" },
    { name: "condicionesAlmacenamiento", label: "Condiciones de almacenamiento", type: "select", options: ["Temperatura ambiente", "Cadena de frío", "Protegido de luz", "No aplica"] },
    { name: "esterilizado", label: "¿Viene esterilizado?", type: "select", options: ["Sí", "No", "No aplica"] },
  ],
  "Artículos de higiene": [
    { name: "tipoArticulo", label: "Tipo de artículo", type: "select", options: ["Kit personal", "Kit familiar", "Papel higiénico", "Jabones y shampoos", "Pañales", "Toallas femeninas", "Cepillos de dientes"] },
    { name: "cantidadPorUnidad", label: "Cantidad por unidad", type: "text", placeholder: "Ej: 6 unidades" },
    { name: "destinatario", label: "Destinatario preferente", type: "select", options: ["Niños", "Adultos", "Adultos mayores", "Familias", "Cualquiera"] },
  ],
  "Ropa y abrigo": [
    { name: "categoria", label: "Categoría", type: "select", options: ["Ropa interior", "Ropa exterior", "Abrigo", "Calzado", "Accesorios", "Frazadas y mantas"] },
    { name: "talla", label: "Talla(s)", type: "select", options: ["XS", "S", "M", "L", "XL", "XXL", "Única"] },
    { name: "genero", label: "Género", type: "select", options: ["Femenino", "Masculino", "Unisex", "Niños", "Niñas"] },
    { name: "estadoPrenda", label: "Estado de la prenda", type: "select", options: ["Nueva con etiqueta", "Nueva sin etiqueta", "Semi-nueva", "Usada en buen estado"] },
    { name: "temporada", label: "Temporada", type: "select", options: ["Invierno", "Verano", "Todo el año"] },
  ],
  "Donación Monetaria": [
    { name: "metodoPago", label: "Método de pago", type: "select", options: ["Transferencia bancaria", "Tarjeta débito/crédito", "Efectivo", "Otro"] },
    { name: "monto", label: "Monto en CLP", type: "text", placeholder: "Ej: 50000" },
    { name: "comprobante", label: "N° comprobante o referencia", type: "text", placeholder: "Ej: TRANS-2026-001" },
  ],
  "Utensilios del hogar": [
    { name: "categoria", label: "Categoría", type: "select", options: ["Ollas y sartenes", "Platos y cubiertos", "Electrodomésticos", "Muebles pequeños", "Ropa de cama", "Otros"] },
    { name: "estadoUtensilio", label: "Estado", type: "select", options: ["Nuevo", "Semi-nuevo", "Usado en buen estado"] },
    { name: "material", label: "Material predominante", type: "text", placeholder: "Ej: Acero inoxidable, Plástico" },
  ],
};

export const categoriasDonacion = [
  {
    icon: "bi-basket2-fill",
    nombre: "Alimentos",
    descripcion: "Alimentos no perecibles, conservas y productos básicos de primera necesidad.",
  },
  {
    icon: "bi-bandaid-fill",
    nombre: "Insumos médicos",
    descripcion: "Medicamentos, material de curación y equipos de primeros auxilios.",
  },
  {
    icon: "bi-droplet-fill",
    nombre: "Higiene",
    descripcion: "Artículos de aseo personal, pañales, papel higiénico y jabón.",
  },
  {
    icon: "bi-bag-fill",
    nombre: "Ropa y abrigo",
    descripcion: "Ropa de todo tipo, frazadas, sleeping y artículos de abrigo.",
  },
  {
    icon: "bi-currency-dollar",
    nombre: "Donaciones monetarias",
    descripcion: "Donaciones monetarias para compras directas según necesidades específicas.",
  },
  {
    icon: "bi-house-fill",
    nombre: "Utensilios del hogar",
    descripcion: "Ollas, platos, cubiertos y elementos básicos para el hogar.",
  },
];

// Cuentas de prueba para Login
export const cuentas = [
  { rut: "111111111", password: "admin1234", rol: "admin", nombre: "Admin Donatón", email: "admin@donaton.cl" },
  { rut: "222222222", password: "user1234", rol: "user", nombre: "Usuario Ejemplo", email: "usuario@donaton.cl" },
];

export const team = [
  { nombre: "Angel Exzequiel Muñoz González", rol: "Desarrollador Frontend", icono: "bi-code-slash", color: "#DD4444" },
  { nombre: "Yasser Antonio Yamil Illanes", rol: "Desarrollador Backend", icono: "bi-server", color: "#3AB795" },
  { nombre: "Martin Ignacio Pizarro Estay", rol: "Desarrollador Backend", icono: "bi-database-gear", color: "#F48080" },
];

export const valores = [
  { icon: "bi-transparency", titulo: "Transparencia", texto: "Cada donación es rastreable desde el origen hasta su entrega. Nadie queda en la oscuridad." },
  { icon: "bi-shield-check", titulo: "Seguridad", texto: "Protegemos los datos de donantes y beneficiarios con autenticación centralizada y acceso controlado." },
  { icon: "bi-arrow-repeat", titulo: "Sostenibilidad", texto: "Nuestra arquitectura modular permite crecer sin comprometer la operación actual de la organización." },
  { icon: "bi-people-fill", titulo: "Coordinación", texto: "Conectamos donantes, empresas, municipalidades y equipos logísticos en un único sistema integrado." },
];

export const hitos = [
  { year: "2023", titulo: "Fundación de Donatón", texto: "Nace como proyecto universitario para resolver el caos logístico en emergencias." },
  { year: "2024", titulo: "Primeros centros activos", texto: "Integramos 12 centros de acopio en la Región Metropolitana con trazabilidad completa." },
  { year: "2025", titulo: "Expansión nacional", texto: "Llegamos a 38 centros activos en 6 regiones del país, con más de 5.200 familias beneficiadas." },
  { year: "2026", titulo: "Plataforma integral", texto: "Lanzamos back-office, transparencia pública y reportes en tiempo real para toda la comunidad." },
];

export const impactoStats = [
  { icono: "bi-heart-fill", valor: "$12.400 M", texto: "Donaciones recibidas", detalle: "Acumulado 2024-2026" },
  { icono: "bi-building-fill", valor: "38", texto: "Centros de acopio", detalle: "Activos en todo Chile" },
  { icono: "bi-people-fill", valor: "5.200+", texto: "Familias beneficiadas", detalle: "Directamente impactadas" },
  { icono: "bi-truck", valor: "920", texto: "Envíos completados", detalle: "Con éxito a destino" },
  { icono: "bi-graph-up-arrow", valor: "94%", texto: "Eficiencia operativa", detalle: "Recursos a destino final" },
  { icono: "bi-currency-dollar", valor: "$0", texto: "Gastos administrativos", detalle: "100% voluntario" },
];

export const distribucionFondos = [
  { concepto: "Ayuda directa a familias", porcentaje: 78, color: "#DD4444" },
  { concepto: "Logística y transporte", porcentaje: 12, color: "#F48080" },
  { concepto: "Capacitación voluntarios", porcentaje: 6, color: "#3AB795" },
  { concepto: "Administración", porcentaje: 4, color: "#194B4F" },
];

export const reportes = [
  { titulo: "Reporte Anual 2025", fecha: "Enero 2026", tipo: "PDF", size: "2.4 MB", icono: "bi-file-earmark-pdf-fill", color: "#DD4444" },
  { titulo: "Estado Financiero Q4 2025", fecha: "Diciembre 2025", tipo: "PDF", size: "1.8 MB", icono: "bi-file-earmark-pdf-fill", color: "#DD4444" },
  { titulo: "Balance Social 2025", fecha: "Noviembre 2025", tipo: "PDF", size: "3.1 MB", icono: "bi-file-earmark-pdf-fill", color: "#DD4444" },
  { titulo: "Auditoría Externa 2025", fecha: "Octubre 2025", tipo: "PDF", size: "4.2 MB", icono: "bi-file-earmark-check-fill", color: "#3AB795" },
  { titulo: "Informe de Impacto por Región", fecha: "Septiembre 2025", tipo: "XLSX", size: "1.2 MB", icono: "bi-file-earmark-spreadsheet-fill", color: "#194B4F" },
  { titulo: "Memoria de Gestión 2024-2025", fecha: "Agosto 2025", tipo: "PDF", size: "5.7 MB", icono: "bi-file-earmark-text-fill", color: "#F48080" },
];

export const gobernanza = [
  { nombre: "Angel Exzequiel Muñoz González", cargo: "Lider Corporativo", img: 'https://i.imgflip.com/9e4vwk.jpg' },
  { nombre: "Yasser Antonio Yamil Illanes", cargo: "Lider de Operaciones y Logistica", img: 'https://i.ytimg.com/vi/amp6D_XRH3I/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLAC8O1bG0zD7RxQ6nG6d50a7j1dIQ' },
  { nombre: "Martin Ignacio Pizarro Estay", cargo: "Lider de Relaciones Públicas", img: 'https://media.tenor.com/ThwiQuVpaicAAAAM/cat-licking-a-lollipop-and-being-super-cool.gif' },
];

export const pasosFuncionamiento = [
  { num: "1", icon: "bi-gift-fill", titulo: "Realizas tu donación", texto: "Solo respondes un formulario corto con el tipo de recurso, cantidad, etc. Todo queda documentado en el sistema." },
  { num: "2", icon: "bi-building-fill", titulo: "Asignación al centro", texto: "La plataforma asigna tu donación al centro de acopio que más necesita de tu donación." },
  { num: "3", icon: "bi-truck", titulo: "Logística y traslado", texto: "El equipo logístico de Donatón gestiona el transporte y la distribución a los centros." },
  { num: "4", icon: "bi-check-circle-fill", titulo: "Confirmación de entrega", texto: "Te informaremos cuando tu donación llegue a aquellos que lo necesitan." },
];

export const estadoColor = {
  "Entregado": "#3AB795",
  "En tránsito": "#0dcaf0",
  "En acopio": "#FFC107",
  "Pendiente": "#DD4444",
  "Asignado": "#0d6efd",
  "Cubierto": "#3AB795",
};

export const CHART_COLORS = ["#DD4444", "#F48080", "#3AB795", "#194B4F"];

export const urgenciaColorMap = { Alta: "danger", Media: "warning", Baja: "secondary" };
export const estadoNecColorMap = { Pendiente: "danger", Asignado: "warning", Cubierto: "success" };

// ── LocalStorage persistence ──────────────────────────────

const P = "donaton_";

export function seedLocalStorage() {
  if (localStorage.getItem(P + "seeded")) return;
  localStorage.setItem(P + "centros", JSON.stringify(centrosData));
  localStorage.setItem(P + "donaciones", JSON.stringify(donacionesEjemplo));
  localStorage.setItem(P + "necesidades", JSON.stringify(necesidadesEjemplo));

  localStorage.setItem(P + "cuentas", JSON.stringify(cuentas));
  localStorage.setItem(P + "user_needs", JSON.stringify([]));
  localStorage.setItem(P + "user_need_counter", "0");
  localStorage.setItem(P + "seeded", "true");
}

export function loadFromStorage(key) {
  const raw = localStorage.getItem(P + key);
  return raw ? JSON.parse(raw) : null;
}

export function saveToStorage(key, data) {
  localStorage.setItem(P + key, JSON.stringify(data));
}

// ── User-submitted needs (localStorage-backed) ────────────

export function agregarNecesidadUsuario(data) {
  const needs = loadFromStorage("user_needs") || [];
  const counter = parseInt(localStorage.getItem(P + "user_need_counter") || "0", 10) + 1;
  localStorage.setItem(P + "user_need_counter", String(counter));
  const necesidad = {
    id: `USR-NEC-${String(counter).padStart(3, "0")}`,
    ...data,
    donado: "0",
    urgencia: "",
    estado: "Pendiente",
    fecha: new Date().toISOString().split("T")[0],
  };
  needs.push(necesidad);
  saveToStorage("user_needs", needs);
  return necesidad;
}

export function getNecesidadesUsuario() {
  return loadFromStorage("user_needs") || [];
}

export function eliminarNecesidadUsuario(id) {
  const needs = loadFromStorage("user_needs") || [];
  saveToStorage("user_needs", needs.filter((n) => n.id !== id));
}

export function actualizarNecesidadUsuario(id, data) {
  const needs = loadFromStorage("user_needs") || [];
  const idx = needs.findIndex((n) => n.id === id);
  if (idx === -1) return null;
  Object.assign(needs[idx], data);
  saveToStorage("user_needs", needs);
  return needs[idx];
}