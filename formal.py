# -*- coding: utf-8 -*-
import sys
import shutil
import zipfile
import os
import requests

names = {
   'hall':'_19_4.zip',
    'common':'_19_2.zip',

    # 'festivity':'_18_4.zip',
    # 'spring_guide':'_19_3.zip',
    # 'spring_festival':'_19_0.zip',
    # 'fools_day':'_19_0.zip',
    'festivity51':'_19_0.zip',
    'zhd_bsmz':'_19_0.zip',


    # 'common_jj':'_19_0.zip',
    # 'bcbm':'_19_1.zip',
    'fkszg':'_18_2.zip',
    # 'fruit':'_18_1.zip',
    'hhmf':'_18_3.zip',
    'jlbd':'_18_3.zip',
    # 'phoenix':'_18_2.zip',
    # 'shz':'_19_1.zip',
    'slwh':'_18_3.zip',
    'slwh3D':'_18_5.zip',
    # 'xyzb':'_18_3.zip',
    'fkzww':'_18_2.zip',

    # 'common_qp':'_18_3.zip',
    'fkjh':'_18_4.zip',
    # 'brnn':'_18_4.zip',
    'ddz':'_19_5.zip',
    # 'xydz':'_18_2.zip',
    'sgzb':'_18_5.zip',

    'common_by':'_19_3.zip',
    'shby':'_19_4.zip',
    'fishing':'_19_4.zip', 
    'fkby':'_19_4.zip',
    'classic':'_4_4.zip',
    'djs':'_4_3.zip',
    'lwmj':'_4_3.zip',
    'monkey':'_4_4.zip',
    'public':'_4_4.zip',
    'sgdk':'_4_3.zip',
}

skins = [
    'hall_19_0.zip',
    'hall_19_1.zip',
    'hall_19_2.zip',
    'hall_19_3.zip',
    'hall_19_4.zip',
]

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

    # cp skins
    skins_folder = "skins_12489"
    skins_path = os.path.join(mypath, skins_folder)
    if os.path.exists(skins_path):
        shutil.rmtree(skins_path)
    os.makedirs(skins_path)

    for i, value in enumerate(skins):
        print("fuck------------->>>" +  value)
        zip_name = value
        tempfile = os.path.join("Z:\\skins_12489", zip_name)
        pub_file = os.path.join(skins_path, zip_name)
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
