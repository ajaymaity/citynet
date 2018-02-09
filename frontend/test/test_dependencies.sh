#!/bin/bash

# Base Script File (test/test_dependencies.sh)
# Created: Wed 31 Jan 2018 18:25:04 GMT
# Version: 1.0
#
# This Bash script was developped by Cory.
#
# (c) Corentin Chéron <chronc@tcd.ie> 

error() {
   echo "ERROR in dependencies TEST on line $1 !!!!!!"
   exit -1
  }
trap 'error $LINENO' ERR


set -e
# mapbox
[ "`npm list 2>/dev/null | grep "mapbox-gl" | head -1 | cut -d'@' -f 2`" == "0.44.0" ]
# eslint
[ "`npm  list 2>/dev/null | grep "eslint" | head -1 | cut -d'@' -f 2`" == "4.16.0" ]


echo "All tests Succeeded!"
