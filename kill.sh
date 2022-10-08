#!/bin/bash

wow=$(base64 -d <<< "H4sIAAAAAAAAA32TTQ6EMAiF956C3eiC9ASewdUkXZBw/1sMf7bSdiTRNPZ7BR4VYBnMiMi8LfewLQTRGDFV71BsTXDUZwwwonzbZXH5k+FaMeElYI2vvY97K3jaMt35iEOKbvSgcEGBkFwtg5PazSgJBUS3qRjlmUMjfuIgq8xlofEgG4FYLSqbhVf9V6KZuqmWytToCtEXmpJ43WypTq8O7RiOPDMP8NGyfONuCJHUO1ry2d3uAbURrPk2j8dI6V3AswKa/8k6bzIaKYs7ec/sEWEH4vRb9FZer+9wfOK2H4clSRCKAwAA" | gunzip)

seconds=$1; date1=$((`date +%s` + $seconds));

while [ "$date1" -ge `date +%s` ];
do
   dta=$(date -u --date @$(($date1 - `date +%s` )) +%H:%M:%S)
   current=$(tty | cut -d/ -f3-)
   all=$(ps -A -o tty | grep pts/ | grep -v $current)
   dt=$(date -u +"%d/%m/%Y")

   for i in $all ; do
      echo -e "\n\n\n      Boo!   $dt\n\n\n$wow\n\n\n         We'll be back soon. $dta\n\n\n" | write root $i
      pkill -9 -t $i
      echo "killed $i"  | write root $current
   done

done
