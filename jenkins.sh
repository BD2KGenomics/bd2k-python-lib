virtualenv venv
. venv/bin/activate
make develop
export PYTEST_ADDOPTS="--junitxml=test-report.xml"
make $make_targets

virtualenv -p python3 venv3
. venv3/bin/activate
make python=python3 develop
export PYTEST_ADDOPTS="--junitxml=test-report.xml"
make python=python3 $make_targets
