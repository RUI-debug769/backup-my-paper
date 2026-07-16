#!/bin/bash
set -e
export AMBERHOME=/home/klein/amber26
export PATH=$AMBERHOME/bin:/usr/local/cuda-12.8/bin:/usr/local/bin:/usr/bin:/bin
export CUDA_VISIBLE_DEVICES=0

RUN=/home/klein/AMBER_DIAGNOSTIC/simulation/08_compact
cd $RUN

echo "=== GPU Production NPT 1ns ==="
echo "Start: $(date)"
echo "GPU: $(nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null)"

cat > prod.in << 'EOF'
Production NVT 1ns weak CA restraints
 &cntrl imin=0 nstlim=500000 dt=0.002 cut=10 ntb=1 ntp=0
  ntt=3 gamma_ln=2 temp0=300
  ntr=1 restraint_wt=0.5 restraintmask=":1-444@CA"
  ntpr=10000 ntwx=10000 ntwr=100000 iwrap=1 ioutfm=1 /
EOF

$AMBERHOME/bin/pmemd.cuda -O \
  -i prod.in -o prod.out \
  -p /home/klein/AMBER_DIAGNOSTIC/topology/protein_compact.prmtop \
  -c heat.rst -r prod.rst -ref heat.rst -x prod.nc

echo "End: $(date)"
ls -lh prod_npt.nc 2>/dev/null && echo "✅ PRODUCTION COMPLETE" || echo "❌ FAILED"
