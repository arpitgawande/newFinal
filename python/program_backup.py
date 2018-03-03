
# coding: utf-8

# In[ ]:

import os
import subprocess
import glob
from shutil import move, copy

from git import Repo,remote

program_folder = './programs/'
os.makedirs(program_folder, exist_ok=True)

notebook_folder = program_folder + './notebooks/'
os.makedirs(notebook_folder, exist_ok=True)

python_folder = program_folder +'./python/'
os.makedirs(python_folder, exist_ok=True)

pdf_folder = program_folder +'./pdf/'
os.makedirs(pdf_folder, exist_ok=True)

notebook_list = glob.glob('*.ipynb')
print('Notebook List:', notebook_list)            
for filename in notebook_list:
    subprocess.check_call(['jupyter', 'nbconvert', '--to', 'script', filename])
    #subprocess.call(['jupyter', 'nbconvert', '--to', 'pdf', filename])

for filename in notebook_list:
    try:
        copy(filename, notebook_folder)
        print('copied:', filename)
        filename = filename.split('.')[0]+'.py'
        move(filename, python_folder)
        print('moved:', filename)
        filename = filename.split('.')[0]+'.pdf'
        move(filename, pdf_folder)
        print('moved:', filename)
        print('******************')
    except Exception as err:
        print(err)

os.chdir(program_folder)
subprocess.check_call('git add .', shell=True)
subprocess.check_call('git commit -m "New updates"', shell=True)
subprocess.check_call('git push -u origin master', shell=True)

# #remote_url = 'https://github.com/arpitgawande/newFinal.git'        
# repo = Repo(program_folder)
# origin = repo.remote(name='origin')
# #origin = repo.create_remote('origin', url=remote_url)
# assert origin.exists()
# repo.index.add(['./*'])
# master = repo.heads.master
# repo.git.commit('-m', 'New Updates', author='Arpit')
# origin.push()

