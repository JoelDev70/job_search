
import pymysql
import sys

# 1. Simuler les constantes requises par Django 3.13+
pymysql.constants.COMMAND = None
sys.modules["MySQLdb"] = pymysql

# 2. Forcer l'initialisation de PyMySQL
pymysql.install_as_MySQLdb()

# 3. Patch de force brute sur l'exception de version de Django
from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.utils import NotSupportedError

original_init = BaseDatabaseWrapper.init_connection_state

def patched_init_connection_state(self):
    try:
        original_init(self)
    except NotSupportedError as e:
        if "MariaDB" in str(e):
            # Si Django râle à cause de la version de MariaDB, on ignore l'erreur
            pass
        else:
            raise e

# On injecte notre fonction modifiée directement dans le cœur de Django
BaseDatabaseWrapper.init_connection_state = patched_init_connection_state
