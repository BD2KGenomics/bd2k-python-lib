# Copyright (C) 2015 UCSC Computational Genomics Lab
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

define help

Supported targets: 'develop', 'sdist', 'clean', 'test', 'pypi', or 'pypi_stable'.

The 'develop' target creates an editable install (aka develop mode).

The 'sdist' target creates a source distribution of this project.

The 'clean' target undoes the effect of 'develop' and 'sdist'.

The 'test' target runs unit tests. Set the 'tests' variable to run a particular test.

The 'pypi' target publishes the current commit of this project to PyPI after enforcing that the
working copy and the index are clean, and tagging it as an unstable .dev build.

The 'pypi_stable' target is like 'pypi' except that it doesn't tag the build as
an unstable build. IOW, it publishes a stable release.


endef
export help
.PHONY: help
help:
	@echo "$$help"


python=python2.7
tests=src

green=\033[0;32m
normal=\033[0m
red=\033[0;31m


.PHONY: develop
develop: _check_venv
	$(python) setup.py egg_info develop


.PHONY: clean_develop
clean_develop: _check_venv
	- $(python) setup.py develop -u
	- rm -rf src/*.egg-info


.PHONY: sdist
sdist: _check_venv
	$(python) setup.py sdist


.PHONY: clean_sdist
clean_sdist:
	- rm -rf dist


.PHONY: test
test: _check_venv
	$(python) setup.py test --addopts "-vv --assert=plain --continue-on-collection-errors $(tests)"


.PHONY: pypi
pypi: _check_clean_working_copy _check_running_on_jenkins
	@test "$$(git rev-parse --verify remotes/origin/master)" != "$$(git rev-parse --verify HEAD)" \
		&& echo "Not on master branch, silently skipping deployment to PyPI." \
		|| $(python) setup.py egg_info --tag-build=.dev$$BUILD_NUMBER sdist bdist_egg upload


.PHONY: pypi_stable
pypi_stable: _check_clean_working_copy _check_running_on_jenkins
	test "$$(git rev-parse --verify remotes/origin/master)" != "$$(git rev-parse --verify HEAD)" \
		&& echo "Not on master branch, silently skipping deployment to PyPI." \
		|| $(python) setup.py egg_info register sdist bdist_egg upload


.PHONY: clean_pypi
clean_pypi:
	- rm -rf build/


.PHONY: clean
clean: clean_develop clean_sdist clean_pypi
	-rm -rf __pychache__
	-rm -rf .cache .eggs
	find . -name '*.pyc' | xargs rm


.PHONY: _check_venv
_check_venv:
	@$(python) -c 'import sys; sys.exit( int( not hasattr(sys, "real_prefix") ) )' \
		|| ( echo "$(red)A virtualenv must be active.$(normal)" ; false )


.PHONY: _check_clean_working_copy
_check_clean_working_copy:
	@echo "$(green)Checking if your working copy is clean ...$(normal)"
	@git diff --exit-code > /dev/null \
		|| ( echo "$(red)Your working copy looks dirty.$(normal)" ; false )
	@git diff --cached --exit-code > /dev/null \
		|| ( echo "$(red)Your index looks dirty.$(normal)" ; false )
	@test -z "$$(git ls-files --other --exclude-standard --directory)" \
		|| ( echo "$(red)You have are untracked files:$(normal)" \
			; git ls-files --other --exclude-standard --directory \
			; false )


.PHONY: _check_running_on_jenkins
_check_running_on_jenkins:
	@echo "$(green)Checking if running on Jenkins ...$(normal)"
	test -n "$$BUILD_NUMBER" \
		|| ( echo "$(red)This target should only be invoked on Jenkins.$(normal)" ; false )
