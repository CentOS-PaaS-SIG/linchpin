#!/usr/bin/env python

from __future__ import print_function

import os
import sys
import ast
import json
import click

from collections import OrderedDict

from linchpin.cli import LinchpinCli
from linchpin.exceptions import LinchpinError
from linchpin.cli.context import LinchpinCliContext
from linchpin.shell.click_default_group import DefaultGroup
from linchpin.shell.mutually_exclusive import MutuallyExclusiveOption


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

    output = 'Nothing to do. Check input and try again.'
    rcs = [return_code]

    for k, v in results.iteritems():

        output = '\nID: {0}\n'.format(k)
        output += 'Action: {0}\n'.format(v['action'])
        output += '\n{0:<20}\t{1:>6}\t{2:<5}\t{3:<10}\n'.format('Target',
                                                                'Run ID',
                                                                'uHash',
                                                                'Exit Code')
        output += '-------------------------------------------------\n'
        for target, run_data in v['summary_data'].iteritems():
            for rundb_id, data in run_data.iteritems():

                output += '{0:<20}\t{1:>6}\t{2:>5}'.format(target,
                                                           rundb_id,
                                                           data['uhash'])
                output += '\t{0:>9}\n'.format(data['rc'])

                # add all return codes to a little dictionary for use with
                # a future flag that allows to record failures, but continue
                # on anyway.
                rcs.append(data['rc'])

        task_results = v.get('results_data')
        if task_results:
            for target, results in task_results.iteritems():
                if results['task_results']:
                    tasks = results['task_results'][0].get('failed')

                    if not isinstance(tasks, int) and len(tasks):
                        trs = tasks

                        if trs is not None:
                            trs.reverse()
                            tr = trs[0]
                            msg = tr._check_key('msg')
                            ctx.log_state("\n--------------------------------"
                                          "----")
                            ctx.log_state("Task '{0}' failed with"
                                          " error '{1}' for Target:"
                                          " {2}".format(tr.task_name,
                                                        msg,
                                                        target))
                            ctx.log_state("\n\nAdd -vvvv to the linchpin"
                                          " command to see the stack trace")
                            ctx.log_state("----------------------------------"
                                          "--\n")

                # FIXME make sure the return_code is valid here

    # PRINT OUTPUT RESULTS HERE
    ctx.log_state(output)
    uar = lpcli.get_cfg('lp', 'use_actual_rcs')
    use_actual_rcs = ast.literal_eval(uar.title())

    if use_actual_rcs:
        return_code = min(rcs)
    else:
        return_code = sum(rc for rc in rcs)

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
              help="Template data passed to PinFile template.\n\n"
                   "If template data is from a file, it must be"
                   " prepended with an '@' character."
              )
@click.option('-o', '--output-file', '--output-pinfile', 'outfile',
              metavar='OUTPUT_FILE',
              help='Write out PinFile to provided location')
@click.option('-w', '--workspace', type=click.Path(), envvar='WORKSPACE',
              help='Use the specified workspace. Also works if the'
                   ' familiar Jenkins WORKSPACE environment variable is set')
@click.option('-v', '--verbose', count=True, default=0,
              help='Enable verbose output')
@click.option('--version', is_flag=True,
              help='Prints the version and exits')
@click.option('--creds-path', type=click.Path(), envvar='CREDS_PATH',
              help='Use the specified credentials path. Also works'
                   ' if CREDS_PATH environment variable is set')
@click.option('--ask-vault-pass', is_flag=True, default=False,
              help='Prompts for vault password')
