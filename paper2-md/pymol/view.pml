# Paper 2 — MBL Lectin + Valeraldehyde 1ns MD
# 在 PyMOL 中: File → Run Script → 选择此文件

delete all
load first_frame.pdb, system
load strip.dcd, system

show cartoon, system and polymer
color marine, system and polymer
show sticks, resn VDL
color magenta, resn VDL
select binding_site, (resn VDL around 5) and polymer
show sticks, binding_site
color salmon, binding_site
intra_fit system
zoom resn VDL, 8
bg_color white
set movie_loop, 1

print "Paper 2 — MBL Lectin + Valeraldehyde 1ns MD"
print "  Blue = protein  |  Magenta = ligand  |  Orange = binding site"
