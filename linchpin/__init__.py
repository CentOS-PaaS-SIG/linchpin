#!/usr/bin/env python

import os
import sys
import click
import shutil
import logging
import requests

from distutils import dir_util
from jinja2 import Environment, PackageLoader

from linchpin.cli import LinchpinCli
from linchpin.exceptions import LinchpinError
from linchpin.cli.context import LinchpinCliContext


pass_context = click.make_pass_decorator(LinchpinCliContext, ensure=True)
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


class LinchpinAliases(click.Group):

    lp_commands = ['init', 'up', 'destroy', 'fetch']
    lp_aliases = {
        'rise': 'up',
        'drop': 'destroy',
        'down': 'destroy',
    }

    def list_commands(self, ctx):
        """
        Provide a list of available commands. Anhthing deprecated should
        not be listed
        """

        return self.lp_commands

    def get_command(self, ctx, name):

        """
        Track aliases for specific commands and the commands and return the
        correct action.
        """

        cmd = self.lp_aliases.get(name)

        if cmd is None:
            cmd = name

        rv = click.Group.get_command(self, ctx, cmd)
        return rv


def _handle_results(ctx, results):
    """
    Handle results from the Ansible API. Either as a return value (retval)
    when running with the ansible console enabled, or as a list of TaskResult
    objects, and a return value.

    If a target fails along the way, this method immediately exits with the
    appropriate return value (retval). If the ansible console is disabled, an
    error message will be printed before exiting.

    :param results:
        The dictionary of results for each target.
    """

    retval = 0

    for k, v in results.iteritems():
        if not isinstance(v, int):
            trs = v

            if trs is not None:
                trs.reverse()
                tr = trs[0]
                if tr.is_failed():
                    msg = tr._check_key('msg')
                    ctx.log_state("Target '{0}': {1} failed with"
                                  " error '{2}'".format(k, tr._task, msg))
                    sys.exit(retval)
        else:
            if v:
                sys.exit(v)


@click.group(cls=LinchpinAliases,
             invoke_without_command=True,
             no_args_is_help=True,
             context_settings=CONTEXT_SETTINGS)
@click.option('-c', '--config', type=click.Path(), envvar='LP_CONFIG',
              help='Path to config file')
@click.option('-p', '--pinfile', envvar='PINFILE',
              help='Use a name for the PinFile different from'
                   ' the configuration.')
@click.option('-w', '--workspace', type=click.Path(), envvar='WORKSPACE',
              help='Use the specified workspace if the familiar Jenkins'
                   ' $WORKSPACE environment variable is not set')
@click.option('-v', '--verbose', is_flag=True, default=False,
              help='Enable verbose output')
@click.option('--version', is_flag=True,
              help='Prints the version and exits')
@click.option('--creds-path', type=click.Path(), envvar='LP_CREDS',
              help='Use the specified credentials path if CREDS_PATH'
                   'environment variable is not set')
@pass_context
def runcli(ctx, config, pinfile, workspace, verbose, version, creds_path):
    """linchpin: hybrid cloud orchestration"""

    ctx.load_config(lpconfig=config)
    # workspace arg in load_config used to extend linchpin.conf
    ctx.load_global_evars()
    ctx.setup_logging()
    ctx.verbose = verbose

    if pinfile:
        ctx.log_info('pinfile name changed to {0}'.format(pinfile))
        ctx.pinfile = pinfile

    if version:
        ctx.log_state('linchpin version {0}'.format(ctx.version))
        sys.exit(0)

    if creds_path is not None:
        ctx.set_evar('creds_path',
                     os.path.realpath(os.path.expanduser(creds_path)))

    if workspace is not None:
        ctx.workspace = os.path.realpath(os.path.expanduser(workspace))
        ctx.log_debug("ctx.workspace: {0}".format(ctx.workspace))

    # global LinchpinCli placeholder
    global lpcli
    lpcli = LinchpinCli(ctx)


@runcli.command('init', short_help='Initializes a linchpin project.')
@pass_context
def init(ctx):
    """
    Initializes a linchpin project, which generates an example PinFile, and
    creates the necessary directory structure for topologies and layouts.

    :param ctx: Context object defined by the click.make_pass_decorator method
    """

    pf_w_path = _get_pinfile_path(exists=False)

    try:
        # lpcli.lp_init(pf_w_path, targets) # TODO implement targets option
        lpcli.lp_init(pf_w_path)
    except LinchpinError as e:
        ctx.log_state(e)
        sys.exit(1)


@runcli.command()
@click.argument('targets', metavar='TARGETS', required=False,
                nargs=-1)
