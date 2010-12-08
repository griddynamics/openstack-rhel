#!/bin/sh

ip addr show dev $1|grep 'inet '|perl -pi -e 's/^.*inet ([0-9\.]+).*$/$1/'
