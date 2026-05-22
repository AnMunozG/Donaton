import pymysql
import sys

# 1. Esto DEBE ir primero. Engaña a Python para que crea que pymysql es MySQLdb
pymysql.install_as_MySQLdb()

# 2. Ahora que el "engaño" está listo, podemos importar cosas de Django sin que explote
try:
    from django.db.backends.mysql.base import DatabaseWrapper
    
    # Desactivamos el chequeo de versión (Error 10.5)
    DatabaseWrapper.check_database_version_supported = lambda self: None
    
    # Desactivamos el RETURNING (Error 1064) de forma segura
    from django.db.backends.mysql.features import DatabaseFeatures
    DatabaseFeatures.can_return_columns_from_insert = property(lambda self: False)
    DatabaseFeatures.can_return_rows_from_bulk_insert = property(lambda self: False)
except Exception:
    pass