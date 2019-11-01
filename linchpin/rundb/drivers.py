from __future__ import absolute_import

from .tinydb import TinyRunDB
from .mongodb import MongoDB


DB_DRIVERS = {
    "TinyRunDB": TinyRunDB,
    "MongoDB": MongoDB,
}


def get_all_drivers():
    return DB_DRIVERS
