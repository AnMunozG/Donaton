from io import BytesIO
from datetime import datetime
from asgiref.sync import sync_to_async
from ..clients import donaciones_client


async def generar_certificado(rut: str, year: int) -> BytesIO:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import cm
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.colors import HexColor, colors as rl_colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

    PRIMARY = HexColor("#DD4444")

    try:
        all_donaciones = await donaciones_client.listar_donaciones(params={"origen": rut})
    except Exception:
        all_donaciones = []

    donaciones_data = [
        d for d in (all_donaciones if isinstance(all_donaciones, list) else [])
        if d.get("fecha", "").startswith(str(year))
    ]

    buf = BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=letter,
        topMargin=2 * cm, bottomMargin=2 * cm,
        leftMargin=2.5 * cm, rightMargin=2.5 * cm,
    )
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle("Title2", parent=styles["Title"], textColor=PRIMARY, fontSize=22, spaceAfter=6)
    subtitle_style = ParagraphStyle("Sub", parent=styles["Normal"], textColor=HexColor("#1a1a2e"), fontSize=12, spaceAfter=20)
    body_style = ParagraphStyle("Body", parent=styles["Normal"], fontSize=10, leading=14, spaceAfter=8)
    small_style = ParagraphStyle("Small", parent=styles["Normal"], fontSize=8, textColor=rl_colors.gray)

    total_kg = sum(float(d.get("cantidad", 0) or 0) for d in donaciones_data if d.get("tipo") != "Donación Monetaria")
    total_monetario = sum(float(d.get("cantidad", 0) or 0) for d in donaciones_data if d.get("tipo") == "Donación Monetaria")
    centros = set(d.get("centroId", "") for d in donaciones_data)

    elements = []

    elements.append(Paragraph("Certificado de Donación", title_style))
    elements.append(Paragraph(f"Año {year}", subtitle_style))
    elements.append(Spacer(1, 0.5 * cm))

    elements.append(Paragraph(f"<b>Donante:</b> {rut}", body_style))
    elements.append(Spacer(1, 0.3 * cm))

    elements.append(Paragraph(
        f"Durante el año <b>{year}</b>, realizaste <b>{len(donaciones_data)}</b> donaciones "
        f"a <b>{len(centros)}</b> centros de acopio, "
        f"totalizando <b>{total_kg:.0f} kg</b> en artículos "
        f"y <b>${total_monetario:,.0f}</b> en donaciones monetarias.",
        body_style
    ))
    elements.append(Spacer(1, 0.5 * cm))

    if donaciones_data:
        elements.append(Paragraph("<b>Detalle de donaciones:</b>", body_style))
        elements.append(Spacer(1, 0.2 * cm))

        table_data = [["Fecha", "Tipo", "Cantidad", "Unidad", "Centro", "Estado"]]
        for d in sorted(donaciones_data, key=lambda x: x.get("fecha", "")):
            table_data.append([
                d.get("fecha", ""),
                d.get("tipo", ""),
                str(d.get("cantidad", "")),
                d.get("unidad", ""),
                str(d.get("centroId", "")),
                d.get("estado", ""),
            ])

        col_widths = [65, 120, 55, 45, 80, 65]
        table = Table(table_data, colWidths=col_widths)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
            ("TEXTCOLOR", (0, 0), (-1, 0), rl_colors.white),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("ALIGN", (2, 0), (3, -1), "CENTER"),
            ("GRID", (0, 0), (-1, -1), 0.5, rl_colors.Color(0.85, 0.85, 0.85)),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [rl_colors.white, HexColor("#f8f8f8")]),
        ]))
        elements.append(table)

    elements.append(Spacer(1, 1 * cm))
    elements.append(Paragraph("Gracias por tu generosidad y compromiso con quienes más lo necesitan.", body_style))
    elements.append(Spacer(1, 0.3 * cm))
    elements.append(Paragraph("— Equipo Donatón", body_style))
    elements.append(Spacer(1, 0.5 * cm))
    elements.append(Paragraph(f"Certificado generado el {datetime.now().strftime('%d/%m/%Y')}", small_style))

    await sync_to_async(doc.build)(elements)
    buf.seek(0)
    return buf
