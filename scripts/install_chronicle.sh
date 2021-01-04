mkdir compiled_chronicle
cd compiled_chronicle
git clone https://github.com/couchbase/chronicle.git
cd chronicle
sed -i 's/git@github.com:davisp\/jiffy.git/https:\/\/github.com\/davisp\/jiffy.git/' ./examples/chronicled/rebar.config
rebar3 as examples compile