@pass_context
def runcli(ctx, config, pinfile, template_data, outfile,
           workspace, verbose, version, creds_path, ask_vault_pass):
    """linchpin: hybrid cloud orchestration"""

    ctx.load_config(lpconfig=config)
    # workspace arg in load_config used to extend linchpin.conf
    ctx.load_global_evars()
    ctx.setup_logging()

    ctx.verbosity = verbose

    # if the pinfile is a template, data will be passed here
    ctx.pf_data = template_data
    ctx.outfile = None
    if outfile:
        ctx.outfile = outfile
        ctx.set_cfg('tmp', 'outfile', outfile)

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

    ctx.ask_vault_pass = ask_vault_pass


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
@click.argument('provider', metavar='PROVIDER', required=False, nargs=1)
@pass_context
def init(ctx, provider):
    """
    Initializes a linchpin project, which generates an example PinFile, and
    creates the necessary directory structure for topologies and layouts.

    Utilizes lp_fetch with the following parameters:

    remote:         git://github.com/CentOS-PaaS-SIG/linchpin
    root:           workspaces
    fetch_type:     workspace
    fetch_protocol: FetchGit
    fetch_ref:      master
    dest_ws:        Unused, will use workspace/provider
    nocache:        True


    """

    remote = ctx.get_cfg('init', 'remote',
                         default='git://github.com/CentOS-PaaS-SIG/linchpin')
    root = ctx.get_cfg('init', 'root', default='workspaces/dummy')
    fetch_type = ctx.get_cfg('init', 'fetch_type', default='workspace')
    fetch_proto = 'FetchGit'
    fetch_ref = ctx.get_cfg('init', 'fetch_ref', default='master')
    nocache = ast.literal_eval(ctx.get_cfg('init', 'nocache', default='True'))

    if provider:
        root = 'workspaces/{0}'.format(provider)

    try:
        lpcli.lp_fetch(remote, root=root, fetch_type=fetch_type,
                       fetch_protocol=fetch_proto, fetch_ref=fetch_ref,
                       dest_ws=None, nocache=nocache)
    except LinchpinError as e:
        ctx.log_state(e)
        sys.exit(1)


@runcli.command()
@click.argument('targets', metavar='TARGETS', required=False,
                nargs=-1)
@click.option('-r', '--run-id', metavar='run_id', type=int,
              help='Idempotently provision using `run-id` data',
              cls=MutuallyExclusiveOption, mutually_exclusive=["tx_id"])
@click.option('-t', '--tx-id', metavar='tx_id', type=int,
              help='Provision resources using the Transaction ID (tx-id)',
              cls=MutuallyExclusiveOption, mutually_exclusive=["run_id"])
@click.option('--inventory-format', '--if', 'inventory_format', default="cfg",
              metavar='INVENTORY_FORMAT', help="Inventory format cfg/json")
@click.option('--ignore-failed-hooks', '--ifh', 'ignore_failed_hooks',
              is_flag=True, default=False, metavar='IGNORE_FAILED_HOOKS',
              help='Ignores failed hooks')
@click.option('--no-hooks', '--nh', 'no_hooks', is_flag=True, default=None,
              metavar='NO_HOOKS', help='Do not run hooks')
@pass_context
def up(ctx, targets, run_id, tx_id, inventory_format, ignore_failed_hooks,
       no_hooks):
    """
    Provisions nodes from the given target(s) in the given PinFile.

    The `run_id` requires an associated target, where the `tx_id` will look up
    the targets from the specified transaction.

    The data from the targets is obtained from the PinFile (default).
    By setting `use_rundb_for_actions = True` in linchpin.conf, any
    up transaction which use the `-r/--run_id` or `-t/--tx_id` option will
    obtain target data from the RunDB.

    targets:    Provision ONLY the listed target(s). If omitted, ALL targets in
    the appropriate PinFile will be provisioned.

    run-id:     Use the data from the provided run_id value
    """
    vault_pass = os.environ.get('VAULT_PASSWORD', '')

    if ctx.ask_vault_pass:
        vault_pass = click.prompt("enter vault password", hide_input=True)

    ctx.set_evar('vault_pass', vault_pass)

    if ignore_failed_hooks:
        ctx.set_cfg("hook_flags", "ignore_failed_hooks", ignore_failed_hooks)
    if no_hooks:
        ctx.set_cfg("hook_flags", "no_hooks", no_hooks)

    if tx_id:
        try:
            return_code, results = lpcli.lp_up(targets=targets,
                                               tx_id=tx_id,
                                               inv_f=inventory_format)
            _handle_results(ctx, results, return_code)
        except LinchpinError as e:
            ctx.log_state(e)
            sys.exit(1)
    else:  # if tx_id is not passed, use run_id as a baseline
        if (not len(targets) or len(targets) > 1) and run_id:
            raise click.UsageError("A single target is required when calling"
                                   " destroy with `--run_id` option")
        try:
            return_code, results = lpcli.lp_up(targets=targets,
                                               run_id=run_id,
                                               tx_id=tx_id,
                                               inv_f=inventory_format)
            _handle_results(ctx, results, return_code)
        except LinchpinError as e:
            ctx.log_state(e)
            sys.exit(1)

