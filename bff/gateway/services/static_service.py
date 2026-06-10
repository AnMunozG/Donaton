from ..clients import logistica_client

REGIONES = [
    "Arica y Parinacota", "Tarapacá", "Antofagasta", "Atacama",
    "Coquimbo", "Valparaíso", "Metropolitana de Santiago", "O'Higgins",
    "Maule", "Ñuble", "Biobío", "La Araucanía", "Los Ríos",
    "Los Lagos", "Aysén del General Carlos Ibáñez del Campo",
    "Magallanes y de la Antártica Chilena",
]

CATEGORIAS_DONACION = [
    {"code": "alimentos", "nombre": "Alimentos no perecibles", "icono": "bi-basket-fill", "descripcion": "Arroz, fideos, legumbres, aceite, leche en polvo"},
    {"code": "ropa", "nombre": "Ropa y abrigo", "icono": "bi-handbag-fill", "descripcion": "Chaquetas, frazadas, calcetines, zapatos"},
    {"code": "medicamentos", "nombre": "Insumos médicos", "icono": "bi-heart-pulse-fill", "descripcion": "Vendas, alcohol, paracetamol, mascarillas"},
    {"code": "higiene", "nombre": "Higiene personal", "icono": "bi-droplet-fill", "descripcion": "Jabón, pasta dental, pañales, toallitas"},
    {"code": "dinero", "nombre": "Donación Monetaria", "icono": "bi-cash-coin", "descripcion": "Aporte económico vía transferencia o webpay"},
    {"code": "otros", "nombre": "Otros", "icono": "bi-box-seam-fill", "descripcion": "Muebles, útiles de aseo, agua embotellada"},
]

PASOS_FUNCIONAMIENTO = [
    {"code": "p1", "paso": 1, "titulo": "Regístrate", "descripcion": "Crea una cuenta como donante o voluntario."},
    {"code": "p2", "paso": 2, "titulo": "Elige cómo ayudar", "descripcion": "Selecciona una campaña, centro o necesidad activa."},
    {"code": "p3", "paso": 3, "titulo": "Coordina tu aporte", "descripcion": "Define monto, artículos o tiempo según tu elección."},
    {"code": "p4", "paso": 4, "titulo": "Sigue el impacto", "descripcion": "Recibe actualizaciones y mira el impacto de tu ayuda."},
]

IMPACTO_STATS = [
    {"code": "s1", "valor": "12.400+", "label": "Donaciones recibidas", "icono": "bi-gift-fill"},
    {"code": "s2", "valor": "38", "label": "Centros activos", "icono": "bi-building-fill"},
    {"code": "s3", "valor": "5.200+", "label": "Familias beneficiadas", "icono": "bi-people-fill"},
    {"code": "s4", "valor": "920", "label": "Voluntarios activos", "icono": "bi-person-arms-up"},
    {"code": "s5", "valor": "$12.400 M", "label": "Fondos recaudados", "icono": "bi-cash-stack"},
    {"code": "s6", "valor": "120+", "label": "Empresas aliadas", "icono": "bi-building-gear"},
]

DISTRIBUCION_FONDOS = [
    {"code": "df1", "label": "Ayuda directa", "porcentaje": 75},
    {"code": "df2", "label": "Logística", "porcentaje": 12},
    {"code": "df3", "label": "Administración", "porcentaje": 8},
    {"code": "df4", "label": "Campañas futuras", "porcentaje": 5},
]

REPORTES = [
    {"code": "r1", "titulo": "Reporte Anual 2025", "fecha": "2026-01-15", "tipo": "PDF", "size": "2.4 MB", "icono": "bi-filetype-pdf", "color": "#e63946"},
    {"code": "r2", "titulo": "Auditoría Financiera 2025", "fecha": "2026-02-10", "tipo": "PDF", "size": "1.8 MB", "icono": "bi-filetype-pdf", "color": "#e63946"},
    {"code": "r3", "titulo": "Impacto Social 2025", "fecha": "2026-03-05", "tipo": "PDF", "size": "3.1 MB", "icono": "bi-filetype-pdf", "color": "#457b9d"},
    {"code": "r4", "titulo": "Detalle de Gastos 2025", "fecha": "2026-03-20", "tipo": "XLSX", "size": "856 KB", "icono": "bi-filetype-xlsx", "color": "#2d6a4f"},
    {"code": "r5", "titulo": "Listado de Centros 2025", "fecha": "2026-04-01", "tipo": "XLSX", "size": "420 KB", "icono": "bi-filetype-xlsx", "color": "#2d6a4f"},
    {"code": "r6", "titulo": "Memoria Anual 2024", "fecha": "2025-06-30", "tipo": "PDF", "size": "4.2 MB", "icono": "bi-filetype-pdf", "color": "#e63946"},
]

