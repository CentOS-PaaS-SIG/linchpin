from setuptools import setup
import os

ignore_dir = ['.git']

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
"""
drwxr-xr-x. 2 root root  4096 Oct 10 17:17 libvirt_xml
drwxr-xr-x. 2 root root  4096 Oct 10 17:17 library
drwxr-xr-x. 2 root root  4096 Oct 10 17:17 filter_plugins
drwxr-xr-x. 2 root root  4096 Oct 10 17:17 bin
drwxr-xr-x. 2 root root  4096 Oct 10 17:17 keystore
drwxr-xr-x. 2 root root  4096 Oct 10 17:17 aws_cfn_templates
drwxr-xr-x. 2 root root  4096 Oct 10 17:17 sample_outputs
drwxr-xr-x. 2 root root  4096 Oct 10 17:17 ex_schemas
drwxr-xr-x. 3 root root  4096 Oct 10 17:17 configure
drwxr-xr-x. 2 root root  4096 Oct 10 17:17 plugins
drwxr-xr-x. 4 root root  4096 Oct 10 17:17 docs
drwxr-xr-x. 2 root root  4096 Oct 10 17:17 inventory
drwxr-xr-x. 6 root root  4096 Oct 11 10:28 tests
drwxr-xr-x. 2 root root  4096 Oct 11 10:49 inventory_layouts
drwxr-xr-x. 2 root root  4096 Oct 12 16:43 inventory_outputs
drwxr-xr-x. 6 root root  4096 Oct 13 12:31 provision
drwxr-xr-x. 2 root root  4096 Oct 15 02:06 example_playbooks
drwxr-xr-x. 2 root root  4096 Oct 16 04:38 ex_topo
drwxr-xr-x. 2 root root  4096 Oct 16 10:26 outputs
"""


setup(
    name='LinchpinCli',
    version='1.0',
    py_modules= ['linchpin'],
    install_requires=[
        'Click',
        'ansible',
        'jinja2'
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