#    try:
#        return_code, results = lpcli.lp_up(targets=targets, run_id=run_id)
#        _handle_results(ctx, results, return_code)
#    except LinchpinError as e:
#        ctx.log_state(e)
#        sys.exit(1)


@runcli.command()
@click.argument('targets', metavar='TARGET', required=False,
                nargs=-1)
@click.option('-r', '--run-id', metavar='run_id', type=int,
              help='Destroy resources using a target-based ID (run-id)',
              cls=MutuallyExclusiveOption, mutually_exclusive=["tx_id"])
@click.option('-t', '--tx-id', metavar='tx_id', type=int,
              help='Destroy resources using the transaction ID (tx-id)',
              cls=MutuallyExclusiveOption, mutually_exclusive=["run_id"])
@click.option('--ignore-failed-hooks', '--ifh', 'ignore_failed_hooks',
              metavar='ignore_failed_hooks', is_flag=True, default=False,
              help='Ignores failed hooks')
@click.option('--no-hooks', '--nh', 'no_hooks', metavar='NO_HOOKS',
              is_flag=True, help='Do not run hooks')
@pass_context
def destroy(ctx, targets, run_id, tx_id, ignore_failed_hooks, no_hooks):
    """
    Destroys resources using either the run_id or tx_id (mutually exclusive).

    The run_id requires an associated target, where the tx_id will look up
    the targets from the specified transaction.

    The data from the targets is obtained from the PinFile (default) or from
    the RunDB (by setting `use_rundb_for_actions = True` in linchpin.conf).

    targets:    Destroy ONLY the listed target(s). If omitted, ALL targets in
    the appropriate PinFile will be destroyed.

    """
    vault_pass = os.environ.get('VAULT_PASSWORD', '')
    if ctx.ask_vault_pass:
        vault_pass = click.prompt("enter vault password", hide_input=True)

    ctx.set_evar('vault_pass', vault_pass)

    if ignore_failed_hooks:
        ctx.set_cfg("hook_flags", "ignore_failed_hooks", ignore_failed_hooks)
    if no_hooks:
        ctx.set_cfg("hook_flags", "no_hooks", no_hooks)


    if tx_id:
        try:
            return_code, results = lpcli.lp_destroy(targets=targets,
                                                    tx_id=tx_id)
            _handle_results(ctx, results, return_code)
        except LinchpinError as e:
            ctx.log_state(e)
            sys.exit(1)
    else:  # if tx_id is not passed, use run_id as a baseline
        if (not len(targets) or len(targets) > 1) and run_id:
            raise click.UsageError("A single target is required when calling"
                                   " destroy with `--run_id` option")
        try:
            return_code, results = lpcli.lp_destroy(targets=targets,
                                                    run_id=run_id,
                                                    tx_id=tx_id)
            _handle_results(ctx, results, return_code)
        except LinchpinError as e:
            ctx.log_state(e)
            sys.exit(1)


@runcli.command()
@click.argument('remote', default=None, required=True, nargs=1)
@click.option('-t', '--type', 'fetch_type', metavar='TYPE', required=False,
              default='workspace', help='Which component of a workspace to'
              ' fetch. (Default: workspace)')
@click.option('-r', '--root', metavar='ROOT', default='',
              help='Use this to specify the location of the workspace'
                   ' within the root url. If root is not set, the root'
                   ' of the given remote will be used.')
