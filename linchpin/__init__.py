import os
import yaml
import click
import sys
import pprint
import os.path
from tabulate import tabulate
from jinja2 import Environment, PackageLoader
from linchpin.cli.utils import checkpaths, display, mkdir
from linchpin.cli.utils import list_by_ext, copy_files, tabulate_print
from linchpin.cli.utils import write_to_file 
from linchpin.cli import LinchpinCli
from tabulate import tabulate


class Config(object):
    """ Global config object accesible by all the click modules """
    VERSION = "v1.0.0"
    def __init__(self):
        self.clipath = os.path.dirname(os.path.realpath(__file__))
        self.env = Environment(loader=PackageLoader('linchpin', 'templates'))
        self.linchpinfile = self.env.get_template('PinFile.j2')
        self.lpconfig = self.env.get_template('linchpin_config.yml.j2')
        self.INIT_DIR_LAYOUT = ['topologies', 'layouts', 'inventories']
        self.TEMPLATES_PATH  = self.clipath+"/templates/" 
        self.workspace = os.environ.get('LINCHPIN_WORKSPACE', False)
        if not self.workspace:
            self.workspace = os.environ.get('PWD')+"/"

pass_config = click.make_pass_decorator(Config, ensure=True)
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(invoke_without_command=True, context_settings=CONTEXT_SETTINGS)
@click.option('-v', '--verbose', count=True)
@click.option('--home-directory', type=click.Path())
@click.option('--version', is_flag=True)
@pass_config
def cli(config, verbose, home_directory, version):
    """
    Welcome to linchpin command line client
    """
    config.verbose = verbose
    if home_directory is None:
        home_directory = '.'
    config.home_directory = home_directory
    if version:
        click.echo("LinchpinCLI "+Config.VERSION)
        click.echo("WORKSPACE = "+config.workspace)


@cli.command()
@pass_config
def init(config):
    """ init module of linchpin """
    click.echo('Initialising the templates for linchpin file !')
    click.echo('WORKSPACE = '+config.workspace)
    if checkpaths(config.workspace):
        reply = display("WARNING:001", "prompt")
        if not reply:
            sys.exit(0)
    if config.verbose:
        click.echo("### verbose mode ###")
    if os.path.isdir(config.workspace):
        path = config.workspace
        config.linchpinfile.stream().dump(path+'PinFile')
        for dir in config.INIT_DIR_LAYOUT:
            mkdir(path+dir)
        dir_list = ["topologies", "layouts"]
        copy_files(config.TEMPLATES_PATH, config.workspace, dir_list)
        #copy_files(path, dir_list, config)
    else:
        click.echo("Invalid WORKSPACE to initialise!!")


@cli.command()
@click.option("--layout","-l", is_flag=True)
@click.option("--topology","-t", is_flag=True)
@click.option("--upstream", default=None, required=False)
@pass_config
def list(config, topology, layout, upstream):
    """ list module of linchpin """
    lpcli = LinchpinCli(config)
    if topology:
        click.echo(": TOPOLOGY LIST :")
        files = lpcli.lp_topo_list(upstream)
        tabulate_print(files, ['Sno', 'Name'])
    if layout:
        click.echo(": LAYOUT LIST :")
        files = lpcli.lp_layout_list(upstream)
        tabulate_print(files, ['Sno', 'Name'])


@cli.group()
@pass_config
def topology(config):
    pass


@topology.command(name='list')
@click.option('--upstream',
              default=None,
              required=False,
              help="upstream url for topology")
@pass_config
def topology_list(config, upstream):
    lpcli = LinchpinCli(config)
    click.echo(": TOPOLOGIES LIST :")
    files = lpcli.lp_topo_list(upstream)
    tabulate_print(files, ['Sno', 'Name'])


@topology.command(name='get')
@click.option('--upstream',
              default=None,
              required=False,
              help="upstream url for topology")
@click.argument('topo')
@pass_config
def topology_get(config, topo, upstream):
    """
    Get topology by name
    """
    lpcli = LinchpinCli(config)
    output = lpcli.lp_topo_get(topo)
    click.echo(output)
    dest_path = config.workspace+"/topologies/"+topo
    write_to_file(dest_path, output)


@cli.group()
@pass_config
def layout(config):
    pass


@layout.command(name='list')
@click.option('--upstream',
              default=None,
              required=False,
              help="upstream url for layouts")
@pass_config
def layouts_list(config, upstream):
    lpcli = LinchpinCli(config)
    click.echo(": LAYOUTS LIST :")
    files = lpcli.lp_layout_list(upstream)
    tabulate_print(files, ['Sno', 'Name'])