GOBERNANZA = [
    {"code": "g1", "nombre": "María González", "cargo": "Directora Ejecutiva", "img_url": "https://i.imgflip.com/9e4vwk.jpg"},
    {"code": "g2", "nombre": "Carlos Muñoz", "cargo": "Director Financiero", "img_url": "https://i.ytimg.com/vi/amp6D_XRH3I/hq720.jpg"},
    {"code": "g3", "nombre": "Ana Soto", "cargo": "Directora de Operaciones", "img_url": "https://media.tenor.com/ThwiQuVpaicAAAAM/cat-licking-a-lollipop-and-being-super-cool.gif"},
]

EQUIPO = [
    {"code": "t1", "nombre": "Usuario 1", "cargo": "Administrador", "email": "admin@donaton.cl", "foto_url": "", "activo": True},
    {"code": "t2", "nombre": "Usuario 2", "cargo": "Donante", "email": "user@donaton.cl", "foto_url": "", "activo": True},
    {"code": "t3", "nombre": "Usuario 3", "cargo": "Voluntario", "email": "voluntario@donaton.cl", "foto_url": "", "activo": True},
]

VALORES = [
    {"code": "v1", "titulo": "Empatía", "descripcion": "Ponemos a las personas en el centro de nuestras acciones.", "icono": "bi-heart-fill"},
    {"code": "v2", "titulo": "Transparencia", "descripcion": "Cada recurso tiene un destino claro y verificable.", "icono": "bi-eye-fill"},
    {"code": "v3", "titulo": "Eficiencia", "descripcion": "Optimizamos cada recurso para maximizar el impacto.", "icono": "bi-graph-up-arrow"},
    {"code": "v4", "titulo": "Colaboración", "descripcion": "Juntos multiplicamos la ayuda.", "icono": "bi-people-fill"},
]

HITOS = [
    {"code": "h1", "year": "2023", "titulo": "Fundación", "descripcion": "Nacimos con la misión de conectar donantes con centros de acopio.", "tipo": "fundacion"},
    {"code": "h2", "year": "2024", "titulo": "Primeros 10 centros", "descripcion": "Logramos activar 10 centros de acopio en la Región Metropolitana.", "tipo": "expansion"},
    {"code": "h3", "year": "2025", "titulo": "+5000 donaciones", "descripcion": "Alcanzamos las 5.000 donaciones gestionadas a nivel nacional.", "tipo": "logro"},
    {"code": "h4", "year": "2026", "titulo": "Cobertura nacional", "descripcion": "Proyectamos llegar a todas las regiones de Chile.", "tipo": "meta"},
]


UNIDADES_POR_TIPO = {
    "Alimentos no perecibles": ["kg", "unidades", "cajas"],
    "Insumos médicos": ["unidades", "cajas", "sobres"],
    "Artículos de higiene": ["unidades", "kits", "cajas"],
    "Ropa y abrigo": ["prendas", "cajas", "kits"],
    "Donación Monetaria": ["CLP", "USD"],
    "Utensilios del hogar": ["unidades", "juegos", "cajas"],
}

