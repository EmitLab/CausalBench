conda create -n causal-test python=3.10 -y
conda activate causal-test
pip install torch
cd ..      
pip install .
cd /tests
python execute.py 