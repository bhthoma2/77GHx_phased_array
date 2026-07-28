#!/bin/bash
LOGDIR=/home/bthomas3/Videos/77GHz_phased_array/sim/.tmp

printf "%-20s  %-6s  %-14s  %-12s\n" "Corner" "Temp" "Freq (GHz)" "Swing (Vpp)"
printf "%-20s  %-6s  %-14s  %-12s\n" "------" "----" "----------" "-----------"

for f in \
  "vco_hbt_typ_m40 hbt_typ -40" \
  "vco_hbt_typ_27  hbt_typ 27" \
  "vco_hbt_typ_125 hbt_typ 125" \
  "vco_hbt_bcs_m40 hbt_bcs -40" \
  "vco_hbt_bcs_27  hbt_bcs 27" \
  "vco_hbt_bcs_125 hbt_bcs 125" \
  "vco_hbt_wcs_m40 hbt_wcs -40" \
  "vco_hbt_wcs_27  hbt_wcs 27" \
  "vco_hbt_wcs_125 hbt_wcs 125"; do
  logfile=$(echo $f | awk '{print $1}')
  corner=$(echo $f | awk '{print $2}')
  temp=$(echo $f | awk '{print $3}')

  fosc_raw=$(grep "^fosc" ${LOGDIR}/${logfile}.log 2>/dev/null | awk '{print $3}')
  swing_raw=$(grep "^vosc_pp" ${LOGDIR}/${logfile}.log 2>/dev/null | awk '{print $3}')

  if [ -z "$fosc_raw" ]; then
    fosc_ghz="FAILED"
  else
    fosc_ghz=$(awk "BEGIN {printf \"%.3f\", $fosc_raw / 1e9}")
  fi

  if [ -z "$swing_raw" ]; then
    swing_v="FAILED"
  else
    swing_v=$(awk "BEGIN {printf \"%.4f\", $swing_raw}")
  fi

  printf "%-20s  %-6s  %-14s  %-12s\n" "$corner" "$temp" "$fosc_ghz" "$swing_v"
done
