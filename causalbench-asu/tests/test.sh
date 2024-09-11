echo "Creating conda environment..."
conda create -n causal-test python=3.10 -y
conda activate causal-test
cd ../..    
echo "Building package..."
pip install gcastle
pip install torch
pip install build
python -m build
pip install dist/causalbench_asu-0.1rc3-py3-none-any.whl 
pip install pytest
cd causalbench-asu/tests
echo "Test system"
python test-execute.py 
echo "Test login function"
python test-auth.py 
