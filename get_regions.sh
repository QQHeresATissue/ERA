#!/bin/bash -x
IFS='	
'

if [ -z "$1" ]; then
  echo "Usage: $0 <Region>"
  exit 1
fi

echo "Getting system list for ${1}"
wget -4 -q -O- http://evemaps.dotlan.net/region/${1} | grep -e '/map/'${1} | cut -d '/' -f 4 | cut -d '"' -f 1 | sort -u > ${1}_sys

if [ ! -d "tmp" ]; then
  mkdir ./tmp
fi

for i in `cat ${1}_sys`; do
  echo "Parsing ${1}/${i}"
  wget -4 -O- http://evemaps.dotlan.net/range/1/${i} | grep '/map' | cut -d ':' -f 2 | cut -d '"' -f 1 | sort -u | grep , | sed -e 's/,/","/g' | sed 's/^/["/;s/$/"]/' > ./tmp/${i}.json
done;

find ./ -size 0 -print0 | xargs -0 rm
rm ${1}_sys

echo "[" > ${1}.json
for i in `ls ./tmp`; do

  for s in `cat ./tmp/${i}`; do

    echo "	{ \"name\": \"${i}\", \"connections\": ${s} }," >> ${1}.json

  done

done
sed -i '$s/..$//' ${1}.json
echo "]" >> ${1}.json

#rm -r tmp/*
