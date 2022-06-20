#!/bin/bash
set -x
sleep 5
CMD=$1
GENIP=$2
PASSCODE=$3
if test -n "$GENIP"
then
while true
do
    curl $GENIP:8321/p2pid
    retVal=$?
    if [ $retVal -ne 0 ]; then
        sleep 1
    else
        break
    fi
done
fi
TSSPEER=$(curl $GENIP:8321/p2pid)

echo "AAAAAAAAAAAAAAAAAAAAAAAA"
echo $TSSPEER
echo "AAAAAAAAAAAAAAAAAAAAAAAA"
if [ -z "$TSSPEER" ]
then
      echo PASSCODE | $CMD -home /root/.oppyChain/config -key  operator.key
else
      echo PASSCODE| $CMD -home /root/.oppyChain/config -key operator.key -peer /ip4/$GENIP/tcp/6668/p2p/$TSSPEER
fi
