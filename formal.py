# -*- coding: utf-8 -*-
import sys
import shutil
import zipfile
import os
import requests

names = {
    'hall':'_17_1.zip',
    'common':'_18_0.zip',

    'bcbm':'_17_0.zip',
    'fkszg':'_17_0.zip',
    'fruit':'_17_0.zip',
    'hhmf':'_17_0.zip',
    'jlbd':'_17_0.zip',
    'phoenix':'_17_0.zip',
    'shz':'_17_0.zip',
    'slwh':'_17_0.zip',
    'slwh3D':'_17_0.zip',
    'xyzb':'_17_0.zip',

    'fkjh':'_17_0.zip',
    'brnn':'_17_0.zip',
    'ddz':'_17_0.zip',
    'xydz':'_17_0.zip',

    'fkby':'_17_0.zip',
    'classic':'_2_0.zip',
    'djs':'_2_0.zip',
    'lwmj':'_2_0.zip',
    'monkey':'_2_0.zip',
    'public':'_2_0.zip',
    'sgdk':'_2_0.zip',
}

def cp_pre_zips(mypath):
    if os.path.exists(mypath):
        shutil.rmtree(mypath)
    os.makedirs(mypath)

    for key, value in names.items():
        zip_name = key+value
        tempfile = os.path.join("Y:\\", zip_name)
        pub_file = os.path.join(mypath, zip_name)
        if os.path.isfile(tempfile):
            print("copy zip:" + zip_name )
            with open(pub_file, 'wb') as f:
                shutil.copyfile(tempfile, pub_file)
        else:
            print("file does not exists:" + zip_name)
            return

def generate_cdn_list(mypath):
    filename = mypath +"\cdn_list.lua"
    pre_str = "https://www.dafuhao-ol.com/JspUpDownTest/myfiles/"
    with open(filename, 'w') as f:    
        for key, value in names.items():
            cdn_path = pre_str + key + value + "\n"
            f.write(cdn_path)

if __name__ == '__main__':
    os.chdir("E:/update_pre")
    mypath = os.path.join(os.getcwd(),"formal")

    cp_pre_zips(mypath)
    generate_cdn_list(mypath)

    print "success"
    os.system("pause")
