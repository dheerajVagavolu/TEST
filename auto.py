import os
import sys
from glob import glob
import numpy as np
import matplotlib.pyplot as plt

#All directory addresses
AUTO_REPO = ""
SCRIPT_DIR = ""
CUR_DIR = ""

# Starting the script in the project directory
cur_dir = os.getcwd()
CUR_DIR = cur_dir
print(cur_dir)

AUTO_REPO = CUR_DIR + "/Auto_Repos"
SCRIPT_DIR = CUR_DIR + "/Evol_stat_plotter"

f = open("repos.txt", "r")
contents = f.readlines()


os.chdir(AUTO_REPO)

# for repo in contents:
#     gitcmd = "git clone " +repo
#     os.system(gitcmd)

repo_folders = next(os.walk('.'))[1]

print(repo_folders)

os.chdir(CUR_DIR)

for a in repo_folders:
    cur_repo = AUTO_REPO+"/"+a
    cmd = "cp Evol_stat_plotter/ultimate.py Auto_Repos/"+a
    cmd1 = "cp Evol_stat_plotter/Doxyfile Auto_Repos/"+a
    os.system(cmd)
    os.system(cmd1)
    os.chdir(cur_repo)
    cmd2 = "python3 ultimate.py 1"
    os.system(cmd2)
    os.chdir(CUR_DIR)
