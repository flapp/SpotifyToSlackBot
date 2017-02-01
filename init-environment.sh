#!/bin/bash
# requires xcode command line tools
# initialise the python virtual environment
#  * install necessary packets inside the virtualenv
#  * set the paths/configurations of the uploader

# make sure we're picking the right directory if we're running from a different directory
echo "** init-environment.sh - bootstrap python virtualenv"
echo "** Calling script: \"$0\""
echo "** This script: \"${BASH_SOURCE[0]}\""
export DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo "** This script dir: \"${DIR}\""

export PYTHON_VIRTUALENV="${DIR}/python-virtualenv"

if [ ! -e "$PYTHON_VIRTUALENV" ]; then

	echo "** virtualenv for ansible not found in $PYTHON_VIRTUALENV, creating..."

	gcc --version 2&>/dev/null
	if [ $? != 0 ]; then
		echo "** Please install OSX Xcode Command Line Tools"
		exit
	fi

	virtualenv --version 2&>/dev/null
	if [ $? != 0 ]; then
		echo "** virtualenv not found, installing."
		echo "** Please provide root password:"
		sudo easy_install virtualenv
		echo "** virtualenv install finished"
	fi

	virtualenv "$PYTHON_VIRTUALENV"
	source "$PYTHON_VIRTUALENV/bin/activate"

	#avoid errors on newer XCode command line tools
	#thanks, http://bruteforce.gr/bypassing-clang-error-unknown-argument.html
	export ARCHFLAGS=-Wno-error=unused-command-line-argument-hard-error-in-future

	#using a frozen pip environment to avoid sneaky updates
	pip install -r pip-reqs.txt
	
	echo "* Pip freeze state:"
	pip freeze
	echo "**"

else
	echo "** virtualenv for ansible found in $PYTHON_VIRTUALENV, activating ..."
	source "$PYTHON_VIRTUALENV/bin/activate"
fi

