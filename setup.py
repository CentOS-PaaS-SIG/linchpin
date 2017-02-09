from setuptools import setup, find_packages
#from distutils.core import setup
from pip.req import parse_requirements
import os

# reading requirements from requirements.txt
dir_path = os.path.dirname(os.path.realpath(__file__))
reqs_file = 'requirements.txt'.format(dir_path)
<<<<<<< 7eef16c0f0fbf4c14d478d67bc8862976621ff48

=======
>>>>>>> fixed up packaging, and libraries to make it more pythonic
with open(reqs_file) as f:
    required = f.read().splitlines()

ignore_dir = ['.git']

setup(
    name='linchpin',
    version='0.9.1',
    description = 'Ansible based multi cloud orchestrator',
    author = 'samvaran kashyap rallabandi',
    author_email = 'samvaran.kashyap@gmail.com',
    url = 'http://linch-pin.readthedocs.io/',
    setup_requires=required,
    install_requires=required,
    entry_points='''
        [console_scripts]
        linchpin=linchpin:cli
    ''',
    extras_require = {
        'beaker':  ['beaker-client==23.3'],
        'docs': ["docutils","sphinx","sphinx_rtd_theme"],
        'tests': ["nose","mock","coverage"],
        'libvirt': ["libvirt-python>=3.0.0", "lxml"],
    },
    dependency_links = ['https://github.com/eevee/camel/tree/v0.1/tarball/'],
    zip_safe=False,
    packages=find_packages(),
    include_package_data=True,
    scripts=['scripts/linchpin_complete.sh']
)
