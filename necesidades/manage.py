#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

def main():
    # --- PARCHE DE RUTAS PARA WINDOWS ---
    # Esto le dice a Python que mire dentro de la carpeta actual si no encuentra los módulos
    base_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(base_dir)
    # ------------------------------------

    # Fuerza a Django a buscar el settings correcto sin importar cómo te lea la consola
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()