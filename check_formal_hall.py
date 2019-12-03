# encoding=utf8

import os
import sys
import zipfile
import shutil
import re


# ###############################
cur_dir = os.path.dirname(os.path.abspath(__file__))
formal_dir = os.path.join(cur_dir, "formal")
check_dir = os.path.join(cur_dir, "check") 
real_check_list = []
# ###############################

def get_hall_zip_name():
    node_names = os.listdir(formal_dir)
    for node_name in node_names:
        if node_name.find("hall") != -1:
            return node_name
    return None

def extract_check_file_from_zip(zip_name):
    check_list = ["update", "seed"]
    with zipfile.ZipFile(zip_name) as f:
        for check in check_list:
            c = re.compile("%s.*"%check) 
            for name in f.namelist():
                # if name.find(check_file) != -1:
                if c.search(name) != None:
                    f.extract(name, check_dir)
                    print("need check: " + name)
                    real_check_list.append(name)
        

def create_check_files():
    zip_name = get_hall_zip_name()
    if zip_name != None:
        hall_zip_file = os.path.join(formal_dir, zip_name)
        extract_check_file_from_zip(hall_zip_file)

# ################### decode ####################
def lstFilesByDir(_dir,_func=None,recursion=True):
    dirs = os.listdir(_dir)
    for item in dirs:
        fullPath = os.path.join(_dir,item)
        if os.path.isdir(fullPath):
            if recursion:
                lstFilesByDir(fullPath,_func,recursion)
        else:
            if _func:
                _func(fullPath)

def funcXXTEA(path1,path2):
    command = ""
    if sys.platform == 'win32':
        command = "call xxtea decrypt god key_file=key {0} {1}".format(path1,path2)
    else:
        command = "./xxtea decrypt god key_file=key {0} {1}".format(path1,path2)
    retCommand = os.system(command)
    if  retCommand != 0:
        raise Exception("error:{0}".format(path1))


def func(path):
    fileName = os.path.basename(path)
    arr = os.path.splitext(fileName)
    fileDir =os.path.dirname(path)
    if len(arr)!=2:
        return
    if arr[1]==".luac":
        funcXXTEA(path,os.path.join(fileDir,arr[0])+".lua")
        os.remove(path)
    elif arr[1]==".png" or arr[1]==".jpg":
        funcXXTEA(path,path)
# #######################################

def clear_check_dir():
    if os.path.exists(check_dir):
        shutil.rmtree(check_dir)
    else:
        os.makedirs(check_dir)

def decode_check_files():
    print("decode check file begin")
    if os.path.isdir(check_dir):
        lstFilesByDir(check_dir, func)

def check_apiConfig():
    print("check apiConfig begin")
    apiConfig = os.path.join(check_dir, "update/script/apiConfig.lua")
    c = re.compile(r"^apiConfig\.GAME_SVR_TYPE\s*=")
    c2 = re.compile(r"^apiConfig\.GAME_SVR_TYPE\s*=\s*1")
    if os.path.isfile(apiConfig):
        check_line = ""
        with open(apiConfig,"rb") as f:
            for line in f.readlines():
                if c.search(line) != None:
                    print(line)
                    assert(c2.search(line) != None), 'apiConfig.GAME_SVR_TYPE != 1'          
                    break
    else:
        print("apiConfig file not exist!!!")

def check_seed_line(line):
    seed_list = ['debug', 'binary_debug', 'network_dump', 'active', 'crash_pop']        
    c2 = re.compile("r.*false")
    for seed in seed_list:
        c = re.compile(r"^seed\.%s"%seed)
        if c.search(line) != None:
            print(line)
            assert(c2.search(line) != None), 'seed debug switch must be false'
            # assert (line.strip().strip('\n').endswith('false')), 'seed debug must be false !' 

def check_seed():
    print("check seed begin")
    seed = os.path.join(check_dir, "script/seed.lua")
    if os.path.isfile(seed):
        with open(seed,"rb") as f:
            for line in f.readlines():
                check_seed_line(line)        

def check_files():
    clear_check_dir()
    create_check_files()
    if len(real_check_list) > 0:
        decode_check_files()
        check_apiConfig()
        check_seed()
    else:
        print("no check files, no need to check")

if __name__ == '__main__':
    check_files()





    
