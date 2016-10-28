import os
import yaml
import os.path
import click 
from jinja2 import Environment, PackageLoader
import shutil, errno
import sys
import json
import inspect
import pdb
import ansible
import pprint
from tabulate import tabulate
from ansible import utils
import jsonschema as jsch
from collections import namedtuple
from ansible import utils
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.plugins.callback import CallbackBase
MSGS = {
"ERROR:001": "No lpf files found. Please use linchpin init to initailise ", 
"ERROR:002": "Multiple lpf files found. Please use linchpin rise with --lpf <path> ", 
"ERROR:003": "Topology or Layout mentioned in lpf file not found . Please check your lpf file.", 
"WARNING:001": "lpf file structure found current directory. Would you like to continue ?(y/n) " 
}

PLAYBOOKS={
"PROVISION": "site.yml",
"TEARDOWN": "site.yml",
"SCHEMA_CHECK": "schema_check.yml",

}


class PlaybookCallback(CallbackBase):
    """Playbook callback"""

    def __init__(self):
        super(PlaybookCallback, self).__init__()
        # store all results
        self.results = []

    def v2_runner_on_ok(self, result, **kwargs):
        """Save result instead of printing it"""
        self.results.append(result)

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
    counter = 1
    all_files = []
    for filename in files:
        file_tuple = [counter, filename]
        all_files.append(file_tuple)
        counter += 1
    return all_files

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
    """ checks whether the linchpin layout already exists in cwd"""
    cur_dir = os.getcwd()
    print os.listdir(cur_dir)
    layout_files = ['layouts', 'topologies', 'linchfile.lpf']
    for f in layout_files:
        if f in os.listdir(cur_dir):
            return True

def parse_yaml(lpf):
    """ parses yaml file into json object """
    with open(lpf, 'r') as stream:
        try:
            lpf = yaml.load(stream)
            return lpf
        except yaml.YAMLError as exc:
            print(exc)

def invoke_linchpin(config, e_vars, playbook="PROVISION", console=True):
    """ Invokes linchpin playbook """
    playbook_path = config.clipath+"/provision/"+PLAYBOOKS[playbook]
    inventory = Inventory(loader=config.loader, variable_manager=config.variable_manager,  host_list=[])
    config.variable_manager.extra_vars = e_vars 
    passwords = {}
    utils.VERBOSITY = 4
    pbex = PlaybookExecutor(playbooks=[playbook_path], inventory=inventory, variable_manager=config.variable_manager, loader=config.loader, options=config.options, passwords=passwords)
    if console == False:
        cb = PlaybookCallback()
        pbex._tqm._stdout_callback = cb
        return_code = pbex.run()
        results = cb.results
    else:
       results = pbex.run()
    return results

def search_path(name, path):
    """ searches for files by name in a given path """
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

def get_evars(lpf):
    """ creates a group of extra vars on basis on linchpin file """
    e_vars = []
    for group in lpf:
        topology = lpf[group].get("topology") 
        layout = lpf[group].get("layout")
        e_var_grp = {}
        e_var_grp["topology"] = search_path(topology, os.getcwd())
        e_var_grp["layout"] = search_path(layout, os.getcwd() )
        if None in  e_var_grp.values():
            display("ERROR:003")
        e_vars.append(e_var_grp)
    return e_vars
        

class Config(object):
    """ Global config object accesible by all the click modules """
    def __init__(self):
        self.verbose = False
        self.env = Environment(loader=PackageLoader('linchpin', 'templates'))
        self.linchpinfile = self.env.get_template('linchpin.lpf.j2')
        self.clipath = os.path.dirname(os.path.realpath(__file__))
        self.dir_list = ["layouts","topologies"]
        self.variable_manager = VariableManager()
        self.loader = DataLoader()
        self.inventory = Inventory(loader=self.loader, variable_manager=self.variable_manager,  host_list=['localhost'])
        utils.VERBOSITY = 4
        Options = namedtuple('Options', ['listtags', 'listtasks', 'listhosts', 'syntax', 'connection','module_path', 'forks', 'remote_user', 'private_key_file', 'ssh_common_args', 'ssh_extra_args', 'sftp_extra_args', 'scp_extra_args', 'become', 'become_method', 'become_user', 'verbosity', 'check'])
        self.playbook_path = 'playbooks/test_playbook.yml'
        self.options = Options(listtags=False, listtasks=False, listhosts=False, syntax=False, connection='ssh', module_path=None, forks=100, remote_user='test', private_key_file=None, ssh_common_args=None, ssh_extra_args=None, sftp_extra_args=None, scp_extra_args=None, become=True, become_method=None, become_user='root', verbosity=utils.VERBOSITY, check=False)
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
        copy_files(path, dir_list, config)
    else:
        click.echo("Invalid path to initialize !!")

