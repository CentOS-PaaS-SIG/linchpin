from setuptools import setup, findall
import os

# reading requirements from requirements.txt
with open('requirements.txt') as f:
    required = f.read().splitlines()

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

setup(
    name='linchpin',
    version='0.9.1',
    description = 'Ansible based multi cloud orchestrator',
    author = 'samvaran kashyap rallabandi',
    author_email = 'samvaran.kashyap@gmail.com',
    url = 'http://linch-pin.readthedocs.io/',
    py_modules= ['linchpin'],
    install_requires=required,
    entry_points='''
        [console_scripts]
        linchpin=linchpin:cli
    ''',
    extras_require = {
        'libvirt': ["libvirt-python>=3.0.0"],
    },
    dependency_links = ['https://github.com/eevee/camel/tree/v0.1/tarball/'],
    packages=[
          'library',
          'keystore',
          'ex_schemas',
          'configure',
          'docs',
          'tests',
          'inventory_layouts',
          'provision',
          'ex_topo',
          'outputs',
          'templates',
          'linchpin_api',
          'cli',
          'InventoryFilters'
    ],
    package_data={
          'library': list_all_files('library'),
          'keystore': list_all_files('keystore'),
          'ex_schemas': list_all_files('ex_schemas'),
          'configure': list_all_files('configure'),
          'docs': list_all_files('docs'),
          'tests': list_all_files('tests'),
          'inventory_layouts': list_all_files('inventory_layouts'),
          'provision': list_all_files('provision'),
          'ex_topo': list_all_files('ex_topo'),
          'outputs': list_all_files('outputs'),
          'templates': list_all_files('templates'),
          'linchpin_api': list_all_files('linchpin_api'),
          'cli': list_all_files('cli'),
          'InventoryFilters': list_all_files('InventoryFilters')
    },
    data_files=[
         ('', ['linchpin_config.yml']),
         ('', ['requirements.txt']),
    ],
    scripts=['scripts/linchpin_complete.sh']
)
