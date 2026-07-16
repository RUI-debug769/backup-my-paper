"""
Paper 2 — OpenMM MD 模拟: MBL_lectin × valeraldehyde
GPU/CPU 自适应, 一步构建+模拟
"""
import sys, os, time
import numpy as np

# Force OpenMM to use CPU (stable, no CUDA setup needed)
os.environ["OPENMM_DEFAULT_PLATFORM"] = "CPU"

from openmm import app, unit
from openmm import XmlSerializer, LangevinMiddleIntegrator, MonteCarloBarostat
import openmm as mm

WORKDIR = os.path.expanduser("~/paper2/md_openmm")
os.makedirs(WORKDIR, exist_ok=True)
PDB_PATH = os.path.expanduser("~/paper2/proteins/A0A3N4L3H6_lectin.pdb")

print("=" * 60)
print("Paper 2 MD: MBL_lectin × valeraldehyde (OpenMM)")
print("=" * 60)

# ============================================================
# 1. 加载 + 修复蛋白
# ============================================================
print("\n[1/6] 加载蛋白结构...")
try:
    from pdbfixer import PDBFixer
    fixer = PDBFixer(filename=PDB_PATH)
    fixer.findMissingResidues()
    fixer.findMissingAtoms()
    fixer.addMissingAtoms()
    fixer.addMissingHydrogens(7.0)
    app.PDBFile.writeFile(fixer.topology, fixer.positions,
                          open(f"{WORKDIR}/protein_fixed.pdb", "w"))
    print(f"  PDBFixer: OK — {fixer.topology.getNumAtoms()} 原子 (含H)")
    topo = fixer.topology
    positions = fixer.positions
except Exception as e:
    print(f"  PDBFixer 失败 ({e}), 直接加载...")
    pdb = app.PDBFile(PDB_PATH)
    topo = pdb.topology
    positions = pdb.positions
    print(f"  {topo.getNumAtoms()} 原子")

# ============================================================
# 2. 力场 + 溶剂化
# ============================================================
print("\n[2/6] 设置力场 + 溶剂化...")
import openmmforcefields
ffxml_dir = os.path.join(os.path.dirname(openmmforcefields.__file__), "ffxml", "amber")
protein_ff = os.path.join(ffxml_dir, "protein.ff14SB.xml")
water_ff = os.path.join(ffxml_dir, "tip3p_standard.xml")
print(f"  力场: ff14SB + TIP3P")
forcefield = app.ForceField(protein_ff, water_ff)
modeller = app.Modeller(topo, positions)

# 加水
modeller.addSolvent(forcefield,
                     model="tip3p",
                     padding=1.2 * unit.nanometers,
                     ionicStrength=0.15 * unit.molar,
                     positiveIon="Na+",
                     negativeIon="Cl-")
print(f"  溶剂化: {modeller.topology.getNumAtoms()} 总原子")

# ============================================================
# 3. 构建 System
# ============================================================
print("\n[3/6] 构建物理系统...")
system = forcefield.createSystem(modeller.topology,
                                  nonbondedMethod=app.PME,
                                  nonbondedCutoff=1.0 * unit.nanometers,
                                  constraints=app.HBonds)
print(f"  {system.getNumParticles()} 粒子, {system.getNumForces()} 力")

# ============================================================
# 4. 积分器 + 恒压器
# ============================================================
print("\n[4/6] 设置积分器...")
integrator = LangevinMiddleIntegrator(300 * unit.kelvin,  # 室温起步
                                       1.0 / unit.picoseconds,
                                       2.0 * unit.femtoseconds)
# 恒压
system.addForce(MonteCarloBarostat(1.0 * unit.atmospheres,
                                    300 * unit.kelvin, 25))

# ============================================================
# 5. Simulation 对象
# ============================================================
print("\n[5/6] 选择计算平台...")
platforms = [mm.Platform.getPlatform(i) for i in range(mm.Platform.getNumPlatforms())]
plat_names = [p.getName() for p in platforms]
print(f"  可用平台: {plat_names}")

# 优先 CUDA → OpenCL → CPU
target = "CUDA" if "CUDA" in plat_names else ("OpenCL" if "OpenCL" in plat_names else "CPU")
platform = mm.Platform.getPlatformByName(target)
print(f"  使用: {target}")

sim = app.Simulation(modeller.topology, system, integrator, platform)
sim.context.setPositions(modeller.positions)
print(f"  Simulation 就绪")

# ============================================================
# 6. 能量最小化 → 平衡 → 生产
# ============================================================
print("\n[6/6] 运行 MD...")

# 6a. 最小化
print("  最小化...")
sim.minimizeEnergy(maxIterations=1000)
state = sim.context.getState(getEnergy=True)
print(f"  初始能量: {state.getPotentialEnergy().value_in_unit(unit.kilojoules_per_mole):.0f} kJ/mol")

# 6b. NVT 平衡 (100 ps)
print("  NVT 平衡 (100 ps)...")
sim.reporters.append(app.StateDataReporter(
    sys.stdout, 1000, step=True, temperature=True,
    potentialEnergy=True, speed=True, separator="\t"))
sim.reporters.append(app.DCDReporter(f"{WORKDIR}/trajectory.dcd", 1000))

sim.step(50000)  # 100 ps at 2 fs

# 6c. NPT 平衡 (100 ps)
print("  NPT 平衡...")
sim.step(50000)

# 6d. 生产 MD (1 ns 测试)
print(f"\n  生产 MD (1 ns, {target} 平台)...")
t0 = time.time()
sim.step(500000)  # 1 ns
elapsed = time.time() - t0
ns_per_day = (1.0 / (elapsed / 86400))
print(f"\n  模拟速度: {ns_per_day:.0f} ns/day ({target} 平台)")
print(f"  预计 200ns: {200/ns_per_day:.1f} 天")

# ============================================================
# 7. 保存最终状态
# ============================================================
print(f"\n保存结果...")
sim.saveState(f"{WORKDIR}/final_state.xml")
# Extract final coordinates
state = sim.context.getState(getPositions=True)
app.PDBFile.writeFile(sim.topology, state.getPositions(),
                      open(f"{WORKDIR}/final_frame.pdb", "w"))
print(f"✅ MD 测试完成!")
print(f"  轨迹: {WORKDIR}/trajectory.dcd")
print(f"  最终构象: {WORKDIR}/final_frame.pdb")
