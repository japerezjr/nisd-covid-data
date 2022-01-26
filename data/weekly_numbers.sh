#!/usr/bin/bash
WEEKS=''
for i in `md5sum nisd_numbers.202* | sort -u -k1,1 | sort -k2 | awk '{ print $2}'`
do
   WEEKS+="$i "
done

#WEEKS='nisd_numbers.20210921184502.log '
#WEEKS+='nisd_numbers.20210922230002.log '
#WEEKS+='nisd_numbers.20210929230002.log '
#WEEKS+='nisd_numbers.20211006230001.log '
#WEEKS+='nisd_numbers.20211013230001.log '
#WEEKS+='nisd_numbers.20211020230002.log '
#WEEKS+='nisd_numbers.20211027230005.log '
#WEEKS+='nisd_numbers.20211103230003.log '
#WEEKS+='nisd_numbers.20211110230001.log'

echo "NISD Total:"
for WEEK in $WEEKS
do
    echo $WEEK
    head -n1 $WEEK
#    awk 'NR > 1 { print }' $WEEK | jq '. | to_entries | .[] | select(.key == "Beard ES")'
done
echo "BEARD:"
for WEEK in $WEEKS
do
    awk 'NR > 1 { print }' $WEEK | jq '. | to_entries | .[] | select(.key == "Beard ES")'
done
