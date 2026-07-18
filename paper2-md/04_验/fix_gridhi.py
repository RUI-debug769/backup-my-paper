path = "/home/klein/amber26_src/pmemd26_src/src/pmemd/src/mdin_ewald_dat.F90"
f = open(path).read()
f = f.replace("gridhi = 512", "gridhi = 1024")
open(path, "w").write(f)
print("gridhi changed: 512 -> 1024")