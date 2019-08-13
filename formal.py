# -*- coding: utf-8 -*-
import sys
import shutil
import zipfile
import os
import requests

names = {
    'hall':'_20_2.zip',
    # 'common':'_20_1.zip',
    # 'platform_default':'_20_1.zip',

    # 'festivity':'_18_5.zip',
    # 'spring_guide':'_19_4.zip',
    # 'summer_guide':'_20_3.zip',
    # 'spring_festival':'_19_0.zip',
    # 'fools_day':'_19_0.zip',
    # 'festivity51':'_19_1.zip',
    # 'festivity55':'_19_2.zip',
    # 'zhd_bsmz':'_19_1.zip',


    'common_jj':'_19_3.zip',
    'bcbm':'_19_3.zip',
    # 'fkszg':'_18_4.zip',
    'fruit':'_18_3.zip',
    # 'hhmf':'_18_4.zip',
    # 'jlbd':'_18_4.zip', 
    # 'phoenix':'_18_3.zip',
    # 'shz':'_19_3.zip',
    # 'slwh':'_18_4.zip',
    'slwh3D':'_18_7.zip',
    # 'xyzb':'_18_4.zip',
    # 'fkzww':'_18_3.zip',

    'common_qp':'_18_5.zip',
    'fkjh':'_18_6.zip',
    'brnn':'_18_6.zip',
    'ddz':'_19_8.zip',
    # 'xydz':'_18_3.zip',
    # 'sgzb':'_18_6.zip',
    # 'fkmj':'_19_0.zip',

    # 'common_by':'_20_1.zip',
    # 'shby':'_20_2.zip',
    # 'fishing':'_20_2.zip', 
    'fkby':'_20_2.zip',
    # 'classic':'_5_1.zip',
    # 'djs':'_5_1.zip',
    # 'lwmj':'_5_1.zip',
    # 'monkey':'_5_1.zip',
    # 'public':'_5_1.zip',
    # 'sgdk':'_5_0.zip',
    # 'public_fkby_scene':'_1_0.zip',

}

skins = {
    'hall':'_20_2.zip',
}

skin_folders = ["skins_12489", "skins_10001"]

def cp_skin_zips(mypath, skins_folder):
    skins_path = os.path.join(mypath, skins_folder)
    if os.path.exists(skins_path):
        shutil.rmtree(skins_path)
    os.makedirs(skins_path)

    for key, value in skins.items():
        zip_name = key+value
        tempfile = os.path.join("Z:\\" + skins_folder, zip_name)
        pub_file = os.path.join(skins_path, zip_name)
        if os.path.isfile(tempfile):
            print("copy zip:" + tempfile )
            with open(pub_file, 'wb') as f:
                shutil.copyfile(tempfile, pub_file)
        else:
            print("file does not exists:" + zip_name)
            return

def cp_pre_zips(mypath):
    if os.path.exists(mypath):
        shutil.rmtree(mypath)
    os.makedirs(mypath)

    for key, value in names.items():
        zip_name = key+value
        tempfile = os.path.join("Z:\\", zip_name)
        pub_file = os.path.join(mypath, zip_name)
        if os.path.isfile(tempfile):
            print("copy zip:" + tempfile)
            with open(pub_file, 'wb') as f:
                shutil.copyfile(tempfile, pub_file)
        else:
            print("file does not exists:" + tempfile)
            return

    # cp skins
    for folder in skin_folders:
        cp_skin_zips(mypath,folder)


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
