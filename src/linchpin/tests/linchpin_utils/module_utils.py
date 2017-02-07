#!/usr/bin/env python

import base64
import optparse
import os
import subprocess
import sys
import traceback
import shutil
try:
    import json
except ImportError:
    import simplejson as json
import ansible.utils.vars as utils_vars
from ansible.parsing.dataloader import DataLoader
from ansible.parsing.utils.jsonify import jsonify
from ansible.parsing.splitter import parse_kv
import ansible.executor.module_common as module_common
import ansible.constants as C


def write_argsfile(argstring, json=False):
    """ Write args to a file for old-style module's use. """
    argspath = os.path.expanduser("~/.ansible_test_module_arguments")
    argsfile = open(argspath, 'w')
    if json:
        args = parse_kv(argstring)
        argstring = jsonify(args)
    argsfile.write(argstring)
    argsfile.close()
    return argspath


def boilerplate_module(modfile, args, interpreter, check, destfile):
    """ simulate what ansible does with new style modules """

    loader = DataLoader()

    complex_args = {}
    if args.startswith("@"):
        # Argument is a YAML file (JSON is a subset of YAML)
        complex_args = utils_vars.combine_vars(complex_args,
                                               loader.load_from_file(args[1:]))
        args = ''
    elif args.startswith("{"):
        # Argument is a YAML document (not a file)
        complex_args = utils_vars.combine_vars(complex_args, loader.load(args))
        args = ''

    if args:
        parsed_args = parse_kv(args)
        complex_args = utils_vars.combine_vars(complex_args, parsed_args)

    task_vars = {}
    if interpreter:
        if '=' not in interpreter:
            print("interpreter must by in the form of \
                   ansible_python_interpreter=/usr/bin/python")
            sys.exit(1)
        interpreter_type, interpreter_path = interpreter.split('=')
        if not interpreter_type.startswith('ansible_'):
            interpreter_type = 'ansible_%s' % interpreter_type
        if not interpreter_type.endswith('_interpreter'):
            interpreter_type = '%s_interpreter' % interpreter_type
        task_vars[interpreter_type] = interpreter_path

    if check:
        complex_args['_ansible_check_mode'] = True

    modname = os.path.basename(modfile)
    modname = os.path.splitext(modname)[0]
    (module_data, module_style, shebang) = module_common.modify_module(
        modname,
        modfile,
        complex_args,
        task_vars=task_vars
    )

    if module_style == 'new' \
       and 'ZIPLOADER_WRAPPER = True' in module_data:
        module_style = 'ziploader'

    modfile2_path = os.path.expanduser(destfile)
    print("* including generated source,\
           if any, saving to: %s" % modfile2_path)
    if module_style not in ('ziploader', 'old'):
        print("* this may offset any line numbers in tracebacks/debuggers!")
    modfile2 = open(modfile2_path, 'w')
    modfile2.write(module_data)
    modfile2.close()
    modfile = modfile2_path

    return (modfile2_path, modname, module_style)


def ziploader_setup(modfile, modname):
    os.system("chmod +x %s" % modfile)

    cmd = subprocess.Popen([modfile, 'explode'],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    out, err = cmd.communicate()
    lines = out.splitlines()
    if len(lines) != 2 or 'Module expanded into' not in lines[0]:
        print("*" * 35)
        print("INVALID OUTPUT FROM ZIPLOADER MODULE WRAPPER")
        print(out)
        sys.exit(1)
    debug_dir = lines[1].strip()

    argsfile = os.path.join(debug_dir, 'args')
    modfile = os.path.join(debug_dir, 'ansible_module_%s.py' % modname)

    print("* ziploader module detected;\
             extracted module source to: %s" % debug_dir)
    return modfile, argsfile


def runtest(modfile, argspath, modname, module_style):
    """Test run a module, piping it's output for reporting."""
    if module_style == 'ziploader':
        modfile, argspath = ziploader_setup(modfile, modname)

    os.system("chmod +x %s" % modfile)

    invoke = "%s" % (modfile)
    if argspath is not None:
        invoke = "%s %s" % (modfile, argspath)

    cmd = subprocess.Popen(invoke,
                           shell=True,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    (out, err) = cmd.communicate()

    try:
        results = json.loads(out)
    except:
        print("*" * 35)
        print("INVALID OUTPUT FORMAT")
        print(out)
        traceback.print_exc()
        sys.exit(1)

    print("*" * 35)
    print("PARSED OUTPUT")
    print(jsonify(results, format=True))
    return results


def rundebug(debugger, modfile, argspath, modname, module_style):
    """Run interactively with console debugger."""

    if module_style == 'ziploader':
        modfile, argspath = ziploader_setup(modfile, modname)

    if argspath is not None:
        subprocess.call("%s %s %s" % (debugger, modfile, argspath), shell=True)
    else:
        subprocess.call("%s %s" % (debugger, modfile), shell=True)


def run_module(options):
    m_path = options["module_path"]
    m_args = options["module_args"]
    m_intr = options["interpretor"]
    m_chk = options["check"]
    m_fname = options["filename"]
    (modfile, modname, module_style) = boilerplate_module(m_path,
                                                          m_args,
                                                          m_intr,
                                                          m_chk,
                                                          m_fname)

    argspath = None
    if module_style not in ('new', 'ziploader'):
        if module_style == 'non_native_want_json':
            argspath = write_argsfile(options.module_args, json=True)
        elif module_style == 'old':
            argspath = write_argsfile(options.module_args, json=False)
        else:
            raise Exception("internal error,\
                            unexpected module style: %s" % module_style)
    results = runtest(modfile, argspath, modname, module_style)
    return results
