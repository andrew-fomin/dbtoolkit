#!/bin/bash

while getopts m:r:d:u:p:c:h option
do
case "${option}"
in
m) MODE=${OPTARG};;
r) RELEASE=${OPTARG};;
d) DB=${OPTARG};;
u) DBUSER=${OPTARG};;
p) DBPASS=${OPTARG};;
c) PFILE=${OPTARG};;
h) HELP="true"
esac
done

if [ -n "$HELP" ]; 
then
 echo "DB toolkit"
 echo
 echo "./release_manage.sh mode -m apply|revert -r release -u username -p password -d tnsname|ezconnect" 
 echo "-m: apply mode. apply - apply release. revert - revert release"
 echo "-r: release id. '-r 000011'"
 echo "-d: db connection string. default no string (local db)"
 echo "-u: db username."
 echo "-p: db password"
 echo "-c: db.properties pathname" 
 echo
fi


#echo "params:" $1 $MODE $RELEASE $DB $DBUSER $DBPASS $HELP

START_RELEASE=$(echo $RELEASE | awk 'BEGIN {FS=":"}{print $1}')
#END_RELEASE=$(echo $RELEASE | awk 'BEGIN {FS=":"}{print $2}')

#echo $START_RELEASE
#echo $END_RELEASE

if [ -z "$START_RELEASE" ]; then
  echo "No release to apply/revert is specified. Terminating."
  echo
  exit -1
fi

#if [ -z "$END_RELEASE" ]; then
#  END_RELEASE=$START_RELEASE
#fi

echo "Going to $MODE release $START_RELEASE"
echo 

if [ ! -z "$PFILE" ]; then
 echo "Using $PFILE properties file. -u/-p/-d keys values are ignored."
 echo
 source "$PFILE"
else
 echo "No db.properties file is specified. Using -u/-p/-d values."
fi

if [ -z $DBUSER ]; then
  echo "No database credentials were provided. Terminating."
  exit -1
fi



#todo: properly check sqlpus is avaialble. This construction doesn't work well
SQLP=$(which sqlplus 2>>/dev/null)

if [ -x "$SQLP" ]; then
 echo "sqlplus found. Proceeding..."
 echo
else
 echo "sqlplus not found. Terminating"
 echo
 exit -1
fi

SQLP="${SQLP} -L"


if [ "$MODE" = "apply" ]; then
    echo "Applying release: $START_RELEASE"

    $SQLP $DBUSER/$DBPASS@$DB @apply-release-$START_RELEASE.sql |tee -a  apply.out

    echo "Release $START_RELEASE applied"
fi

if [ "$MODE" = "revert" ]; then
    echo "Reverting release $START_RELEASE"

    $SQLP $DBUSER/$DBPASS@$DB @revert-release-$START_RELEASE.sql |tee -a revert.out
    
    echo "Release $START_RELEASE applied"
fi
