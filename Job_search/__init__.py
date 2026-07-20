# import pymysql
# import sys

# # 1. Émuler MySQLdb avec PyMySQL pour Python 3.13
# pymysql.constants.COMMAND = None
# sys.modules["MySQLdb"] = pymysql
# pymysql.install_as_MySQLdb()

# # 2. Importer les modules d'initialisation de Django
# from django.db.backends.mysql import base
# from django.db.backends.base.base import BaseDatabaseWrapper

# # 3. Court-circuiter définitivement le blocage de version de MariaDB
# def fake_check_version(*args, **kwargs):
#     pass

# base.DatabaseFeatures.check_database_version_supported = fake_check_version
# BaseDatabaseWrapper.check_database_version_supported = fake_check_version

import pymysql
import sys

# 1. Émuler MySQLdb avec PyMySQL pour l'environnement Python 3.13
pymysql.constants.COMMAND = None
sys.modules["MySQLdb"] = pymysql
pymysql.install_as_MySQLdb()

# 2. Importer les modules d'initialisation de Django
from django.db.backends.mysql import base
from django.db.backends.base.base import BaseDatabaseWrapper

# 3. Court-circuiter définitivement le blocage de version de MariaDB
def fake_check_version(*args, **kwargs):
    pass

base.DatabaseFeatures.check_database_version_supported = fake_check_version
BaseDatabaseWrapper.check_database_version_supported = fake_check_version

# 4. INTERCEPTEUR DE REQUÊTES : Supprime le mot-clé RETURNING si Django l'injecte
original_execute = pymysql.cursors.Cursor.execute

def patched_execute(self, query, args=None):
    if isinstance(query, str) and "RETURNING" in query:
        # Nettoie la requête en retirant "RETURNING `id`" ou similaire en fin de ligne
        if "RETURNING" in query:
            query = query.split("RETURNING")[0].strip()
    return original_execute(self, query, args)

# On applique l'intercepteur directement sur le pilote MySQL
pymysql.cursors.Cursor.execute = patched_execute
