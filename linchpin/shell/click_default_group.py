# -*- coding: utf-8 -*-

# """
#    click_default_group
#    ~~~~~~~~~~~~~~~~~~~
#    Define a default subcommand by `default=True`:
#    .. sourcecode:: python
#       import click
#       from click_default_group import DefaultGroup
#       @click.group(cls=DefaultGroup, default_if_no_args=True)
#       def cli():
#           pass
#       @cli.command(default=True)
#       def foo():
#           click.echo('foo')
#       @cli.command()
#       def bar():
#           click.echo('bar')
#    Then you can invoke that without explicit subcommand name:
#    .. sourcecode:: console
#       $ cli.py --help
#       Usage: cli.py [OPTIONS] COMMAND [ARGS]...
#       Options:
#         --help    Show this message and exit.
#       Command:
#         foo*
#         bar
#       $ cli.py
#       foo
#       $ cli.py foo
#       foo
#       $ cli.py bar
#       bar
#
# Credit: Heungsub Lee <https://github.com/sublee>
#
# Copyright (c) 2015-2016, Heungsub Lee
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification,are permitted provided that the following conditions are met:
#
#   Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
#   Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
#   Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# """

import warnings
import click


__all__ = ['DefaultGroup']
__version__ = '1.2'


class DefaultGroup(click.Group):
    """
    Invokes a subcommand marked with `default=True` if any subcommand not
    chosen.

    :param default_if_no_args: resolves to the default command if no arguments
                               passed.
    """

    def __init__(self, *args, **kwargs):
        # To resolve as the default command.
        if not kwargs.get('ignore_unknown_options', True):
            raise ValueError('Default group accepts unknown options')
        self.ignore_unknown_options = True
        self.default_cmd_name = kwargs.pop('default', None)
        self.default_if_no_args = kwargs.pop('default_if_no_args', False)
        super(DefaultGroup, self).__init__(*args, **kwargs)


    def set_default_command(self, command):
        """Sets a command function as the default command."""
        cmd_name = command.name
        self.add_command(command)
        self.default_cmd_name = cmd_name


    def parse_args(self, ctx, args):

        super(DefaultGroup, self).parse_args(ctx, args)

        # modified from original code to allow default help command
        # when parameters are passed in.
        if not len(ctx.protected_args):
            ctx.protected_args.append(self.default_cmd_name)

    def list_commands(self, ctx):
        """
        Provide a list of available commands. Anything deprecated should
        not be listed
        """

        return ['init', 'up', 'destroy', 'fetch', 'journal', 'setup']

    def get_command(self, ctx, cmd_name):

        lp_aliases = {
            'rise': 'up',
            'drop': 'destroy',
            'down': 'destroy',
        }

        cmd = lp_aliases.get(cmd_name, cmd_name)

        if cmd not in self.commands:
            # No command name matched.
            ctx.arg0 = cmd
            cmd = self.default_cmd_name
        return super(DefaultGroup, self).get_command(ctx, cmd)


    def resolve_command(self, ctx, args):
        base = super(DefaultGroup, self)
        cmd_name, cmd, args = base.resolve_command(ctx, args)
        if hasattr(ctx, 'arg0'):
            args.insert(0, ctx.arg0)
        return cmd_name, cmd, args


    def format_commands(self, ctx, formatter):
        formatter = DefaultCommandFormatter(self, formatter, mark='*')
        return super(DefaultGroup, self).format_commands(ctx, formatter)


    def command(self, *args, **kwargs):
        default = kwargs.pop('default', False)
        decorator = super(DefaultGroup, self).command(*args, **kwargs)
        if not default:
            return decorator
        warnings.warn('Use default param of DefaultGroup or '
                      'set_default_command() instead', DeprecationWarning)


        def _decorator(f):
            cmd = decorator(f)
            self.set_default_command(cmd)
            return cmd
        return _decorator


class DefaultCommandFormatter(object):
    """Wraps a formatter to mark a default command."""


    def __init__(self, group, formatter, mark='*'):
        self.group = group
        self.formatter = formatter
        self.mark = mark


    def __getattr__(self, attr):
        return getattr(self.formatter, attr)


    def write_dl(self, rows, *args, **kwargs):
        rows_ = []
        for cmd_name, help in rows:
            if cmd_name == self.group.default_cmd_name:
                rows_.insert(0, (cmd_name + self.mark, help))
            else:
                rows_.append((cmd_name, help))
        return self.formatter.write_dl(rows_, *args, **kwargs)
