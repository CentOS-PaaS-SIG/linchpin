# Beaker simple single instance deployment

Deployment of a single instance in Beaker with minimal set of settings.
The example is [configurable] using the following arguments:

 - `beaker_simple_distro` - [Beaker distro], default 'RHEL-6.5'.
 - `beaker_simple_arch` - operating system [ISA], default 'x86_64'
 - `beaker_simple_name` - instance name

To run with different configuration, you add `--template-data` option with path
to file or inline, for example:

    linchpin --template-data '{ "beaker_simple_name": "my_system" }' up

From file:

    linchpin --template-data '@settings.json' up

Short version:

    linchpin -d '@settings.json' up

[configurable]: https://linchpin.readthedocs.io/en/latest/managing_resources.html
[Beaker distro]: https://beaker-project.org/docs/user-guide/distros.html
[ISA]: https://en.wikipedia.org/wiki/Instruction_set_architecture
