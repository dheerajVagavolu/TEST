import os
import sys
from glob import glob
import numpy as np
import matplotlib.pyplot as plt

#All directory addresses
REPO_DIR = ""
OUTPUT_DIR = ""
DOT_DIR = ""
MAPS_DIR = ""


#List for tagnames
TAG_LIST = []
components = []
# MAP = {}

# Starting the script in the project directory
cur_dir = os.getcwd()
REPO_DIR = cur_dir
print(cur_dir)


#Creating the tags in a text file.
cmd_tags = 'git tag --sort=creatordate > tagnames'
os.system(cmd_tags)


#Creating a new directory for outputs
new_dir = cur_dir+"/outs_test"
OUTPUT_DIR = new_dir
make = "mkdir " + new_dir
os.system(make)

#Changing directory to output directory
os.chdir(new_dir)
print(os.getcwd())

#creating dots directory for dot files
cur_dir = os.getcwd()
new_dir = cur_dir+"/dots"
DOT_DIR = new_dir
make = "mkdir " + new_dir
os.system(make)

#Changing the directory back to REPO_DIR
os.chdir(REPO_DIR)
print(os.getcwd())

#Reading the tags file and adding to a list
f=open("tagnames","r")

for i in f:
    print("<"+i.strip()+">")
    TAG_LIST.append(i)

f.close()

#Generating the doxygen file for each version and returning to master branch

for i in TAG_LIST:
    i = i.strip()
    command = "git checkout tags/"+i
    os.system(command)
    command = "doxygen > /dev/null 2>&1"
    os.system(command)
    command = "mkdir "+DOT_DIR+"/"+i
    os.system(command)
    command = "find . -name \"*.dot\" | xargs -n 100 cp -t \""+DOT_DIR+"/" +i+"\""
    os.system(command)

command = "git checkout master"
os.system(command)


#Creating the directory for component maps combined

os.chdir(DOT_DIR)
try:
    os.mkdir("component_maps")
except:
    pass
MAPS_DIR = DOT_DIR+"/"+"component_maps"


#Creating different text files for different tags

for k,ii in enumerate(TAG_LIST):

    
    f = open(DOT_DIR+"/component_maps/map_"+str(k)+".txt","w")
    of = open(DOT_DIR+"/component_maps/comp_"+str(k)+".txt","w")
    ii = ii.strip()

    string_decider = "__coll__"

    if(int(sys.argv[1])==0):
        string_decider = "_c"
    elif(int(sys.argv[1])==1):
        string_decider = "__coll__"

    print(string_decider)
    

    all_dots = glob(DOT_DIR + "/" + ii + "/*.dot", recursive=True)

    components = []
    map={}
    MAP = {}
    for each in all_dots:
        with open(each) as dot:
            for line in dot.readlines():
                if "label=" in line:
                    components.append(line.split('"')[1])
    
    components.sort()

    for i in range(len(components)):
        map[components[i]] = i
    
    for num,i in enumerate(map):
        MAP[i] = num
        of.write(i+'\n')


    print("->" + str(len(all_dots)))
    

    for each in all_dots:
   
        nodes = {}
        with open(each) as dot:
            for line in dot.readlines():
                if "label=" in line:
                    ar = line.split()
                    node = ar[0].strip()
                    label = line.split('"')[1]
                    nodes[node] = "Node"+str(MAP[label])
        print(nodes)
        with open(each) as dot:
            for line in dot.readlines():
                if "->" in line:
                    ar = line.split()
                    left = ar[0].strip()
                    right = ar[2].strip()
                    line = nodes[left] + "->" + nodes[right]+"\n"
                    f.write(line)
                elif "label=" in line:
                    ar = line.split()
                    node = ar[0].strip()
                    f.write(node+'\n')
        print("======================================")
    f.close()
    of.close()

# Capturing changes



os.chdir(MAPS_DIR)

g_add = []
g_sub = []
g_sub_init = []

g_add.append(0)
g_sub.append(0)
g_sub_init.append(0)

f3 = open("comp_0.txt",'r')
original_comps = f3.readlines()
f3.close()

for k in range(len(TAG_LIST)-2):
    old = "comp_"+str(k)+".txt"
    new = "comp_"+str(k+1)+".txt"

    f1 = open(old,'r')
    f2 = open(new,'r')

    add = 0
    sub = 0
    sub_init = 0

    l_one = f1.readlines()
    l_two = f2.readlines()

    f1.close()
    f2.close()


    comps_list = []

    for i in l_one:
        if i not in l_two:
            sub = sub+1
            comps_list.append(i)
    

    for i in l_two:
        if i not in l_one:
            add = add+1
    
    
    for i in comps_list:
        if i in original_comps:
            sub_init = sub_init+1


    
    g_add.append(add)
    g_sub.append(sub)
    g_sub_init.append(sub_init)


    print(add)
    print(sub)
    print(sub_init)


bar_width = 0.25

r1 = np.arange(len(g_add))
r2 = [x+bar_width for x in r1]
r3 = [x+bar_width for x in r2]

plt.bar(r1, g_add, color='green', width=bar_width, edgecolor='white', label='added')
plt.bar(r2, g_sub, color='red', width=bar_width, label='Subbed')
plt.bar(r3, g_sub_init, color="#FFDF00", width=bar_width, label='Subbed_init')

plt.legend()


if int(sys.argv[1])==0:
    print("_c - using call graphs")
elif int(sys.argv[1])==1:
    print("__coll__ - using collaborative graphs")


plt.savefig('out.png')



























