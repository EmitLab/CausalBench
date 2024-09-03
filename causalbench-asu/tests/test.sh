mkdir -p ~/miniconda3
curl https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh -o ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm ~/miniconda3/miniconda.sh
conda create -n causal-test python=3.10 -y
conda activate causal-test
pip install torch
cd ..      
pip install .
cd tests
python execute.py 