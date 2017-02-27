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
from linchpin.cli.utils import write_to_file, touch 
from linchpin.cli import LinchpinCli
from tabulate import tabulate


class Context(object):
    """ Global context object accesible by all the click modules """
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

pass_context = click.make_pass_decorator(Context, ensure=True)
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(invoke_without_command=True, context_settings=CONTEXT_SETTINGS)
@click.option('-v', '--verbose', count=True)
@click.option('--home-directory', type=click.Path())
@click.option('--version', is_flag=True)
@pass_context
def cli(context, verbose, home_directory, version):
    """
    Welcome to linchpin command line client
    """
    context.verbose = verbose
    if home_directory is None:
        home_directory = '.'
    context.home_directory = home_directory
    if version:
        click.echo("LinchpinCLI "+Context.VERSION)
        click.echo("WORKSPACE = "+context.workspace)


@cli.command()
@pass_context
def init(context):
    """ init module of linchpin """
    click.echo('Initialising the templates for linchpin file !')
    click.echo('WORKSPACE = '+context.workspace)
    if checkpaths(context.workspace):
        reply = display("WARNING:001", "prompt")
        if not reply:
            sys.exit(0)
    if context.verbose:
        click.echo("### verbose mode ###")
    if os.path.isdir(context.workspace):
        path = context.workspace
        context.linchpinfile.stream().dump(path+'PinFile')
        for dir in context.INIT_DIR_LAYOUT:
            mkdir(path+dir)
        dir_list = ["topologies", "layouts"]
        copy_files(context.TEMPLATES_PATH, context.workspace, dir_list)
    else:
        click.echo("Invalid WORKSPACE to initialise!!")


@cli.command()
@click.option("--layout","-l", is_flag=True)
@click.option("--topology","-t", is_flag=True)
@click.option("--upstream", default=None, required=False)
@pass_context
def list(context, topology, layout, upstream):
    """ list module of linchpin """
    lpcli = LinchpinCli(context)
    if topology:
        click.echo(": TOPOLOGY LIST :")
        files = lpcli.lp_topo_list(upstream)
        tabulate_print(files, ['Sno', 'Name'])
    if layout:
        click.echo(": LAYOUT LIST :")
        files = lpcli.lp_layout_list(upstream)
        tabulate_print(files, ['Sno', 'Name'])


@cli.group()
@pass_context
def topology(context):
    pass


@topology.command(name='list')
@click.option('--upstream',
              default=None,
              required=False,
              help="upstream url for topology")
@pass_context
def topology_list(context, upstream):
    lpcli = LinchpinCli(context)
    click.echo(": TOPOLOGIES LIST :")
    files = lpcli.lp_topo_list(upstream)
    tabulate_print(files, ['Sno', 'Name'])


@topology.command(name='get')
@click.option('--upstream',
              default=None,
              required=False,
              help="upstream url for topology")
@click.argument('topo')
@pass_context
def topology_get(context, topo, upstream):
    """
    Get topology by name
    """
    lpcli = LinchpinCli(context)
    output = lpcli.lp_topo_get(topo)
    click.echo(output)
    dest_path = context.workspace+"/topologies/"+topo
    write_to_file(dest_path, output)


@cli.group()
@pass_context
def layout(context):
    pass


@layout.command(name='list')
@click.option('--upstream',
              default=None,
              required=False,
              help="upstream url for layouts")
@pass_context
def layouts_list(context, upstream):
    lpcli = LinchpinCli(context)
    click.echo(": LAYOUTS LIST :")
    files = lpcli.lp_layout_list(upstream)
    tabulate_print(files, ['Sno', 'Name'])


@layout.command(name='get')
@click.option('--upstream',
              default=None,
              required=False,
              help="upstream url for layouts")
@click.argument('layout')
@pass_context
def layouts_get(context, layout, upstream):
    """
    Get layout by name
    """
    lpcli = LinchpinCli(context)
    output = lpcli.lp_layout_get(layout, upstream)
    click.echo(output)
    dest_path = context.workspace+"/layouts/"+layout
    write_to_file(dest_path, output)


