echo "Creating conda environment..."
conda create -n causal-test python=3.10 -y
echo Conda environment is created
conda activate causal-test
echo Conda environment is activated
cd ../..    
echo "Building package..."

# Model dependicies are not installed automatically so needs to be installed manually until fix
pip install gcastle
pip install torch

pip install build
python -m build
pip install $(ls dist/*.whl | sort | tail -n 1)
pip install pytest
pip install PyJWT
cd causalbench-asu/tests
echo "Test system"
python test-execute.py 
echo "Test login function"
python test-auth.py 
echo "Test dataset functions"
python test-data.py 
echo "Test model functions"
python test-model.py 
echo "Test metric functions"
python test-metric.py 
echo "Test task functions"
python test-task.py 
