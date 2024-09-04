conda create -n causal-test python=3.10.14 -y
conda activate causal-test
python -m pip install --upgrade pip
cd ../..    
pip install torch==2.3.0 --index-url https://download.pytorch.org/whl/cpu-cxx11-abi/torch-2.3.0%2Bcpu.cxx11.abi-cp310-cp310-linux_x86_64.whl
pip install build
python -m build
pip install dist/causalbench_asu-0.1rc1-py3-none-any.whl 
cd causalbench-asu/tests
python execute.py 
