#!/bin/bash

while getopts m:r:d:u:p:h option
do
case "${option}"
in
m) MODE=${OPTARG};;
r) RELEASE=${OPTARG};;
d) DB=${OPTARG};;
u) DBUSER=${OPTARG};;
p) DBPASS=${OPTARG};;
h) HELP="true"
esac
done

if [ -n "$HELP" ];
then
 echo "Rittman Mead Database Release Deployment Script"
 echo
 echo "./release_manage.sh mode -m apply|revert -r release -u username -p password -d tnsname"
 echo
 echo "-m: apply mode. 'apply' - apply release to a DB. 'revert' - rollback release"
 echo "-r: release id. '-r 11' for a single release or '-r 5:11' for a range of releases. Revert is done in backwards order"
 echo "-d: db connection string. Default no string (local db)"
 echo "-u: db username."
 echo "-p: db password"
 echo
fi


#echo "params:" $1 $MODE $RELEASE $DB $DBUSER $DBPASS $HELP

START_RELEASE=$(echo $RELEASE | awk 'BEGIN {FS=":"}{print $1}')
END_RELEASE=$(echo $RELEASE | awk 'BEGIN {FS=":"}{print $2}')

#echo $START_RELEASE
#echo $END_RELEASE

if [ -z "$END_RELEASE" ]; then
  END_RELEASE=$START_RELEASE
fi

if [ -z "$START_RELEASE" ]; then
  echo "No release to apply/revert is specified. -r should point to a single release or a range. Terminating."
  echo
  exit -1
fi

echo "Going to $MODE releases from $START_RELEASE to $END_RELEASE"
echo


#todo: properly check sqlpus is avaialble. This construction works, but doesn't look good
SQLP=$(which sqlplus 2>>/dev/null)
if [ -x "$SQLP" ]; then
 echo "sqlplus found. Proceeding..."
 echo
else
 echo "sqlplus not found. Check that ORACLE_HOME and path variables are set properly. Terminating."
 echo
 exit -1
fi


if [ "$MODE" = "apply" ]; then
  for i in $(seq -f "release-r%06g" $START_RELEASE $END_RELEASE)
  do
    echo "Applying release folder: $i"

    pushd $i >> apply.out
    $SQLP $DBUSER/$DBPASS@$DB @apply-release.sql >> apply.out
    popd >> apply.out

    echo "Release folder $i applied"
  done
fi

if [ "$MODE" = "revert" ]; then
for i in $(seq -f "release-r%06g" $END_RELEASE -1 $START_RELEASE )
  do
    echo "Reverting release folder: $i"

    pushd $i >> revert.out
    $SQLP $DBUSER/$DBPASS@$DB @revert-release.sql >> revert.out
    popd >> revert.out

    echo "Release folder $i applied"
  done
fi