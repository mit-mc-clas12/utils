#!/bin/bash


if [ `uname` == "Darwin" ]; then
	domainName=`hostname -f | sed -e 's/^[^.]*.//'`
else
	domainName=`hostname -d`
fi

echo $domainName
