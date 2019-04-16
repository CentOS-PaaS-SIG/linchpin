# AWS simple EC2 deployment

Deployment of a single instance in AWS EC2 with minimal set of settings.
The example is [configurable] using the following arguments:

 - `aws_simple_flavor` - [EC2 flavor], default 't2.nano'
 - `aws_simple_region` - [EC2 region], default 'us-east-1'
 - `aws_simple_image` - [EC2 image], default 'ami-9887c6e7' which is [CentOS 7]
 - `aws_simple_security` - [EC2 security groups], default is 'default'
 - `aws_simple_public` - Should Linchpin assign public IP to the instance,
   default is  'false'
 - `aws_simple_keypair` - [EC2 keypair] to deploy into the system, has to be
   done before instance deployment, default 'ec2_keypair'
 - `aws_simple_keypath` - Location of private key, default '~/.ssh/id_rsa'

To run with different configuration, you add `--template-data` option with path
to file or inline, for example:

    linchpin --template-data '{ "aws_simple_flavor": "t2.micro" }' up

From file:

    linchpin --template-data '@settings.json' up

Short version:

    linchpin -d '@settings.json' up

[configurable]: https://linchpin.readthedocs.io/en/latest/managing_resources.html
[EC2 flavor]: https://aws.amazon.com/ec2/instance-types/
[EC2 region]: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html
[EC2 image]: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AMIs.html
[CentOS 7]: https://wiki.centos.org/Cloud/AWS#head-cc841c2a7d874025ae24d427776e05c7447024b2
[EC2 security groups]: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-network-security.html
[EC2 keypair]: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html

