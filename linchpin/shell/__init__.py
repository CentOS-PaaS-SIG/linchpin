#!/usr/bin/env python

import os
import sys
import json
import click

from linchpin.cli import LinchpinCli
from linchpin.exceptions import LinchpinError
from linchpin.cli.context import LinchpinCliContext
from linchpin.shell.click_default_group import DefaultGroup


pass_context = click.make_pass_decorator(LinchpinCliContext, ensure=True)
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


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

        if task_results and isinstance(task_results[0], list):
            task_results = task_results[0]

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

        # PRINT OUTPUT RESULTS HERE
        for rundb_id, data in rundb_data.iteritems():

            output += '{0:<20}\t{1:>6}\t{2:>5}'.format(target,
                                                       rundb_id,
                                                       data['uhash'])

            output += '\t{0:>9}\n'.format(return_code)

    ctx.log_state(output)
    sys.exit(return_code)


@click.group(cls=DefaultGroup, default_if_no_args=True, default='help',
             invoke_without_command=True,
             context_settings=CONTEXT_SETTINGS)
@click.option('-c', '--config', type=click.Path(), envvar='LP_CONFIG',
              help='Path to config file')
@click.option('-p', '--pinfile', envvar='PINFILE', metavar='PINFILE',
              help='Use a name for the PinFile different from'
                   ' the configuration.')
@click.option('-d', '--template-data', metavar='TEMPLATE_DATA',
              help='Write out PinFile to provided location')
@click.option('-o', '--output-pinfile', metavar='OUTPUT_PINFILE',
              help='Template data passed to PinFile template')
@click.option('-w', '--workspace', type=click.Path(), envvar='WORKSPACE',
              help='Use the specified workspace. Also works if the'
                   ' familiar Jenkins WORKSPACE environment variable is set')
@click.option('-v', '--verbose', count=True, default=1,
              help='Enable verbose output')
@click.option('--version', is_flag=True,
              help='Prints the version and exits')
@click.option('--creds-path', type=click.Path(), envvar='CREDS_PATH',
              help='Use the specified credentials path. Also works'
                   ' if CREDS_PATH environment variable is set')
@pass_context
def runcli(ctx, config, pinfile, template_data, output_pinfile,
           workspace, verbose, version, creds_path):
    """linchpin: hybrid cloud orchestration"""

    ctx.load_config(lpconfig=config)
    # workspace arg in load_config used to extend linchpin.conf
    ctx.load_global_evars()
    ctx.setup_logging()

    ctx.verbosity = verbose

    # if the pinfile is a template, data will be passed here
    ctx.pf_data = template_data

    if output_pinfile:
        ctx.set_cfg('tmp', 'output_pinfile', output_pinfile)

    ctx.pinfile = None
    if pinfile:
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


@runcli.command('help', short_help='Prints help')
@click.pass_context
def help(ctx):
    """
    Print help
    """

    print(ctx.parent.get_help())


@runcli.command('init', short_help='Initializes a linchpin project.')
@pass_context
def init(ctx):
    """
    Initializes a linchpin project, which generates an example PinFile, and
    creates the necessary directory structure for topologies and layouts.

    """

    # add a providers option someday
    providers = None

    try:
        # lpcli.lp_init(pf_w_path, targets) # TODO implement targets option
        lpcli.lp_init(providers=providers)
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

    targets:    Provision ONLY the listed target(s). If omitted, ALL targets in
    the appropriate PinFile will be provisioned.

    run-id:     Use the data from the provided run_id value
    """

    try:
        return_code, results = lpcli.lp_up(targets=targets, run_id=run_id)
        _handle_results(ctx, results, return_code)
    except LinchpinError as e:
        ctx.log_state(e)
        sys.exit(1)


@runcli.command()
@click.argument('targets', metavar='TARGET', required=False,
                nargs=-1)
@click.option('-r', '--run-id', metavar='run_id',
              help='Destroy resources using `run-id` data')
@pass_context
def destroy(ctx, targets, run_id):
    """
    Destroys nodes from the given target(s) in the given PinFile.

    targets:    Destroy ONLY the listed target(s). If omitted, ALL targets in
    the appropriate PinFile will be destroyed.

    run-id:     Use the data from the provided run_id value
    """

    try:
        return_code, results = lpcli.lp_destroy(targets=targets, run_id=run_id)
        _handle_results(ctx, results, return_code)
    except LinchpinError as e:
        ctx.log_state(e)
        sys.exit(1)


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

    fetch_type:     Specifies which component of a workspace the user wants to
    fetch. Types include: topology, layout, resources, hooks, workspace

    remote:         The URL or URI of the remote directory

    """
    try:
        lpcli.lp_fetch(remote, root=root, fetch_type=''.join(fetch_type))
    except LinchpinError as e:
        ctx.log_state(e)
        sys.exit(1)


@runcli.command()
@click.argument('targets', metavar='TARGETS', required=True, nargs=-1)
@click.option('-c', '--count', metavar='COUNT', default=3, required=False,
              help='(up to) number of records to return (default: 3)')
@click.option('-f', '--fields', metavar='FIELDS', required=False,
              help='List the fields to display')
@pass_context
def journal(ctx, targets, fields, count):
    """
    Display information stored in Run Database

    targets:    Display data for the listed target(s). If omitted, the latest
                records for any/all targets in the RunDB will be displayed.

    fields:     Comma separated list of fields to show in the display.
    (Default: action, uhash, rc)

    (available fields are: uhash, rc, start, end, action)

    """

    all_fields = json.loads(lpcli.get_cfg('lp', 'rundb_schema')).keys()

    if not fields:
        fields = ['action', 'uhash', 'rc']
    else:
        fields = fields.split(',')

    invalid_fields = [field for field in fields if field not in all_fields]

    if invalid_fields:
        ctx.log_state('The following fields passed in are not valid: {0}'
                      ' \nValid fields are {1}'.format(fields, all_fields))
        sys.exit(89)

    no_records = []
    output = 'run_id\t'

    for f in fields:
        output += '{0:>10}\t'.format(f)

    output += '\n'
    output += '--------------------------------------------------'


    try:
        journal = lpcli.lp_journal(targets=targets, fields=fields, count=count)

        for target, values in journal.iteritems():

            keys = values.keys()
            if len(keys):
                print('\nTarget: {0}'.format(target))
                print(output)
                keys.sort(reverse=True)
                for run_id in keys:
                    if int(run_id) > 0:
                        out = '{0:<7}\t'.format(run_id)
                        for f in fields:
                            out += '{0:>9}\t'.format(values[run_id][f])

                        print(out)
            else:
                no_records.append(target)

        if no_records:
            no_out = '\nNo records for targets:'

            for rec in no_records:
                no_out += ' {0}'.format(rec)

            no_out += '\n'

            print(no_out)

    except LinchpinError as e:
        ctx.log_state(e)
        sys.exit(1)


def main():
    # print("entrypoint")
    pass
