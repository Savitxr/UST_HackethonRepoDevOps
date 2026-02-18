#!/bin/bash

OUT="snapshot_$(date +%F_%H-%M-%S).txt"

{
echo "DATE"
date

echo "INSTALLED PACKAGES"
dpkg -l 2>/dev/null || rpm -qa

echo " ENVIRONMENT VARIABLES "
printenv | sort

echo "ACTIVE USERS"
who
} > "$OUT"

echo "Snapshot saved to $OUT"