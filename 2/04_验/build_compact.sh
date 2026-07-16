#!/bin/bash
export AMBERHOME=/home/klein/amber26
export PATH=$AMBERHOME/bin:/usr/local/cuda-12.8/bin:/usr/local/bin:/usr/bin:/bin
export CUDA_VISIBLE_DEVICES=0
cd /home/klein/AMBER_DIAGNOSTIC

# Build compact topology (8Å padding → higher density)
tleap -f - << 'EOF'
source leaprc.protein.ff19SB
source leaprc.water.tip3p
mol = loadpdb /home/klein/AMBER_DIAGNOSTIC/cleaned/protein_clean.pdb
solvatebox mol TIP3PBOX 8.0
addions mol Na+ 0
saveamberparm mol topology/protein_compact.prmtop topology/protein_compact.inpcrd
quit
EOF

ls -lh topology/protein_compact.prmtop && echo "COMPACT OK"
