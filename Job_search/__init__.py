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

# Django doit savoir que le serveur utilisé ne renvoie pas les colonnes
# d'un INSERT. Il ne faut surtout pas supprimer RETURNING au niveau du
# curseur : Django attendrait alors des lignes qui n'existent plus.