@pass_context
def up(ctx, targets):
    """
    Provisions nodes from the given target(s) in the given PinFile.

    :param ctx: Context object defined by the click.make_pass_decorator method

    :param pinfile:
        path to pinfile (Default: ctx.workspace)

    :param targets:
        Provision ONLY the listed target(s). If omitted, ALL targets in the
        appropriate PinFile will be provisioned.
    """

    pf_w_path = _get_pinfile_path()

    try:
        results = lpcli.lp_up(pf_w_path, targets)

        _handle_results(ctx, results)

    except LinchpinError as e:
        ctx.log_state(e)
        sys.exit(1)


@runcli.command()
@click.argument('targets', metavar='TARGET', required=False,
                nargs=-1)
@pass_context
def rise(ctx, targets):
    """
    DEPRECATED. Use 'up'

    """

    pass


@runcli.command()
@click.argument('targets', metavar='TARGET', required=False,
                nargs=-1)
@pass_context
def destroy(ctx, targets):
    """
    Destroys nodes from the given target(s) in the given PinFile.

    :param ctx: Context object defined by the click.make_pass_decorator method

    :param pinfile:
        path to pinfile (Default: ctx.workspace)

    :param targets:
        Destroy ONLY the listed target(s). If omitted, ALL targets in the
        appropriate PinFile will be destroyed.

    """

    pf_w_path = _get_pinfile_path()

    try:
        results = lpcli.lp_destroy(pf_w_path, targets)

        _handle_results(ctx, results)

    except LinchpinError as e:
        ctx.log_state(e)
        sys.exit(1)


@runcli.command()
@click.argument('targets', metavar='TARGET', required=False,
                nargs=-1)
@pass_context
def drop(ctx, targets):
    """
    DEPRECATED. Use 'destroy'.

    There are now two functions, `destroy` and `down` which perform node
    teardown. The `destroy` functionality is the default, and if drop is
    used, will be called.

    The `down` functionality is currently unimplemented, but will shutdown
    and preserve instances. This feature will only work on providers that
    support this option.

    """

    pass


@runcli.command()
@click.argument('fetch_type', default=None, required=True)
@click.argument('remote', default=None, required=True)
@click.option('-r','--root', required=False, default=None)
@pass_context
def fetch(ctx, fetch_type, remote, root):
    """
    Fetches a aspecified linchpin directory from a remote location.

    Fetch types: topology, layout, resources, hooks, workspace

    """
    lpcli = LinchpinCli(ctx)
    lpcli.lp_fetch(remote, fetch_type, root)
#    try:
#        lpcli.lp_fetch(remote, fetch_type, root)
#    except Exception as e:
#        raise LinchpinError("An error has occurred")
        
        

def _get_pinfile_path(pinfile=None, exists=True):

    if not pinfile:
        pinfile = lpcli.pinfile

    pf_w_path = '{0}/{1}'.format(lpcli.workspace, pinfile)

    if not os.path.exists(pf_w_path) and exists:
        lpcli.ctx.log_state('{0} not found in provided workspace: '
                            '{1}'.format(pinfile, lpcli.workspace))
        sys.exit(1)

    return pf_w_path


