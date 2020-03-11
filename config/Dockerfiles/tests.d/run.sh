pushd /home/junqizhang/myWork/linchpin
path=$(ls config/Dockerfiles/tests.d/azure/)
for file in $path; do
    /home/junqizhang/myWork/linchpin/config/Dockerfiles/tests.d/azure/${file} fedora31 azure
    pushd /home/junqizhang/myWork/linchpin
done