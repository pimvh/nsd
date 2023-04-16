#!/bin/sh

# Deal with MacOS
if [[ `uname` == "Darwin" ]]; then
  date_command="gdate"
else
  date_command="date"
fi

# find today
today=$($date_command +%Y%m%d)

# find the epoc from midnight
epoch_midnight=$($date_command --date=$today +%s)

# get current time offset in seconds
time_now=$($date_command +%s)

# caculate second offset from midnight
num_secs=$((x=$time_now, y=$epoch_midnight, x - y ))

# calculate the day offset
day_incr=$((x=$num_secs, x * 99 / 86400))

# make a nice serial
dns_serial=$today$day_incr

echo $dns_serial
