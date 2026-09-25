#!/bin/bash

if [ "$1" == "" ]; then
	echo "no theme name given"
	exit 1
fi

if [ "$(whoami)" != "root" ]; then
	echo "not root"
	exit 1
fi

cp -r usr/share/themes/"$1" /usr/share/themes/