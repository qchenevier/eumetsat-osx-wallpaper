# source .zshrc
source ~/.zshrc

# get env name and conda path
env_name=$(head -1 environment.yml | cut -c7-)
conda_path=$(conda env list --json | grep --color=never "\"\/" | head -1 | cut -c6- | rev | cut -c3- | rev)

# launch script
$conda_path/envs/$env_name/bin/python download_earth_from_eumetsat.py
