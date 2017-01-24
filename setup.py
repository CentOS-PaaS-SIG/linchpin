from setuptools import setup, findall
import os

# reading requirements from requirements.txt
with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='linchpin',
    version='0.8.3',
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
          'library': findall('ibrary'),
          'keystore': findall('keystore'),
          'ex_schemas': findall('ex_schemas'),
          'configure': findall('configure'),
          'docs': findall('docs'),
          'tests': findall('tests'),
          'inventory_layouts': findall('inventory_layouts'),
          'provision': findall('provision'),
          'ex_topo': findall('ex_topo'),
          'outputs': findall('outputs'),
          'templates': findall('templates'),
          'linchpin_api': findall('linchpin_api'),
          'cli': findall('cli'),
          'InventoryFilters': findall('InventoryFilters')
    },
    data_files=[
         ('', ['linchpin_config.yml']),
         ('', ['requirements.txt']),
    ],
    scripts=['scripts/linchpin_complete.sh']
)
