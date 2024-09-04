conda create -n causal-test python=3.10.6 -y
conda activate causal-test
python -m pip install --upgrade pip
cd ../..    
pip install torch==2.3.0 --index-url https://download.pytorch.org/whl/torch_stable.html
pip install build
python -m build
pip install dist/causalbench_asu-0.1rc1-py3-none-any.whl 
cd causalbench-asu/tests
python execute.py 
