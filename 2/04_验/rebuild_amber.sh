#!/bin/bash
# AMBER 26 重编译 — gridhi=1024 fix
# 在 WSL 终端运行: bash /home/klein/rebuild_amber.sh

export AMBERHOME=/home/klein/amber26
SRC=/home/klein/amber26_src/pmemd26_src

# 1. 确认 gridhi 已修改
echo "=== gridhi 检查 ==="
grep -n "gridhi" $SRC/src/pmemd/src/mdin_ewald_dat.F90

# 2. cmake 配置
cd $SRC/build
cmake $SRC \
  -DCMAKE_INSTALL_PREFIX=$AMBERHOME \
  -DCOMPILER=GNU \
  -DCUDA=TRUE \
  -DMPI=FALSE \
  -DBUILD_PYTHON=FALSE \
  -DDOWNLOAD_MINICONDA=FALSE \
  -DCMAKE_CUDA_COMPILER=/usr/local/cuda-12.8/bin/nvcc \
  -DCUDA_TOOLKIT_ROOT_DIR=/usr/local/cuda-12.8

# 3. 只编译 GPU MD 引擎（快）
make -j$(nproc) pmemd.cuda

# 4. 安装
cp $SRC/build/pmemd.cuda $AMBERHOME/bin/pmemd.cuda
echo "=== DONE ==="
$AMBERHOME/bin/pmemd.cuda --version
