function escaparTextoPDF(texto) {
  let result = "";
  for (const ch of texto) {
    const code = ch.charCodeAt(0);
    if (code === 0x28 || code === 0x29 || code === 0x5C) {
      result += "\\" + ch;
    } else if (code < 128) {
      result += ch;
    } else if (code < 256) {
      result += "\\" + code.toString(8).padStart(3, "0");
    } else {
      result += "?";
    }
  }
  return result;
}

function strToLatin1Bytes(str) {
  const bytes = new Uint8Array(str.length);
  for (let i = 0; i < str.length; i++) {
    bytes[i] = str.charCodeAt(i) & 0xFF;
  }
  return bytes;
}

export function descargarPDF(titulo) {
  const tituloPDF = escaparTextoPDF(titulo);
  const date = new Date().toLocaleDateString("es-CL", {
    year: "numeric", month: "long", day: "numeric",
  });
  const datePDF = escaparTextoPDF(date);

  const header = "%PDF-1.4\n";
  const objects = [];
  const offsets = {};
  let pos = header.length;

  function obj(n, content) {
    offsets[n] = pos;
    const s = `${n} 0 obj\n${content}\nendobj\n`;
    objects.push(s);
    pos += s.length;
  }

  obj(1, "<< /Type /Catalog /Pages 2 0 R >>");
  obj(2, "<< /Type /Pages /Kids [3 0 R] /Count 1 >>");
  obj(3, "<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 5 0 R /Resources << /Font << /F1 4 0 R >> >> >>");
  obj(4, "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>");

  const streamData =
    `BT /F1 28 Tf 100 720 Td (${tituloPDF}) Tj ET\n` +
    `BT /F1 11 Tf 100 680 Td (Donaton - Plataforma de Transparencia) Tj ET\n` +
    `BT /F1 10 Tf 100 660 Td (Fecha de generacion: ${datePDF}) Tj ET\n` +
    `BT /F1 10 Tf 100 620 Td (Este documento ha sido generado automaticamente con fines de demostracion.) Tj ET\n` +
    `BT /F1 10 Tf 100 600 Td (Si este fuera un reporte real, aqui encontraria informacion detallada) Tj ET\n` +
    `BT /F1 10 Tf 100 580 Td (sobre las operaciones, finanzas e impacto de Donaton.) Tj ET`;

  obj(5, `<< /Length ${streamData.length} >>\nstream\n${streamData}\nendstream`);

  const doc = header + objects.join("");

  const xrefOffset = doc.length;
  const maxObj = Math.max(...Object.keys(offsets).map(Number));
  let xref = "xref\n";
  xref += `0 ${maxObj + 1}\n`;
  xref += "0000000000 65535 f \n";
  for (let i = 1; i <= maxObj; i++) {
    xref += `${String(offsets[i]).padStart(10, "0")} 00000 n \n`;
  }
  xref += "\ntrailer\n";
  xref += `<< /Size ${maxObj + 1} /Root 1 0 R >>\n`;
  xref += "startxref\n";
  xref += `${xrefOffset}\n`;
  xref += "%%EOF";

  const fullDoc = doc + xref;
  const bytes = strToLatin1Bytes(fullDoc);
  const blob = new Blob([bytes], { type: "application/pdf" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `${titulo.replace(/[\\()]/g, "").replace(/\s+/g, "_")}.pdf`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}
