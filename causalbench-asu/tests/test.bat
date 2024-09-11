@echo off
echo Creating conda environment...
call conda create -n causal-test python=3.10 -y
echo Conda environment is created
call conda activate causal-test
echo Conda environment is activated

cd ../..
echo Building package...
pip install gcastle
pip install torch
pip install build
python -m build
pip install dist\causalbench_asu-0.1rc3-py3-none-any.whl

cd causalbench-asu\tests
echo Tests executing
python test-execute.py