@click.option('--dest', 'dest_ws', metavar='DEST', default=None,
              help='Workspaces destination, the fetched workspace will be'
                   ' relative to this location. (Overrides -w/--workspace)')
@click.option('--branch', 'fetch_ref', metavar='REF', default=None,
              help='Specify the git branch. Used only with'
                   ' git protocol (eg. master).')
@click.option('--git', 'fetch_protocol', flag_value='FetchGit', default=True,
              help='Remote is a git repository (default)')
@click.option('--web', 'fetch_protocol', flag_value='FetchHttp',
              help='Remote is a web directory')
@click.option('--nocache', is_flag=True,
              help='Do not check the cached time, just copy the data to the'
                   ' destination')
@pass_context
def fetch(ctx, remote, fetch_type, root, dest_ws,
          fetch_ref, fetch_protocol, nocache):
    """
    Fetches a specified linchpin workspace or component from a remote location

    """

    if not fetch_type:
        fetch_type = 'workspace'

    try:
        lpcli.lp_fetch(remote, root=root, fetch_type=fetch_type,
                       fetch_protocol=fetch_protocol, fetch_ref=fetch_ref,
                       dest_ws=dest_ws, nocache=nocache)
    except LinchpinError as e:
        ctx.log_state(e)
        sys.exit(1)


@runcli.command()
@click.argument('targets', metavar='TARGETS',
                required=False, default=None, nargs=-1)
@click.option('--view', metavar='VIEW', default='target', required=False,
              help='Type of view display (default: target)')
@click.option('-c', '--count', metavar='COUNT', default=3, required=False,
              help='(up to) number of records to return (default: 3)')
@click.option('-f', '--fields', metavar='FIELDS', required=False,
              help='List the fields to display')
@click.option('-t', '--tx-id', multiple=True, type=int,
              metavar='TX_ID', required=False,
              help="Display a specific transaction by ID (tx_id)."
                   " Only works with '--view=tx'")
@click.option('--output-format', type=str, default="cfg",
              metavar='output_format', required=False,
              help="Inventory output format")
@click.option('--output-type', type=str,
              metavar='output_type', required=False,
              help="default inventory")
@click.option('--target', metavar='target', default="all",
              help='If multiple targets are mentioned \
                    takes parameter for target to be used.\
                    By default all are displayed\
                    displayed')
