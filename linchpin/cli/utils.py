import os
import os.path
import yaml
import click
import shutil
import sys
import json
import inspect
import pdb
import ansible
import pprint
import jsonschema as jsch
from ansible import utils
from tabulate import tabulate
from jinja2 import Environment, PackageLoader


MSGS = {
        "ERROR:001": "No PinFiles found. \
                      Please use linchpin init to initailise ",
        "ERROR:002": "Multiple PinFiles found. \
                      Please use linchpin rise with --pf <path>",
        "ERROR:003": "Topology or Layout mentioned in PinFile not found.\
                      Please check your pf file.",
        "ERROR:004": "linchpin_config file not found in current directory.\
                      Please initialise it with lionchpin init or \
                      linchpin config --reset",
        "ERROR:005": "linchpin_config file not found. In default paths.\
                      Please initialise it with lionchpin init or \
                      linchpin config --reset",
        "WARNING:001": "PinFile structure found current directory.\
                        Would you like to continue ?(y/n)",
        "WARNING:002": "linchpin_config file already found in current directory.\
                        Would you like to reset it ?(y/n)"
}


def mkdir(dir_path):
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
    os.makedirs(dir_path)


def display(message, m_type="print"):
    if m_type == "print":
        click.echo(message+":"+MSGS[message])
    if m_type == "prompt":
        while True:
            reply = raw_input(message+":"+MSGS[message])
            if (reply.lower() == "y" or reply.lower() == "yes"):
                return True
            elif (reply.lower() == "n" or reply.lower() == "no"):
                sys.exit(0)
    sys.exit(0)


def list_by_ext(dir_path, ext):
    files = []
    for file in os.listdir(dir_path):
        if file.endswith(ext):
            files.append(dir_path+"/"+file)
    return files


def list_files(path):
    files = os.listdir(path)
    counter = 1
    all_files = []
    for filename in files:
        file_tuple = [counter, filename]
        all_files.append(file_tuple)
        counter += 1
    return all_files


def get_file(src, dest):
    try:
        fd = open(src, "r")
        name = fd.name.split("/")[-1]
        inp = fd.read()
        open(dest+name, "w").write(inp)
        fd.close()
    except Exception as e:
        click.echo("get file aborted !!!")
        click.echo(str(e))


def copy_files(path, dir_list, config):
    for direc in dir_list:
        dest = path+"/"+direc+"/"
        src = config.clipath+"/templates/"+direc+"/"
        for filename in os.listdir(src):
            src_file = src+filename
            shutil.copy(src_file, dest)


def checkpaths():
    """ checks whether the linchpin layout already exists in cwd"""
    cur_dir = os.getcwd()
    # print os.listdir(cur_dir)
    layout_files = ['layouts', 'topologies', 'PinFile']
    for f in layout_files:
        if f in os.listdir(cur_dir):
            return True


def parse_yaml(pf):
    """ parses yaml file into json object """
    with open(pf, 'r') as stream:
        try:
            pf = yaml.load(stream)
            return pf
        except yaml.YAMLError as exc:
            print(exc)


def search_path(name, path):
    """ searches for files by name in a given path """
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)
