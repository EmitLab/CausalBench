conda create -n causal-test python=3.10 -y
conda activate causal-test
python3 -m pip install --upgrade pip
cd ../..    
pip3 install torch
pip3 install build
python -m build
pip3 install dist/causalbench_asu-0.1rc1-py3-none-any.whl 
cd causalbench-asu/tests
python3 execute.py 
