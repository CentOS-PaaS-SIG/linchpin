import yaml
import json
import jsonschema
import io
from jsonschema import validate
try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser


def get_sections(ini):
    ini = ini.decode('utf-8') 
    buf = io.StringIO(ini)
    config = ConfigParser(allow_no_value=True)
    config.readfp(buf)
    sections = config.sections()
    return sections
