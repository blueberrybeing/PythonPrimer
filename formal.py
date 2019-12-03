# -*- coding: utf-8 -*-
import sys
import shutil
import zipfile
import os
import requests
import check_formal_hall

names = {
    'hall':'_21_0.zip',
    'common':'_21_2.zip',
    'platform_default':'_21_2.zip',

    # # 'festivity':'_18_5.zip',
    # 'spring_guide':'_19_5.zip',
    # 'summer_guide':'_20_7.zip',
    # 'spring_festival':'_19_1.zip',
    # 'fools_day':'_19_1.zip',
    'festivity55':'_20_6.zip',
    # # 'zhd_bsmz':'_19_1.zip',
    'zhd_jfjs':'_20_3.zip',


    # 'common_jj':'_19_4.zip',
    # 'bcbm':'_19_5.zip',
    # 'fkszg':'_18_5.zip',
    # 'fruit':'_18_4.zip',
    # # 'hhmf':'_18_4.zipn,
    # 'jlbd':'_18_5.zip', 
    # # 'phoenix':'_18_3.zip',
    # 'shz':'_19_5.zip',
    # # 'slwh':'_18_4.zip',
    # 'slwh3D':'_18_8.zip',
    # 'xyzb':'_18_6.zip',
    # 'fkzww':'_18_4.zip',
    'xxl':'_21_1.zip',
    'shbz':'_21_1.zip',

    # 'common_qp':'_18_7.zip',
    'fkjh':'_18_10.zip',
    # 'brnn':'_18_7.zip',
    'ddz':'_19_11.zip',
    # 'xydz':'_18_4.zip',
    # 'sgzb':'_18_8.zip',
    # 'fkmj':'_19_3.zip',

    'common_by':'_21_1.zip',
    # 'shby':'_20_4.zip',
    # 'fishing':'_20_5.zip', 
    # # 'fkby':'_20_5.zip', 
    # # 'classic':'_5_3.zip', 
    # # 'djs':'_5_3.zip', 
    # # 'lwmj':'_6_0.zip', 
    # # 'monkey':'_5_3.zip', 
    # # 'public':'_5_3.zip', 
    # # 'public_fkby_scene':'_1_1.zip', 
    # # 'sgdk':'_5_1.zip',

}

skins = [
    "hall_21_2.zip",
]

skin_folders = ["skins_12489", "skins_10001","skins_10002","skins_10003","skins_10004","skins_10005" ]

def cp_skin_zips(mypath, skins_folder):
    skins_path = os.path.join(mypath, skins_folder)
    if os.path.exists(skins_path):
        shutil.rmtree(skins_path)
    os.makedirs(skins_path)

    for zip_name in skins:
        tempfile = os.path.join("Z:\\" + skins_folder, zip_name)
        pub_file = os.path.join(skins_path, zip_name)
        if os.path.isfile(tempfile):
            print("copy zip:" + tempfile )
            with open(pub_file, 'wb') as f:
                shutil.copyfile(tempfile, pub_file)
        else:
            print("file does not exists:" + tempfile)

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
    # generate_cdn_list(mypath)

    # check 
    print("---check_formal_hall---")
    check_formal_hall.check_files()

    print "success"
    os.system("pause")
