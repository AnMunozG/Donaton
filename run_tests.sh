#!/bin/bash
# Crear directorio central de reportes local fuera de Docker
mkdir -p reportes_globales

SERVICIOS=("bff" "logistica" "donaciones" "usuarios")

for SERVICIO in "${SERVICIOS[@]}"
do
    echo "========================================="
    echo "Corriendo pruebas unitarias en: $SERVICIO"
    echo "========================================="

    # Ejecuta pytest en el contenedor
    docker compose exec -T $SERVICIO pytest

    # Copia el reporte autogenerado hacia afuera
    docker compose cp $SERVICIO:/app/reports/reporte.html ./reportes_globales/reporte_$SERVICIO.html

    echo "Reporte visual guardado en reportes_globales/reporte_$SERVICIO.html"
done