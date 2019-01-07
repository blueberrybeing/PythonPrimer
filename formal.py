# -*- coding: utf-8 -*-
import sys
import shutil
import zipfile
import os
import requests

names = {
    'hall':'_18_5.zip',
    'common':'_18_6.zip',
    
    'festivity':'_18_4.zip',

    # 'common_jj':'_18_1.zip',
    # 'bcbm':'_18_0.zip',
    # 'fkszg':'_18_0.zip',
    # 'fruit':'_18_0.zip',
    # 'hhmf':'_18_0.zip',
    # 'jlbd':'_18_1.zip',
    # 'phoenix':'_18_1.zip',
    # 'shz':'_18_0.zip',
    # 'slwh':'_18_1.zip',
    # 'slwh3D':'_18_2.zip',
    'xyzb':'_18_2.zip',
    # 'fkzww':'_18_0.zip',

    # 'common_qp':'_18_0.zip',
    # 'fkjh':'_18_1.zip',
    # 'brnn':'_18_1.zip',
    # 'ddz':'_18_1.zip',
    # 'xydz':'_18_1.zip',
    # 'sgzb':'_18_2.zip',

    # 'shby':'_18_1.zip',
    # 'fishing':'_18_1.zip',
    # 'fkby':'_18_1.zip',
    # 'classic':'_3_1.zip',
    # 'djs':'_3_0.zip',
    # 'lwmj':'_3_0.zip',
    # 'monkey':'_3_0.zip',
    # 'public':'_3_0.zip',
    # 'sgdk':'_3_0.zip',
}

def cp_pre_zips(mypath):
    if os.path.exists(mypath):
        shutil.rmtree(mypath)
    os.makedirs(mypath)

    for key, value in names.items():
        zip_name = key+value
        tempfile = os.path.join("Z:\\", zip_name)
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
    os.chdir("C:\Workspace\pub_formal")
    mypath = os.path.join(os.getcwd(),"formal")

    cp_pre_zips(mypath)
    generate_cdn_list(mypath)

    print "success"
    os.system("pause")
