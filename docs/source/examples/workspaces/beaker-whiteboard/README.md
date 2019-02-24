# Beaker setting whiteboard

Deployment of a single instance in Beaker with minimal set of settings, and
overwriting job whiteboard. Whiteboard is used for additional information for
the user, such as Jenkins build URL.
The example is [configurable] using the following arguments:

 - `beaker_windows_distro` - [Beaker distro], default 'RHEL-6.5'.
 - `beaker_windows_arch` - operating system [ISA], default 'x86_64'
 - `beaker_windows_name` - instance name
 - `beaker_windows_whiteboard` - whiteboard content

To run with different configuration, you add `--template-data` option with path
to file or inline, for example:

    linchpin --template-data "{ \"beaker_whiteboard_whiteboard\": \"$BUILD_URL\" }" up

From file:

    linchpin --template-data '@settings.json' up

Short version:

    linchpin -d '@settings.json' up

[configurable]: https://linchpin.readthedocs.io/en/latest/managing_resources.html
[Beaker distro]: https://beaker-project.org/docs/user-guide/distros.html
[ISA]: https://en.wikipedia.org/wiki/Instruction_set_architecture
