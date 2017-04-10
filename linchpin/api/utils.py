#!/usr/bin/env python

import os
import sys
import yaml
#import json
#import click
#import shutil
#import pprint
#import inspect
#import ansible
#import requests
#import jsonschema as jsch
#
#from tabulate import tabulate
#from jinja2 import Environment, PackageLoader


def yaml2json(pf):

    """ parses yaml file into json object """

    with open(pf, 'r') as stream:
        try:
            pf = yaml.load(stream)
            return pf
        except yaml.YAMLError as exc:
            print(exc)



#    @staticmethod
#    def mkdir(dir_path):
#        if os.path.exists(dir_path):
#            shutil.rmtree(dir_path)
#        os.makedirs(dir_path)
#
#
#    @staticmethod
#    def display(message, m_type="print"):
#        if m_type == "print":
#            click.echo(message+":"+MSGS[message])
#        if m_type == "prompt":
#            while True:
#                reply = raw_input(message+":"+MSGS[message])
#                if (reply.lower() == "y" or reply.lower() == "yes"):
#                    return True
#                elif (reply.lower() == "n" or reply.lower() == "no"):
#                    sys.exit(0)
#        sys.exit(0)
#
#
#    @staticmethod
#    def list_by_ext(dir_path, ext):
#        files = []
#        for file in os.listdir(dir_path):
#            if file.endswith(ext):
#                files.append(dir_path+"/"+file)
#        return files
#
#
#    @staticmethod
#    def list_files(path):
#        files = os.listdir(path)
#        counter = 1
#        all_files = []
#        for filename in files:
#            file_tuple = [counter, filename]
#            all_files.append(file_tuple)
#            counter += 1
#        return all_files
#
#
#    @staticmethod
#    def get_file(src, dest):
#        try:
#            fd = open(src, "r")
#            name = fd.name.split("/")[-1]
#            inp = fd.read()
#            open(dest+name, "w").write(inp)
#            fd.close()
#        except Exception as e:
#            click.echo("get file aborted !!!")
#            click.echo(str(e))
#
#
#    @staticmethod
#    def copy_files(src, dest, dir_list):
#        for direc in dir_list:
#            dest_dir = dest + direc + "/"
#            src_dir = src + direc + "/"
#            for file in os.listdir(src_dir):
#                src_path = src_dir+file
#                shutil.copy(src_path, dest_dir)
#
#
#    @staticmethod
#    def checkpaths(workspace=None):
#        """ checks whether the linchpin layout already exists in cwd"""
#        if workspace is None:
#            cur_dir = os.getcwd()
#        else:
#            cur_dir = os.getcwd()
#        layout_files = ['layouts', 'topologies', 'PinFile']
#        for f in layout_files:
#            if f in os.listdir(cur_dir):
#                return True
#
#
#    @staticmethod
#    def search_path(name, path):
#        """ searches for files by name in a given path """
#        for root, dirs, files in os.walk(path):
#            if name in files:
#                return os.path.join(root, name)
#
#
#    @staticmethod
#    def tabulate_print(items, headers):
#        print_items = []
#        for i in range(0, len(items)):
#            print_items.append((i+1, items[i]["name"]))
#        print tabulate(print_items, headers, tablefmt="fancy_grid")
#
#
#    @staticmethod
#    def write_to_file(dest_path, output):
#        if os.path.isfile(dest_path):
#            click.echo("File exists at path "+dest_path)
#            ans = click.prompt('Do you want to overwrite it ?', default='Y')
#            if ans.lower() in ['no','n']:
#                pass
#            elif ans.lower() in ['yes','y']:
#                with open(dest_path, "w") as txt:
#                    txt.write(output)
#                click.echo("File created successfully")
#        else:
#            with open(dest_path, "w") as txt:
#                txt.write(output)
#            click.echo("File created successfully")
#
#
#    @staticmethod
#    def touch(fname):
#        if os.path.exists(fname):
#            os.utime(fname, None)
#        else:
#            open(fname, 'a').close()
#
#
#
#
#
#    def get_file(src, dest, link=False):
#        if link:
#            r = requests.get(src)
#            name = src.split("/")[-1]
#            open(dest+"/"+name, "w").write(r.content)
#        else:
#            fd = open(src, "r")
#            name = fd.name.split("/")[-1]
#            inp = fd.read()
#            open(dest+name, "w").write(inp)
#            fd.close()
#
#
#    def list_files(path):
#        files = os.listdir(path)
#        all_files = []
#        for filename in files:
#            file_dict = {"name": filename}
#            all_files.append(file_dict)
#        return all_files
#
#
