# python.chronicle

A Python repository to test/experiment-with Chronicle on a small scale

### Requirements
A centos7 vagrant machine up and running

A system with python2(with libraries from requirements.txt installed) 
from where you will be running this repo.

### Getting Started
Once you have the centos7 vagrant machine up, copy the scripts "install_erlang.sh" 
and "install_chronicle.sh" to the root folder of the VM ie; '/install_erlang.sh' ,
'/install_chronicle.sh' 

 Run them one by one:
```
bash install_erlang.sh
```
```
bash install_chronicle.sh
```

The first command installs the dependencies (rebar3 and other libraries) required
for running Chronicle. 
The second command downloads chronicle repo and compiles the examples and stores it
at path '/compiled_chronicle' on the VM.


You can then run the SimpleTests module on your system:
```
python runner.py -n 10.112.200.101 -u username -p password -t SimpleTests
```
(Give the appropriate IP, username, password of your VM)