@pass_context
def journal(ctx, targets, fields, count, view,
            tx_id, output_format, output_type, target):
    """
    Display information stored in Run Database

    view:       How the journal is displayed

                'target': show results of transactions on listed targets
                (or all if omitted)

                'tx': show results of each transaction, with results
                of associated targets used

    (Default: target)

    count:      Number of records to show per target

    targets:    Display data for the listed target(s). If omitted, the latest
                records for any/all targets in the RunDB will be displayed.

    fields:     Comma separated list of fields to show in the display. Used
    only with `--view=target`.
    (Default: action, uhash, rc. Additional fields: start, end)
    """

    if output_type == "inventory":
        inventories = lpcli._write_to_inventory(inv_path=ctx.outfile,
                                                inv_format=output_format)
        if target == "all":
            click.echo("By default all targets inventories are displayed to stdout\
                        For specific target please use --target option")
            for target in inventories:
                click.echo(inventories[target])
        else:
            try:
                click.echo(inventories[target])
            except IndexError as e:
                click.echo("Invalid target")
                click.echo(e.message)
        return inventories

    if view == 'target':

        try:
            journal = lpcli.lp_journal(view=view, targets=targets,
                                       fields=fields, count=count)
        except LinchpinError as e:
            ctx.log_state(e)
            sys.exit(1)

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


        if len(journal):
            for target, values in journal.iteritems():
                keys = values.keys()

                if len(keys):
                    print('\nTarget: {0}'.format(target), file=sys.stderr)
                    print(output, file=sys.stderr)
                    keys.sort(reverse=True)
                    for run_id in keys:
                        if int(run_id) > 0:
                            out = '{0:<7}\t'.format(run_id)
                            for f in fields:
                                out += '{0:>9}\t'.format(values[run_id][f])

                            print(out, file=sys.stderr)
                else:
                    no_records.append(target)


            if no_records:
                no_out = '\nNo records for targets:'

                for rec in no_records:
                    no_out += ' {0}'.format(rec)

                print(no_out, file=sys.stderr)

        else:
            print('No targets available for journal.'
                  ' Please provision something. :)', file=sys.stderr)
        print('\n')
        ctx.log_state(output)

    elif view == 'tx':

        try:
            j = lpcli.lp_journal(view=view, count=count, tx_ids=tx_id)
            if not len(tx_id):
                journal = OrderedDict(reversed(sorted(j.items())))
            else:
                journal = OrderedDict(j.items())
        except LinchpinError as e:
            ctx.log_state(e)
            sys.exit(1)

        output = ''

        if len(journal):
            for lp_id, v in journal.iteritems():

                if v:
                    output += '\nID: {0}\t\t\t'.format(lp_id)
                    output += 'Action: {0}\n'.format(v['action'])
                    output += '\n{0:<20}\t{1:>6}'.format('Target', 'Run ID')
                    output += '\t{0:<5}\t{1:<10}\n'.format('uHash', 'Exit Code')
                    output += '----------------------------------------------'
                    output += '---\n'

                    for targets in v['targets']:
                        for target, values in targets.iteritems():
                            for rundb_id, data in values.iteritems():
                                output += '{0:<20}\t{1:>6}\t'.format(target,
                                                                     rundb_id)
                                output += '{0:>5}'.format(data['uhash'])
                                output += '\t{0:>9}\n'.format(data['rc'])

                    output += '\n======================================='
                    output += '==========\n'

        else:
                output += '\n==================NO TRANSACTIONS======'
                output += '==========\n'

        ctx.log_state(output)


@runcli.command()
@click.option('--old-schema', '-o', is_flag=True)
@click.argument('targets', metavar='TARGETS', required=False,
                nargs=-1)
@pass_context
def validate(ctx, targets, old_schema):
    """
    Validate topologies for the given target(s) in the given PinFile.

    The data from the targets is obtained from the PinFile (default).

    targets:    Validate ONLY the listed target(s). If omitted, ALL targets in
    the appropriate PinFile will be validate

    """

    try:
        old_schema = False
        return_code, results = lpcli.lp_validate(targets=targets,
                                                 old_schema=old_schema)
        for target, item in results.iteritems():
            result = ""
            for kind, outcome in item.iteritems():
                if outcome == "valid" or outcome == "valid under old schema":
                    result += "[SUCCESS] {0} for target '{1}' is "\
                        "{2}\n".format(kind, target, outcome)
                else:
                    result += "[ERROR] {0} for target '{1}' does not "\
                              "validate\n{2}".format(kind, target, outcome)
            ctx.log_state(result)

        if old_schema:
            warning = """
Topologies valid under the old schema may have older directives.
It is suggested to update any of the following:
    res_group_type -> resource_group_type
    res_defs -> resource_definitions
    res_name -> name
    type -> role
    res_type -> role"""
            ctx.log_state(warning)
        sys.exit(return_code)
    except LinchpinError as e:
        ctx.log_state(e)
        sys.exit(1)


@runcli.command()
@click.argument('providers', metavar='PROVIDERS', required=False,
                nargs=-1)
@click.option('--ask-sudo-pass', is_flag=True, default=False,
              help='Prompts for sudo password for package installations')
@pass_context
def setup(ctx, providers, ask_sudo_pass):
    """
    Install the dependencies needed for the given provider(s).

    providers:    Setup ONLY the providers listed. If omitted, it installs
    the dependencies for ALL providers.
    """
    lpcli.ctx.set_evar("ask_sudo_pass", ask_sudo_pass)
    return_code, output = lpcli.lp_setup(providers)
    return sys.exit(return_code)


def main():
    # print("entrypoint")
    pass
