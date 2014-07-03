#!/bin/bash
command -v python && \
command -v fio || \
{ echo >&2 "One or more dependencies are not installed. Aborting."; exit 1; }
echo "Looks like all dependencies are met. You should be good to go."
exit 0;
