import os
import os.path
import click 
from jinja2 import Environment, PackageLoader
import shutil, errno
import sys
import json
import pdb
import ansible
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.executor.playbook_executor import PlaybookExecutor

MSGS = {
"ERROR:001": "No lpf files found. Please use linchpin init to initailise ", 
"WARNING:001": "lpf file structure found current directory. Would you like to continue ?(y/n) " 
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
    files =  os.listdir(path)
    for filename in files:
        click.echo(filename)

def get_file(src, dest):
    try:
        fd = open(src,"r")
        name = fd.name.split("/")[-1]
        inp = fd.read()
        open(dest+name,"w").write(inp)
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
    cur_dir = os.getcwd()
    print os.listdir(cur_dir)
    layout_files = ['layouts', 'topologies', 'linchfile.lpf']
    for f in layout_files:
        if f in os.listdir(cur_dir):
            return True

class Config(object):
    def __init__(self):
        self.verbose = False
        self.env = Environment(loader=PackageLoader('linchpin', 'templates'))
        self.linchpinfile = self.env.get_template('linchpin.lpf.j2')
        self.clipath = os.path.dirname(os.path.realpath(__file__))
        self.dir_list = ["layouts","topologies"]
        self.variable_manager = VariableManager()
        self.loader = DataLoader()
        self.inventory = Inventory(loader=self.loader, variable_manager=self.variable_manager,  host_list=['localhost'])
        Options = namedtuple('Options', ['listtags', 'listtasks', 'listhosts', 'syntax', 'connection','module_path', 'forks', 'remote_user', 'private_key_file', 'ssh_common_args', 'ssh_extra_args', 'sftp_extra_args', 'scp_extra_args', 'become', 'become_method', 'become_user', 'verbosity', 'check'])
        self.playbook_path = 'playbooks/test_playbook.yml'
        self.options = Options(listtags=False, listtasks=False, listhosts=False, syntax=False, connection='ssh', module_path=None, forks=100, remote_user='slotlocker', private_key_file=None, ssh_common_args=None, ssh_extra_args=None, sftp_extra_args=None, scp_extra_args=None, become=True, become_method=None, become_user='root', verbosity=3, check=False)
        #variable_manager.extra_vars = {'hosts': 'mywebserver'} # This can accomodate various other command line arguments.`
        #passwords = {}
        #pbex = PlaybookExecutor(playbooks=[playbook_path], inventory=inventory, variable_manager=variable_manager, loader=loader, options=options, passwords=passwords)
        #results = pbex.run()

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
    if checkpaths():
       reply = display("WARNING:001","prompt")
       if not reply:
           sys.exit(0)
    if config.verbose:
        click.echo("### verbose mode ###")
    if os.path.isdir(path):
        path = path.strip("/")
        config.linchpinfile.stream().dump(path+'/'+'linchfile.lpf')
        mkdir(path+"/topologies")
        mkdir(path+"/layouts")
        dir_list = ["topologies","layouts"]
        copy_files(path, dir_list, config)
    else:
        click.echo("Invalid path to initialize !!")

@cli.command()
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
    #click.echo('get module called !')
    if topo:
        #click.echo("getting the topology file")
        get_file(config.clipath+"/ex_topo/"+topo,"./topologies/")
    if layout:
        #click.echo("list called with layouts")
        get_file(config.clipath+"/inventory_layouts/"+layout,"./layouts/")

@cli.command()
@pass_config
def rise(config ):
    """ rise module of linchpin cli"""
    config.variable_manager.extra_vars = {}
    playbook_path = config.clipath+"/provision/site.yml"
    init_dir = os.getcwd()
    lpfs = list_by_ext(init_dir,".lpf")
    if len(lpfs) == 0:
        display("ERROR:001")
    inventory = Inventory(loader=config.loader, variable_manager=config.variable_manager,  host_list=[])
    config.variable_manager.extra_vars = {"linchpin_config": "/etc/linchpin/linchpin_config.yml"} 
    passwords = {}
    pbex = PlaybookExecutor(playbooks=[playbook_path], inventory=inventory, variable_manager=config.variable_manager, loader=config.loader, options=config.options, passwords=passwords)
    results = pbex.run()