CAMPOS_POR_TIPO = {
    "Alimentos no perecibles": [
        {"name": "tipoAlimento", "label": "Tipo de alimento", "type": "select", "options": ["Granos y legumbres", "Enlatados", "Aceites y condimentos", "Harinas y cereales", "Alimento infantil", "Otros"]},
        {"name": "fechaVencimiento", "label": "Fecha de vencimiento", "type": "date"},
        {"name": "condicionesAlmacenamiento", "label": "Condiciones de almacenamiento", "type": "select", "options": ["Temperatura ambiente", "Refrigerado", "Lugar seco", "No aplica"]},
        {"name": "tipoEnvase", "label": "Tipo de envase", "type": "select", "options": ["Bolsa sellada", "Lata", "Caja", "Botella", "Otro"]},
    ],
    "Insumos médicos": [
        {"name": "tipoInsumo", "label": "Tipo de insumo", "type": "select", "options": ["Medicamentos", "Material de curación", "Equipos médicos", "Insumos de protección", "Oxígeno y respiración"]},
        {"name": "fechaVencimiento", "label": "Fecha de vencimiento", "type": "date"},
        {"name": "registroISP", "label": "Registro ISP (si aplica)", "type": "text", "placeholder": "Ej: ISP-XXXXX"},
        {"name": "condicionesAlmacenamiento", "label": "Condiciones de almacenamiento", "type": "select", "options": ["Temperatura ambiente", "Cadena de frío", "Protegido de luz", "No aplica"]},
        {"name": "esterilizado", "label": "¿Viene esterilizado?", "type": "select", "options": ["Sí", "No", "No aplica"]},
    ],
    "Artículos de higiene": [
        {"name": "tipoArticulo", "label": "Tipo de artículo", "type": "select", "options": ["Kit personal", "Kit familiar", "Papel higiénico", "Jabones y shampoos", "Pañales", "Toallas femeninas", "Cepillos de dientes"]},
        {"name": "cantidadPorUnidad", "label": "Cantidad por unidad", "type": "text", "placeholder": "Ej: 6 unidades"},
        {"name": "destinatario", "label": "Destinatario preferente", "type": "select", "options": ["Niños", "Adultos", "Adultos mayores", "Familias", "Cualquiera"]},
    ],
    "Ropa y abrigo": [
        {"name": "categoria", "label": "Categoría", "type": "select", "options": ["Ropa interior", "Ropa exterior", "Abrigo", "Calzado", "Accesorios", "Frazadas y mantas"]},
        {"name": "talla", "label": "Talla(s)", "type": "select", "options": ["XS", "S", "M", "L", "XL", "XXL", "Única"]},
        {"name": "genero", "label": "Género", "type": "select", "options": ["Femenino", "Masculino", "Unisex", "Niños", "Niñas"]},
        {"name": "estadoPrenda", "label": "Estado de la prenda", "type": "select", "options": ["Nueva con etiqueta", "Nueva sin etiqueta", "Semi-nueva", "Usada en buen estado"]},
        {"name": "temporada", "label": "Temporada", "type": "select", "options": ["Invierno", "Verano", "Todo el año"]},
    ],
    "Donación Monetaria": [
        {"name": "metodoPago", "label": "Método de pago", "type": "select", "options": ["Transferencia bancaria", "Tarjeta débito/crédito", "Efectivo", "Otro"]},
        {"name": "monto", "label": "Monto en CLP", "type": "text", "placeholder": "Ej: 50000"},
        {"name": "comprobante", "label": "N° comprobante o referencia", "type": "text", "placeholder": "Ej: TRANS-2026-001"},
    ],
    "Utensilios del hogar": [
        {"name": "categoria", "label": "Categoría", "type": "select", "options": ["Ollas y sartenes", "Platos y cubiertos", "Electrodomésticos", "Muebles pequeños", "Ropa de cama", "Otros"]},
        {"name": "estadoUtensilio", "label": "Estado", "type": "select", "options": ["Nuevo", "Semi-nuevo", "Usado en buen estado"]},
        {"name": "material", "label": "Material predominante", "type": "text", "placeholder": "Ej: Acero inoxidable, Plástico"},
    ],
}

UNIDADES = [
    {"code": "kg", "nombre": "Kilogramo", "abreviatura": "kg"},
    {"code": "unid", "nombre": "Unidad", "abreviatura": "unidades"},
    {"code": "caja", "nombre": "Caja", "abreviatura": "cajas"},
    {"code": "kit", "nombre": "Kit", "abreviatura": "kits"},
    {"code": "prenda", "nombre": "Prenda", "abreviatura": "prendas"},
    {"code": "juego", "nombre": "Juego", "abreviatura": "juegos"},
    {"code": "sobre", "nombre": "Sobre", "abreviatura": "sobres"},
    {"code": "clp", "nombre": "Peso chileno", "abreviatura": "CLP"},
    {"code": "usd", "nombre": "Dólar", "abreviatura": "USD"},
]


async def get_tipos_recurso():
    productos = await logistica_client.listar_productos()
    return [
        {"code": str(p["id"]), "nombre": p["nombre"], "descripcion": p.get("descripcion", ""), "activo": p.get("activo", True)}
        for p in productos
    ]


async def get_unidades():
    return UNIDADES


async def get_unidades_por_tipo():
    return UNIDADES_POR_TIPO


async def get_campos_por_tipo():
    return CAMPOS_POR_TIPO


async def get_equipo():
    return EQUIPO


async def get_gobernanza():
    return GOBERNANZA


async def get_hitos():
    return HITOS


async def get_valores():
    return VALORES


async def get_reportes():
    return REPORTES


async def get_regiones():
    return [{"nombre": r} for r in REGIONES]


async def get_categorias_donacion():
    return CATEGORIAS_DONACION


async def get_pasos_funcionamiento():
    return PASOS_FUNCIONAMIENTO


async def get_impacto_stats():
    return IMPACTO_STATS


async def get_distribucion_fondos():
    return DISTRIBUCION_FONDOS
