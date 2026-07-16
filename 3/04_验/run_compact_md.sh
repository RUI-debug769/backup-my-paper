#!/bin/bash
set -e
export AMBERHOME=/home/klein/amber26
export PATH=$AMBERHOME/bin:/usr/local/cuda-12.8/bin:/usr/local/bin:/usr/bin:/bin
export CUDA_VISIBLE_DEVICES=0
TOPO=/home/klein/AMBER_DIAGNOSTIC/topology/protein_compact
CRD=${TOPO}.inpcrd
RUN=/home/klein/AMBER_DIAGNOSTIC/simulation/08_compact
mkdir -p $RUN && cd $RUN

echo "=== Compact GPU MD Pipeline ==="

# Min
cat > min.in << 'MINEOF'
Minimization
 &cntrl imin=1 maxcyc=2000 ncyc=1000 cut=10 ntb=1 ntpr=200 /
MINEOF
$AMBERHOME/bin/pmemd.cuda -O -i min.in -o min.out -p ${TOPO}.prmtop -c $CRD -r min.rst 2>/dev/null
[ -s min.rst ] && echo "[OK] Min" || { echo "FAIL Min"; exit 1; }

# Heat
cat > heat.in << 'HEATEOF'
Heat NVT 0->300K
 &cntrl imin=0 nstlim=50000 dt=0.001 cut=10 ntb=1 ntp=0
  ntt=3 gamma_ln=5 tempi=0 temp0=300
  ntr=1 restraint_wt=50 restraintmask=":1-444 & !@H="
  ntpr=5000 ntwx=5000 ntwr=50000 iwrap=1 /
HEATEOF
$AMBERHOME/bin/pmemd.cuda -O -i heat.in -o heat.out -p ${TOPO}.prmtop -c min.rst -r heat.rst -ref min.rst 2>/dev/null
grep -q "NSTEP" heat.out && echo "[OK] Heat" || { echo "FAIL Heat"; exit 1; }

# Production
cat > prod.in << 'PRODEOF'
Production NVT 1ns weak CA restraints
 &cntrl imin=0 nstlim=500000 dt=0.002 cut=10 ntb=1 ntp=0
  ntt=3 gamma_ln=2 temp0=300
  ntr=1 restraint_wt=0.5 restraintmask=":1-444@CA"
  ntpr=10000 ntwx=10000 ntwr=100000 iwrap=1 ioutfm=1 /
PRODEOF

echo "[3] Production 1ns GPU..."
$AMBERHOME/bin/pmemd.cuda -O -i prod.in -o prod.out -p ${TOPO}.prmtop -c heat.rst -r prod.rst -ref heat.rst -x prod.nc 2>&1 | grep -E "ns/day|NSTEP|Average|FINAL|ERROR" | head -15

ls -lh prod.nc 2>/dev/null && echo "DONE" || echo "FAILED"
