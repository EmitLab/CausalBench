conda create -n causal-test python=3.10 -y
conda activate causal-test
python -m pip install --upgrade pip
cd ../..    
conda install pytorch==2.3.0 torchvision==0.18.0 torchaudio==2.3.0 -c pytorch
pip install build
python -m build
pip install dist/causalbench_asu-0.1rc1-py3-none-any.whl 
cd causalbench-asu/tests
python execute.py 
