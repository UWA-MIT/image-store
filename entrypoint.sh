#!/bin/bash

# Start the long-running command
top -b

# Keep the container running
tail -f /dev/null