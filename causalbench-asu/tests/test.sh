conda create -n causal-test python=3.10 -y
source activate base 
conda activate causal-test
pip install torch
cd ../        
pip install .
cd tests
python execute.py 