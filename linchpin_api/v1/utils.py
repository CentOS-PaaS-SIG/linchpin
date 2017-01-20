import os
import requests
import yaml


def get_file(src, dest, link=False):
    if link:
        r = requests.get(src)
        name = src.split("/")[-1]
        open(dest+"/"+name, "w").write(r.content)
    else:
        fd = open(src, "r")
        name = fd.name.split("/")[-1]
        inp = fd.read()
        open(dest+name, "w").write(inp)
        fd.close()

def list_files(path):
    files = os.listdir(path)
    all_files = []
    for filename in files:
        file_dict = {"name": filename}
        all_files.append(file_dict)
    return all_files


def parse_yaml(pf):
    """ parses yaml file into json object """
    print("debug::print file path")
    print(pf)
    with open(pf, 'r') as stream:
        try:
            pf = yaml.load(stream)
            return pf
        except yaml.YAMLError as exc:
            print(exc)
