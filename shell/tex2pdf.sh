#!/bin/bash
#--------------------------------------------------------
# Generating pdf from latex source file using xelatex.
#
#
# Author: Kai Yuan   2010.09.11
#--------------------------------------------------------
KEEPALL=0
DIR=$(pwd)
TEXFILE= 

checkInputPara(){
    if [ ! -f $1 ]; then
        echo "ERROR: cannot find input file $1, exiting."
        exit 1
    else
        TEXFILE=$1
    fi
}

if [ $# == 0 ]; then
    echo -e "
        ky_tex script generates pdf from latex source file using xelatex.
        Usage: $0 [Option] <latex source file> 

        Option:
            -a  keep all generated files (including .aux .log .out). without this
                option only pdf file will be generated.
               
    "
    exit 2
fi

if [ $# == 1 ]; then #only one argument, should be the input file
    checkInputPara $1
fi

if [ $# == 2 ]; then #with -a option
    if [ "$1" == "-a" ]; then 
        KEEPALL=1 
    else
        echo "ERROR: unknown option $1"
        exit 1
    fi
    checkInputPara $2 
fi


xelatex $TEXFILE 


bname=$(basename $TEXFILE)
rootname=$(echo ${bname%%.*})

if [ $KEEPALL == 0 ]; then
    #removing generated files other than pdf
    mv $DIR/$rootname.aux /tmp > /dev/null 2>&1
    mv $DIR/$rootname.log /tmp > /dev/null 2>&1
    mv $DIR/$rootname.out /tmp > /dev/null 2>&1
    
fi

echo "==============================================="
echo "INFO: $rootname.pdf was generated to $DIR."
echo "==============================================="


