#!/bin/sh
server_dir="server"
python update.py "$server_dir"
node "$server_dir/server.js"