# @cli.group()
# @pass_config
# def topology(config):
#     pass
#
# @topology.command(name='list')
# @click.option('--upstream',
#               default=None,
#               required=False,
#               help="upstream url for topology")
# @pass_config
# def topology_list(config, upstream):
#     lpcli = LinchpinCli()
#     click.echo(": TOPOLOGIES LIST :")
#     files = lpcli.lp_topo_list(upstream)
#     t_files = []
#     for i in range(0, len(files)):
#         t_files.append((i+1, files[i]["name"]))
#     headers = ["Sno", "Name"]
#     print tabulate(t_files, headers, tablefmt="fancy_grid")
#
#
# @topology.command(name='get')
# @click.option('--upstream',
#               default=None,
#               required=False,
#               help="upstream url for topology")
# @click.argument('topo')
# @pass_config
# def topology_get(config, topo, upstream):
#     """
#     needs implementation if topology folder is not found raise error
#     """
#     lpcli = LinchpinCli()
#     d = lpcli.lp_topo_get(topo)
#     pprint.pprint(d)
#
#
# @cli.group()
# @pass_config
# def layout(config):
#     pass
#
#
# @layout.command(name='list')
# @click.option('--upstream',
#               default=None,
#               required=False,
#               help="upstream url for layouts")
# @pass_config
# def layouts_list(config, upstream):
#     lpcli = LinchpinCli()
#     click.echo(": LAYOUTS LIST :")
#     files = lpcli.lp_layout_list(upstream)
#     t_files = []
#     for i in range(0, len(files)):
#         t_files.append((i+1, files[i]["name"]))
#     headers = ["Sno", "Name"]
#     print tabulate(t_files, headers, tablefmt="fancy_grid")
#
#
# @layout.command(name='get')
# @click.option('--upstream',
#               default=None,
#               required=False,
#               help="upstream url for layouts")
# @click.argument('layout')
# @pass_config
# def layouts_get(config, layout, upstream):
#     """
#     needs implementation if layout folder is not found raise error
#     """
#     lpcli = LinchpinCli()
#     output = lpcli.lp_layout_get(layout, upstream)
#     pprint.pprint(output)
#
#
# @cli.command()
# @click.option("--pf",
#               default=False,
#               required=False,
#               help="gets the topology by name")
# @click.option("--target",
#               default="all",
#               required=False,
#               help="target name mentioned in PinFile")
# @pass_config
# def rise(config, pf, target):
#     """ rise module of linchpin cli """
#     init_dir = os.getcwd()
#     pfs = list_by_ext(init_dir, "PinFile")
#     if len(pfs) == 0:
#         display("ERROR:001")
#     if len(pfs) > 1:
#         display("ERROR:002")
#     pf = pfs[0]
#     lpcli = LinchpinCli()
#     output = lpcli.lp_rise(pf, target)
#
#
#
# @cli.command()
# @click.option("--pf",
#               default=False,
#               required=False,
#               help="gets the PinFile by name")
# @click.option("--layout",
#               default=False,
#               required=False,
#               help="gets the layout by name")
# @click.option("--topo",
#               default=False,
#               required=False,
#               help="gets the topology by name")
# @pass_config
# def validate(config, topo, layout, pf):
#     """ validate module of linchpin cli : currenly validates only topologies,
#         need to implement PinFile, layouts too"""
#     lpcli = LinchpinCli()
#     topo = os.path.abspath(topo)
#     output = lpcli.lp_validate(topo, layout, pf)
#     pprint.pprint(output)
#
#
# @cli.command()
# @click.option("--init",
#               default=False,
#               required=False,
#               is_flag=True,
#               help="Initialises config file")
# @click.option("--reset",
#               default=False,
#               required=False,
#               is_flag=True,
#               help="sets existing config file parameters")
# @pass_config
# def config(config, reset, init):
#     """ config module of linchpin cli"""
#     if reset:
#         if os.path.isfile("./linchpin_config.yml"):
#             display("WARNING:002", "prompt")
#         config.lpconfig.stream(playbook_dir=config.clipath,
#                                pwd=os.getcwd()).dump('linchpin_config.yml')
#     if init:
#         if not os.path.isfile("./linchpin_config.yml"):
#             display("ERROR:004", "print")
#         conf = yaml.load(open("linchpin_config.yml", "r").read())
#         for key in conf:
#             inp_str = raw_input("Enter value"
#                                 " of {0}:({1}):".format(key, str(conf[key])))
#
#             if inp_str != "":
#                 conf[key] = inp_str
#         config.lpconfig.stream(
#                          playbook_dir=config.clipath,
#                          keystore_path=conf["keystore_path"],
#                          outputfolder_path=conf["outputfolder_path"],
#                          inventoryfolder_path=conf["inventoryfolder_path"],
#                          async=conf["async"],
#                          async_timeout=conf["async_timeout"],
#                          no_output=conf["no_output"],
#                          schema=conf["schema"],
#                          default_layouts_path=conf["default_layouts_path"],
#                          inventory_outputs_path=conf["inventory_outputs_path"],
#                          check_mode=conf["check_mode"],
#                          pwd=os.getcwd()).dump('linchpin_config.yml')
#
#
# @cli.command()
# @click.option("--invtype", default="generic", required=False,
#               type=click.Path(),
#               help="inventory type")
# @click.option("--invout", required=True, type=click.Path(),
#               help="inventory output file")
# @click.option("--layout", default=False, required=True,  type=click.Path(),
#               help="layout file usually found in layout folder")
# @click.option("--topoout", default=False, required=True, type=click.Path(),
#               help="topology output file usually found in output folders")
# @pass_config
# def invgen(config, topoout, layout, invout, invtype):
#     """ invgen module of linchpin cli """
#     topoout = os.path.abspath(topoout)
#     layout = os.path.abspath(layout)
#     invout = os.path.abspath(invout)
#     lpcli = LinchpinCli()
#     result = lpcli.lp_invgen(topoout, layout, invout, invtype)
#     pprint.pprint(result)


def main():
    # print("entrypoint")
    pass
