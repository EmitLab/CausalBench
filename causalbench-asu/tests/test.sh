echo "Creating conda environment..."
conda create -n causal-test python=3.10 -y
conda activate causal-test
cd ../..    
echo "Building package..."
#python -m pip install torch==2.3
pip install build
python -m build
pip install dist/causalbench_asu-0.1rc1-py3-none-any.whl 
cd causalbench-asu/tests
echo "Tests executing"
python execute.py 
