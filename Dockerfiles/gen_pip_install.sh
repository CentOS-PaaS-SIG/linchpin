#!/bin/bash

echo "#!/bin/bash -ex" > pip_install.sh
for line in $(cat ../requirements.txt)
do
  echo "pip install $line" >> pip_install.sh
done
chmod 755 pip_install.sh
