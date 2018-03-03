#!/bin/bash
# Base Script File (demo.sh)

cd cityback
#reset the DB
./reset_db.sh

# start all the servers in dev mode
./start_dev.sh
