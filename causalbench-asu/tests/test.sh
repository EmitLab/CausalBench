mkdir -p ~/miniconda3
curl https://repo.anaconda.com/miniconda/Miniconda3-py39_24.5.0-0-MacOSX-x86_64.sh -o ~/miniconda/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm ~/miniconda3/miniconda.sh
conda create -n causal-test python=3.10 -y
conda activate causal-test
pip install torch
cd ..      
pip install .
cd tests
python execute.py 