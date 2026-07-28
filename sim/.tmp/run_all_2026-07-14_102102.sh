#!/bin/bash
NGSPICE=/home/bthomas3/Videos/ngspice_pdk/install/bin/ngspice
SIMDIR=/home/bthomas3/Videos/77GHz_phased_array/sim
LOGDIR=${SIMDIR}/.tmp

SIMS=(
  vco_hbt_typ_m40
  vco_hbt_typ_27
  vco_hbt_typ_125
  vco_hbt_bcs_m40
  vco_hbt_bcs_27
  vco_hbt_bcs_125
  vco_hbt_wcs_m40
  vco_hbt_wcs_27
  vco_hbt_wcs_125
)

pids=()
for f in "${SIMS[@]}"; do
  echo "Launching: $f"
  $NGSPICE -b ${SIMDIR}/${f}.spice > ${LOGDIR}/${f}.log 2>&1 &
  pids+=($!)
done

echo "Waiting for all ${#pids[@]} simulations..."
for pid in "${pids[@]}"; do
  wait $pid
  echo "PID $pid done"
done
echo "All simulations complete."
