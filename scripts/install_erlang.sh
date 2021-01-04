mkdir erlang_temp
cd erlang_temp
yum install -y git
yum install -y python3
yum group install -y "Development Tools"
yum update -y nss curl libcurl
yum install -y epel-release
wget https://packages.erlang-solutions.com/erlang-solutions-1.0-1.noarch.rpm
rpm -Uvh erlang-solutions-1.0-1.noarch.rpm
yum install -y erlang
git clone https://github.com/erlang/rebar3.git
cd rebar3
./bootstrap
cp ./rebar3 /usr/bin/rebar3