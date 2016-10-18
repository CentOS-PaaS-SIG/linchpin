import os
import os.path
import click 
from jinja2 import Environment, PackageLoader
import shutil, errno

def list_files(path):
    files =  os.listdir(path)
    for filename in files:
        click.echo(filename)

def copy_files(path, dir_list, config):
    for direc in dir_list:
        dest = path+"/"+direc+"/"
        src = config.clipath+"/templates/"+direc+"/"
        for filename in os.listdir(src):
            src_file = src+filename
            shutil.copy(src_file, dest)

class Config(object):
    
    def __init__(self):
        self.verbose = False
        self.env = Environment(loader=PackageLoader('linchpin', 'templates'))
        self.linchpinfile = self.env.get_template('linchpin.lpf.j2')
        self.clipath = os.path.dirname(os.path.realpath(__file__))
        self.dir_list = ["layouts","topologies"]
pass_config = click.make_pass_decorator(Config, ensure=True)

@click.group(chain=True)
@click.option('--verbose', is_flag=True)
@click.option('--home-directory', type=click.Path())
@pass_config
def cli(config, verbose, home_directory):
    """
    Welcome to linchpin command line client: lpcli
    """
    config.verbose = verbose
    if home_directory is None:
        home_directory = '.'
    config.home_directory = home_directory

@cli.command()
@click.option("--path", default=".", type=click.Path(), required=False,  help="path for initialisation")
@pass_config
def init(config, path):
    """ init module of linchpin """
    click.echo('Initailising the templates for linchpin file !')
    if config.verbose:
        click.echo("### verbose mode ###")
    if os.path.isdir(path):
        path = path.strip("/")
        config.linchpinfile.stream().dump(path+'/'+'linchfile.lpf')
        os.mkdir(path+"/topologies")
        os.mkdir(path+"/layouts")
        dir_list = ["topologies","layouts"]
        import pdb
        pdb.set_trace()
        copy_files(path, dir_list, config)
    else:
        click.echo("Invalid path to initialize !!")

@cli.command('list')
@click.option('--topos', default=False, required=False, is_flag=True)
@click.option('--layouts', default=False, required=False, is_flag=True)
@pass_config
def list(config, topos, layouts):
    """ list module of linchpin  """
    click.echo('linchpin list called !')
    if topos:
        #click.echo("list called with topologies")
        list_files(config.clipath+"/ex_topo")
    if layouts:
        #click.echo("list called with layouts")
        list_files(config.clipath+"/inventory_layouts")

@cli.command()
@click.option("--topo", default=False, required=False,  help="gets the topology by name")
@click.option("--layout", default=False, required=False,  help="gets the layout by name")
@pass_config
def get(config, topo, layout):
    """ get module of linchpin cli"""
    click.echo('get module called !')
