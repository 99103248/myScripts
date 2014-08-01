#!/bin/bash
#########################################
# Matrix transpose with Awk
#
# Kai Yuan
# kent.yuan at gmail dot com
#
# 2011-07-07
#
#########################################
fs=${2:-" "}
file=$1

awk  -v FS="$fs" '{for (i=1;i<=NF;i++) a[i,NR]=$i; }END{
    for(i=1;i<=NF;i++) {
        for(j=1;j<=NR;j++)
			printf "%s%s", a[i,j], (j==NR? ORS:OFS);
    } 
}' "$file"
