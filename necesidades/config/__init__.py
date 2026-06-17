import pymysql

# 1. Enlazar PyMySQL como el conector predeterminado
pymysql.install_as_MySQLdb()

# 2. Forzar compatibilidad con MariaDB antiguo anulando las propiedades con funciones lambda
from django.db.backends.mysql.features import DatabaseFeatures
from django.db.backends.base.base import BaseDatabaseWrapper

# Sobrescribimos las propiedades usando la función 'property' para que Django lea siempre False
DatabaseFeatures.can_return_rows_from_bulk_insert = property(lambda self: False)
DatabaseFeatures.can_return_id_from_insert = property(lambda self: False)
DatabaseFeatures.has_select_for_update_skip_locked = property(lambda self: False)

# Desactivar por completo el validador de versión mínima compatible
BaseDatabaseWrapper.check_database_version_supported = lambda self: None