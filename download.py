import requests

################################################
#### Description ####
# This script download all of all .deb files 
# from a repo's Packages file
# 
####  Usage ####
# python -m venv env
# source env/bin/activate 
# pip install requests
# python download.py
# deactivate
# 
################################################

import requests
import os

def download_packages_file(repo_base_url, packages_file_name='Packages', save_path='.'):
    """
    Download the Packages file from a repository.

    Parameters:
    - repo_base_url: The base URL of the repository.
    - packages_file_name: The name of the Packages file in the repository.
    - save_path: The local directory to save the Packages file.
    """
    packages_url = f"{repo_base_url}/{packages_file_name}"
    response = requests.get(packages_url)
    if response.status_code == 200:
        packages_file_path = os.path.join(save_path, packages_file_name)
        with open(packages_file_path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded {packages_file_name} to {save_path}")
        return packages_file_path
    else:
        print(f"Failed to download {packages_file_name}")
        return None

def download_deb_files(packages_file_path):
    download_directory = 'debians'
    if not os.path.exists(download_directory):
        os.makedirs(download_directory)

    with open(packages_file_path, 'r') as file:
        content = file.read()

    packages = content.split('\n\n')

    for package in packages:
        for line in package.split('\n'):
            if line.startswith('Filename:'):
                filename = line.split(' ')[1].strip()
                deb_url = f"{repo_base_url}/{filename}"
                file_path = os.path.join(download_directory, os.path.basename(filename))

                if not os.path.exists(file_path):
                    response = requests.get(deb_url)
                    if response.status_code == 200:
                        with open(file_path, 'wb') as deb_file:
                            deb_file.write(response.content)
                        print(f'Downloaded {file_path}')
                    else:
                        print(f'Failed to download {filename}')
                else:
                    print(f'File already exists, skipping: {file_path}')
                break

# Example usage
repo_base_url = 'https://repo.misty.moe/apt/'
packages_file_name = 'Packages'  # Assuming the Packages file is directly under the repo base URL
save_path = '.'  # Current directory, but you can specify another path

# Download the Packages file
packages_file_path = download_packages_file(repo_base_url, packages_file_name, save_path)

# If the Packages file was successfully downloaded, proceed to download the .deb files
if packages_file_path:
    download_deb_files(packages_file_path)