@cli.command()
@click.option("--pf",
              default=False,
              required=False,
              help="gets the topology by name")
@click.argument('targets', nargs=-1)
@pass_context
def rise(context, pf, targets):
    """ rise module of linchpin cli """
    click.echo(targets)
    init_dir = os.getcwd()
    pfs = list_by_ext(init_dir, "PinFile")
    if len(pfs) == 0:
        display("ERROR:001")
    if len(pfs) > 1:
        display("ERROR:002")
    pf = pfs[0]
    lpcli = LinchpinCli(context)
    output = lpcli.lp_rise(pf, targets)


@cli.command()
#@click.option("--target", default="all", required=False,  help="target cloud")
@click.option("--pf", default=False, required=False,  help="path of Pinfile")
@click.argument('targets', nargs=-1)
@pass_context
def drop(context, pf, targets):
    """ drop module of linchpin cli"""
    click.echo(targets)
    init_dir = os.getcwd()
    pfs = list_by_ext(init_dir, "PinFile")
    if len(pfs) == 0:
        display("ERROR:001")
    if len(pfs) > 1:
        display("ERROR:002")
    pf = pfs[0]
    lpcli = LinchpinCli(context)
    output = lpcli.lp_drop(pf, targets)

@cli.group()
@pass_context
def config(context):
        pass


@config.command(name='init')
@pass_context
def config_init(context):
    if os.path.isfile(context.workspace+"/linchpin_config.yml"):
        click.confirm("Linchpin config exists would you like to overrite it?",
                      abort=True)
    playbook_dir = click.prompt('Please enter playbook directory',
                                default=context.clipath)
    keystore_path = click.prompt('Please enter keystore path',
                                 default=context.workspace+'keystore')
    outputfolder_path = click.prompt('Please enter outputfolder path ',
                                     default=context.workspace+'outputs')
    async = click.prompt('Please enter async mode',
                         default='false')
    async_timeout = click.prompt('Please enter async timeout',
                                 default=999)
    no_output = click.prompt('no output mode',
                             default='false')
    inventory_layouts_path = click.prompt('Please enter a inventory \
                                          layouts path',
                                          default=context.workspace+'layouts')
    inventory_outputs_path = click.prompt('Please enter inventory outputs',
                                          default=context.workspace+'inventories')
    check_mode = click.prompt('checkmode', default='no')
    pwd = context.workspace
    context.lpconfig.stream(
                     playbook_dir=playbook_dir,
                     keystore_path=keystore_path,
                     outputfolder_path=outputfolder_path,
                     async=async,
                     async_timeout=async_timeout,
                     no_output=no_output,
                     inventory_layouts_path=inventory_layouts_path,
                     inventory_outputs_path=inventory_outputs_path,
                     check_mode=check_mode,
                     pwd=pwd).dump('linchpin_config.yml')


@cli.group()
@pass_context
def validate(context):
    pass


@validate.command(name='topology')
@click.argument('topology', nargs=1)
@pass_context
def validate_topology(context, topology):
    click.echo("inside validate topology")
    lpcli = LinchpinCli(context)
    click.echo(topology)
    topology = os.path.abspath(topology)
    result = lpcli.lp_validate_topology(topology)
    return result


@cli.command()
@click.option("--invtype","-it",
              default="generic",
              required=False,
              type=click.Path(),
              prompt=True,
              help="options: generic | openstack | aws | gcloud | libvirt")
@click.option("--invout","-io",
              required=True,
              type=click.Path(),
              prompt=True,
              help="inventory output file path")
@click.option("--layout","-l",
              required=True,
              prompt=True,
              type=click.Path(),
              help="layout file path")
@click.option("--topoout","-to",
              required=True,
              type=click.Path(),
              prompt=True,
              help="topology output file usually found in output folders")
@pass_context
def invgen(context, topoout, layout, invout, invtype):
    """ invgen module of linchpin cli """
    topoout = os.path.abspath(topoout)
    layout = os.path.abspath(layout)
    touch(invout)
    invout = os.path.abspath(invout)
    lpcli = LinchpinCli(context)
    result = lpcli.lp_invgen(topoout, layout, invout, invtype)
