import os
import yaml
import click
import sys
import pdb
import pprint
import os.path
from tabulate import tabulate
from jinja2 import Environment, PackageLoader
from cli.utils import checkpaths, display, mkdir, copy_files, list_by_ext
from cli.cli import LinchpinCli


class Config(object):
    """ Global config object accesible by all the click modules """
    def __init__(self):
        self.verbose = False
        self.env = Environment(loader=PackageLoader('linchpin', 'templates'))
        self.linchpinfile = self.env.get_template('PinFile.j2')
        self.lpconfig = self.env.get_template('linchpin_config.yml.j2')
        self.clipath = os.path.dirname(os.path.realpath(__file__))
        self.dir_list = ["layouts", "topologies"]

pass_config = click.make_pass_decorator(Config, ensure=True)


@click.group()
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
@click.option("--path",
              default=".",
              type=click.Path(),
              required=False,
              help="path for initialisation")
@pass_config
def init(config, path):
    """ init module of linchpin """
    click.echo('Initailising the templates for linchpin file !')
    if checkpaths():
        reply = display("WARNING:001", "prompt")
        if not reply:
            sys.exit(0)
    if config.verbose:
        click.echo("### verbose mode ###")
    if os.path.isdir(path):
        path = path.strip("/")
        config.linchpinfile.stream().dump(path+'/'+'PinFile')
        config_path = path+'/'+'linchpin_config.yml'
        config.lpconfig.stream(pwd=path,
                               playbook_dir=config.clipath).dump(config_path)
        mkdir(path+"/topologies")
        mkdir(path+"/layouts")
        mkdir(path+"/inventory")
        dir_list = ["topologies", "layouts"]
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
def list(ctx, config, topos, layouts):
    """ list module of linchpin  """
    if (not topos) and (not layouts): 
        click.echo('linchpin list usage linchpin list <--topos> <--layouts> ')
    headers = ["Sno","Name"]
    if topos and layouts:
        t_l = linchpin_list(config, topos, layouts)
        click.echo(": TOPOLOGIES LIST :")
        print tabulate(t_l[0], headers, tablefmt="fancy_grid")
        click.echo(": LAYOUTS LIST :")
        print tabulate(t_l[1], headers, tablefmt="fancy_grid")
        # sys.exit(0)
    if topos:
        click.echo(": TOPOLOGIES LIST :")
        files = linchpin_list(config, topos, layouts)
        print tabulate(files, headers, tablefmt="fancy_grid")
    if layouts:
        click.echo(": LAYOUTS LIST :")
        files = linchpin_list(config, topos, layouts)
        print tabulate(files, headers, tablefmt="fancy_grid")
        

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
    lpcli = LinchpinCli()
    click.echo(": TOPOLOGIES LIST :")
    files = lpcli.lp_topo_list(upstream)
    t_files = []
    for i in range(0, len(files)):
        t_files.append((i+1, files[i]["name"]))
    headers = ["Sno", "Name"]
    print tabulate(t_files, headers, tablefmt="fancy_grid")


@topology.command(name='get')
@click.option('--upstream',
              default=None,
              required=False,
              help="upstream url for topology")
@click.argument('topo')
@pass_config
def topology_get(config, topo, upstream):
    """
    needs implementation if topology folder is not found raise error
    """
    lpcli = LinchpinCli()
    d = lpcli.lp_topo_get(topo)
    pprint.pprint(d)


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
    lpcli = LinchpinCli()
    click.echo(": LAYOUTS LIST :")
    files = lpcli.lp_layout_list(upstream)
    t_files = []
    for i in range(0, len(files)):
        t_files.append((i+1, files[i]["name"]))
    headers = ["Sno", "Name"]
    print tabulate(t_files, headers, tablefmt="fancy_grid")


@layout.command(name='get')
@click.option('--upstream',
              default=None,
              required=False,
              help="upstream url for layouts")
@click.argument('layout')
@pass_config
def layouts_get(config, layout, upstream):
    """
    needs implementation if layout folder is not found raise error
    """
    lpcli = LinchpinCli()
    output = lpcli.lp_layout_get(layout, upstream)
    pprint.pprint(output)


@cli.command()
@click.option("--lpf",
              default=False,
              required=False,
              help="gets the topology by name")
@click.option("--target",
              default="all",
              required=False,
              help="target name mentioned in PinFile")
@pass_config
def rise(config, lpf, target):
    """ rise module of linchpin cli """
    init_dir = os.getcwd()
    lpfs = list_by_ext(init_dir, "PinFile")
    if len(lpfs) == 0:
        display("ERROR:001")
    if len(lpfs) > 1:
        display("ERROR:002")
    lpf = lpfs[0]
    lpcli = LinchpinCli()
    output = lpcli.lp_rise(lpf, target)


@cli.command()
@click.option("--target", default="all", required=False,  help="target cloud")
@click.option("--lpf", default=False, required=False,  help="path of Pinfile")
@pass_config
def drop(config, lpf, target):
    """ drop module of linchpin cli"""
    init_dir = os.getcwd()
    lpfs = list_by_ext(init_dir, "PinFile")
    if len(lpfs) == 0:
        display("ERROR:001")
    if len(lpfs) > 1:
        display("ERROR:002")
    lpf = lpfs[0]
    lpcli = LinchpinCli()
    output = lpcli.lp_drop(lpf, target)


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
    """ validate module of linchpin cli : currenly validates only topologies,
        need to implement lpf, layouts too"""
    lpcli = LinchpinCli()
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
    lpcli = LinchpinCli()
    result = lpcli.lp_invgen(topoout, layout, invout, invtype)
