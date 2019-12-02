from __future__ import absolute_import

from .tinydb import TinyRunDB

try:
    from .mongodb import MongoDB
except Exception as e:
    print("WARNING:" + str(e))
    print("WARNING: pymongo is currently not supported in python 2.7.x \
          Please Upgrade to Python 3.x If you would like to use Mongodb \
          Driver for rundb operations in linchpin")

try:
    DB_DRIVERS = {
        "TinyRunDB": TinyRunDB,
        "MongoDB": MongoDB,
    }
except Exception as e:
    DB_DRIVERS = {
        "TinyRunDB": TinyRunDB,
    }
    print("WARNING:" + str(e))
    print("WARNING: pymongo is currently not supported in python 2.7.x \
          Please Upgrade to Python 3.x If you would like to use Mongodb \
          Driver for rundb operations in linchpin")


def get_all_drivers():
    return DB_DRIVERS