@cli.command()
@click.option('--topos', default=False, required=False, is_flag=True)
@click.option('--layouts', default=False, required=False, is_flag=True)
@pass_config
def list(config, topos, layouts):
    """ list module of linchpin  """
    if (not topos) and (not layouts): 
        click.echo('linchpin list usage linchpin list <--topos> <--layouts> ')
    headers = ["Sno","Name"]
    if topos:
        click.echo(": TOPOLOGIES LIST :")
        files = list_files(config.clipath+"/ex_topo")
        print tabulate(files, headers, tablefmt="fancy_grid")
        
    if layouts:
        click.echo(": LAYOUTS LIST :")
        files = list_files(config.clipath+"/inventory_layouts")
        print tabulate(files, headers, tablefmt="fancy_grid")
        

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
@click.option("--lpf", default=False, required=False,  help="gets the topology by name")
@pass_config
def rise(config, lpf):
    """ rise module of linchpin cli : still need to fix the linchpin_config and outputs, inventory_outputs paths"""
    config.variable_manager.extra_vars = {}
    init_dir = os.getcwd()
    lpfs = list_by_ext(init_dir,".lpf")
    if len(lpfs) == 0:
        display("ERROR:001")
    if len(lpfs) > 1:
        display("ERROR:002") 
    lpf = lpfs[0]
    lpf = parse_yaml(lpf)
    e_vars_grp = get_evars(lpf)
    for e_vars in e_vars_grp:
        """ need to change them to be a part of config obj"""
        e_vars['linchpin_config'] = "/etc/linchpin/linchpin_config.yml"
        e_vars['outputfolder_path'] = init_dir+"/outputs"
        e_vars['inventory_outputs_path'] = init_dir+"/inventory"
        e_vars['state'] = "present"
        output = invoke_linchpin(config, e_vars, "PROVISION", console=True)

@cli.command()
@click.option("--lpf", default=False, required=False,  help="gets the topology by name")
@pass_config
def drop(config, lpf):
    """ drop module of linchpin cli : still need to fix the linchpin_config and outputs, inventory_outputs paths"""
    config.variable_manager.extra_vars = {}
    init_dir = os.getcwd()
    lpfs = list_by_ext(init_dir,".lpf")
    if len(lpfs) == 0:
        display("ERROR:001")
    if len(lpfs) > 1:
        display("ERROR:002")
    lpf = lpfs[0]
    lpf = parse_yaml(lpf)
    e_vars_grp = get_evars(lpf)
    for e_vars in e_vars_grp:
        """ need to change them to be a part of config obj """
        e_vars['linchpin_config'] = "/etc/linchpin/linchpin_config.yml"
        topo_name = parse_yaml(e_vars["topology"])["topology_name"]
        e_vars['topology_output_file'] = init_dir+"/outputs/"+topo_name+".output"
        e_vars['inventory_outputs_path'] = init_dir+"/inventory"
        e_vars['state'] = "absent"
        invoke_linchpin(config, e_vars, "PROVISION", console=True)

@cli.command()
@click.option("--lpf", default=False, required=False,  help="gets the topology by name")
@click.option("--layout", default=False, required=False,  help="gets the topology by name")
@click.option("--topo", default=False, required=False,  help="gets the topology by name")
@pass_config
def validate(config, topo, layout , lpf):
    """ validate module of linchpin cli : currenly validates only topologies, need to implement lpf, layouts too"""
    e_vars = {}
    e_vars["schema"] = config.clipath+"/ex_schemas/schema_v3.json"
    e_vars["data"] = topo
    #result = invoke_linchpin(config, e_vars, "SCHEMA_CHECK")
    result = invoke_linchpin(config, e_vars, "SCHEMA_CHECK", console=False)[-1]
    pprint.pprint(result.__dict__)
    

@cli.command()
@click.option("--layout", default=False, required=True,  help="layout file usually found in layout folder")
@click.option("--output", default=False, required=True,  help="topology output file usually found in output folders")
@pass_config
def invgen(config, output, layout):
    """ invgen module of linchpin cli """
    pass
