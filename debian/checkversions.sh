#!/bin/bash
set -e

cd src
pymodver=$(python -c 'import graphiteudp; print graphiteudp.__version__')
cd - >> /dev/null

packagever=$(head -1 debian/changelog | sed 's/[a-zA-Z0-9-]\+ (\([0-9.]\+\)).*/\1/g')

if [ "$pymodver" != "$packagever" ]
then
	echo "Version mismatch between debian/changelog ($packagever) and src/graphiteudp.py ($pymodver)"
	exit 1
fi