@layout.command(name='get')
@click.option('--upstream',
              default=None,
              required=False,
              help="upstream url for layouts")
@click.argument('layout')
@pass_config
def layouts_get(config, layout, upstream):
    """
    Get layout by name
    """
    lpcli = LinchpinCli(config)
    output = lpcli.lp_layout_get(layout, upstream)
    click.echo(output)
    dest_path = config.workspace+"/layouts/"+layout
    write_to_file(dest_path, output)


@cli.command()
@click.option("--pf",
              default=False,
              required=False,
              help="gets the topology by name")
@click.argument('targets', nargs=-1)
#@click.option("--target",
#              default="all",
#              required=False,
#              help="target name mentioned in PinFile")
@pass_config
def rise(config, pf, targets):
    """ rise module of linchpin cli """
    click.echo(targets)
    init_dir = os.getcwd()
    pfs = list_by_ext(init_dir, "PinFile")
    if len(pfs) == 0:
        display("ERROR:001")
    if len(pfs) > 1:
        display("ERROR:002")
    pf = pfs[0]
    lpcli = LinchpinCli(config)
    output = lpcli.lp_rise(pf, targets)


@cli.command()
#@click.option("--target", default="all", required=False,  help="target cloud")
@click.option("--pf", default=False, required=False,  help="path of Pinfile")
@click.argument('targets', nargs=-1)
@pass_config
def drop(config, pf, targets):
    """ drop module of linchpin cli"""
    click.echo(targets)
    init_dir = os.getcwd()
    pfs = list_by_ext(init_dir, "PinFile")
    if len(pfs) == 0:
        display("ERROR:001")
    if len(pfs) > 1:
        display("ERROR:002")
    pf = pfs[0]
    lpcli = LinchpinCli(config)
    output = lpcli.lp_drop(pf, targets)


@cli.command()
@click.option("--pf",
              default=False,
              required=False,
              help="gets the PinFile by name")
@click.option("--layout",
              default=False,
              required=False,
              help="gets the layout by name")
@click.option("--topo",
              default=False,
              required=False,
              help="gets the topology by name")
@pass_config
def validate(config, topo, layout, pf):
    """ validate module of linchpin cli : 
        validates only topologies for now
    """
    lpcli = LinchpinCli(config)
    topo = os.path.abspath(topo)
    output = lpcli.lp_validate(topo, layout, pf)
    pprint.pprint(output)


@cli.command()
@click.option("--init",
              default=False,
              required=False,
              is_flag=True,
              help="Initialises config file")
@click.option("--reset",
              default=False,
              required=False,
              is_flag=True,
              help="sets existing config file parameters")
@pass_config
def config(config, reset, init):
    """ config module of linchpin cli"""
    if reset:
        if os.path.isfile("./linchpin_config.yml"):
            display("WARNING:002", "prompt")
        config.lpconfig.stream(playbook_dir=config.clipath,
                               pwd=os.getcwd()).dump('linchpin_config.yml')
    if init:
        if not os.path.isfile("./linchpin_config.yml"):
            display("ERROR:004", "print")
        conf = yaml.load(open("linchpin_config.yml", "r").read())
        for key in conf:
            inp_str = raw_input("Enter value of "+key+":("+str(conf[key])+"):")
            if inp_str != "":
                conf[key] = inp_str
        config.lpconfig.stream(
                         playbook_dir=config.clipath,
                         keystore_path=conf["keystore_path"],
                         outputfolder_path=conf["outputfolder_path"],
                         inventoryfolder_path=conf["inventoryfolder_path"],
                         async=conf["async"],
                         async_timeout=conf["async_timeout"],
                         no_output=conf["no_output"],
                         schema=conf["schema"],
                         inventory_layouts_path=conf["inventory_layouts_path"],
                         inventory_outputs_path=conf["inventory_outputs_path"],
                         check_mode=conf["check_mode"],
                         pwd=os.getcwd()).dump('linchpin_config.yml')


@cli.command()
@click.option("--invtype", default="generic", required=False,
              type=click.Path(),
              help="inventory type")
@click.option("--invout", required=True, type=click.Path(),
              help="inventory output file")
@click.option("--layout", default=False, required=True,  type=click.Path(),
              help="layout file usually found in layout folder")
@click.option("--topoout", default=False, required=True, type=click.Path(),
              help="topology output file usually found in output folders")
@pass_config
def invgen(config, topoout, layout, invout, invtype):
    """ invgen module of linchpin cli """
    topoout = os.path.abspath(topoout)
    layout = os.path.abspath(layout)
    invout = os.path.abspath(invout)
    lpcli = LinchpinCli(config)
    result = lpcli.lp_invgen(topoout, layout, invout, invtype)
    pprint.pprint(result)
