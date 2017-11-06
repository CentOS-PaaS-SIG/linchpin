from .tinyrundb import TinyRunDB


DB_DRIVERS = {
    "TinyRunDB": TinyRunDB,
}


def get_all_drivers():
    return DB_DRIVERS
