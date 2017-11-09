#!/usr/bin/env python

import os
import sys
import click

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


def _handle_results(ctx, results, return_code):
    """
    Handle results from the RunDB output and Ansible API.
    Either as a return value (retval) when running with the
    ansible console enabled, or as a list of TaskResult
    objects, and a return value.

    If a target fails along the way, this method immediately exits with the
    appropriate return value (retval). If the ansible console is disabled, an
    error message will be printed before exiting.

    :param results:
        The dictionary of results for each target.
    """

    output = '\n{0:<20}\t{1:<6}\t{2:<5}\t{3:<10}\n'.format('Target',
                                                           'Run ID',
                                                           'uHash',
                                                           'Exit Code')
    output += '-------------------------------------------------\n'

    for target, data in results.iteritems():
        rundb_data = data['rundb_data']
        task_results = data['task_results']

        return_code = 99

        # PRINT OUTPUT RESULTS HERE
        for rundb_id, data in rundb_data.iteritems():

            output += '{0:<20}\t{1:>6}\t{2:>5}'.format(target,
                                                       rundb_id,
                                                       data['uhash'])

            return_code = data['rc']
            output += '\t{0:>9}\n'.format(return_code)

        if not isinstance(task_results, int):
            trs = task_results

            if trs is not None:
                trs.reverse()
                tr = trs[0]
                if tr.is_failed():
                    msg = tr._check_key('msg')
                    ctx.log_state("Target '{0}': {1} failed with"
                                  " error '{2}'".format(target, tr._task, msg))
        else:
            if task_results:
                return_code = task_results


    ctx.log_state(output)
    sys.exit(return_code)


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
@click.option('--creds-path', type=click.Path(), envvar='CREDS_PATH',
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
@click.option('-r', '--run-id', metavar='run_id',
              help='Idempotently provision using `run-id` data')
@pass_context
def up(ctx, targets, run_id):
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
        return_code, results = lpcli.lp_up(pf_w_path, targets, run_id=run_id)
        _handle_results(ctx, results, return_code)

    except LinchpinError as e:
        ctx.log_state(e)
        sys.exit(1)


@runcli.command()
@click.argument('targets', metavar='TARGET', required=False, nargs=-1)
@pass_context
def rise(ctx, targets):
    """
    DEPRECATED. Use 'up'

    """

    pass


@runcli.command()
@click.argument('targets', metavar='TARGET', required=False,
                nargs=-1)
@click.option('-r', '--run-id', metavar='run_id',
              help='Destroy resources using `run-id` data')
@pass_context
def destroy(ctx, targets, run_id):
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
        return_code, results = lpcli.lp_destroy(pf_w_path,
                                                targets,
                                                run_id=run_id)

        _handle_results(ctx, results, return_code)

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
@click.argument('fetch_type', default=None, required=False, nargs=-1)
@click.argument('remote', default=None, required=True, nargs=1)
@click.option('-r', '--root', default=None, required=False,
              help='Use this to specify the subdirectory of the workspace of'
              ' the root url')
@pass_context
def fetch(ctx, fetch_type, remote, root):
    """
    Fetches a specified linchpin workspace or component from a remote location.

    :param fetch_type: Specifies which component of a workspace the user
    wants to fetch. Types include: topology, layout, resources, hooks, workspace

    :param REMOTE: The URL or URI of the remote directory

    """
    try:
        lpcli.lp_fetch(remote, ''.join(fetch_type), root)
    except LinchpinError as e:
        ctx.log_state(e)
        sys.exit(1)


def _get_pinfile_path(pinfile=None, exists=True):

    if not pinfile:
        pinfile = lpcli.pinfile

    pf_w_path = '{0}/{1}'.format(lpcli.workspace, pinfile)

    if not os.path.exists(pf_w_path) and exists:
        lpcli.ctx.log_state('{0} not found in provided workspace: '
                            '{1}'.format(pinfile, lpcli.workspace))
        sys.exit(1)

    return pf_w_path


def main():
    # print("entrypoint")
    pass
