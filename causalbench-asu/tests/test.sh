conda create -n causal-test python=3.10 -y
source activate base 
conda activate causal-test
pip install torch
cd causalbench-asu/        
pip install .
cd causalbench-asu/tests
python execute.py 