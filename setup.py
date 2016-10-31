from setuptools import setup
import os

ignore_dir = ['.git']
"""
dirty fix for linchpin auto complete. Adds following expression to /etc/profile and sources it
eval "$(_LINCHPIN_COMPLETE=source linchpin)" 
need to think of a better way to do the same.
"""
if "eval \"$(_LINCHPIN_COMPLETE=source linchpin)\"" not in open("/etc/profile","r").read():
    fd = open("/etc/profile","a")
    fd.write("eval \"$(_LINCHPIN_COMPLETE=source linchpin)\"")
    fd.close()
    os.system("source /etc/profile")

def list_all_files(root_dir):
    file_set = []
    for dir_, _, files in os.walk(root_dir):
        for file_name in files:
            rel_dir = os.path.relpath(dir_, root_dir)
            rel_file = os.path.join(rel_dir, file_name)
            if any(ext in rel_file for ext in ignore_dir):
                continue
            file_set.append(rel_file)
    return file_set

setup(
    name='linchpin',
    version='0.8',
    py_modules= ['linchpin'],
    install_requires=[
        'Click',
        'ansible',
        'jinja2',
        'tabulate'
    ],
    entry_points='''
        [console_scripts]
        linchpin=linchpin:cli
    ''',
    packages=[
          'library',
          'filter_plugins',
          'keystore',
          'ex_schemas',
          'configure',
          'docs',
          'tests',
          'inventory_layouts',
          'inventory_outputs',
          'provision',
          'ex_topo',
          'outputs',
          'templates',
    ],
    package_data={
          'library': list_all_files('library'),
          'filter_plugins': list_all_files('filter_plugins'),
          'keystore': list_all_files('keystore'),
          'ex_schemas': list_all_files('ex_schemas'),
          'configure': list_all_files('configure'),
          'docs': list_all_files('docs'),
          'tests': list_all_files('tests'),
          'inventory_layouts': list_all_files('inventory_layouts'),
          'inventory_outputs': list_all_files('inventory_outputs'),
          'provision': list_all_files('provision'),
          'ex_topo': list_all_files('ex_topo'),
          'outputs': list_all_files('outputs'),
          'templates': list_all_files('templates'),
    },
    data_files=[
         ('/etc/linchpin', ['linchpin_config.yml']),
    ]
)
