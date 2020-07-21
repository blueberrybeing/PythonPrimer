# -*- coding: utf-8 -*-
import sys
import shutil
import zipfile
import os
import requests
import check_formal_hall

# skins = ["hall_23_0.zip","platform_default_23_0.zip"]
skins = ["hall_24_2.zip"]
# skins = ["platform_default_23_0.zip"]
names = {
    'hall'              :'_24_2.zip',
    'common'            :'_24_1.zip',
    'platform_default'  :'_24_1.zip',

    'festivity55'       :'_21_9.zip',
    # 'zhd_bsmz'          :'_19_1.zip',
    # 'zhd_jfjs'          :'_20_4.zip',
    'guide'             :'_24_1.zip',
    'card'              :'_24_1.zip',
    'activityNewUser'   :'_24_0.zip',

    'common_jj'         :'_19_8.zip',
    'fkzww'             :'_18_8.zip',
    'xxl'               :'_21_9.zip',
    # 'shbz'              :'_21_9.zip',
    'jzsc'              :'_22_3.zip',

    'common_qp'         :'_18_12.zip',
    'fkjh'              :'_18_15.zip',
    'ddz'               :'_24_1.zip',
    # 'sgzb'              :'_18_12.zip',
    'fkmj'              :'_19_10.zip',

    'paths'             :'_2_0.zip',
    'xfish'             :'_24_2.zip',
    'xmxxl'             :'_24_1.zip',
    # 'hwby'              :'_24_0.zip',

    'common_by'         :'_25_0.zip',
    'shby'              :'_23_0.zip',
    'fishing'           :'_22_0.zip',
    # 'common_by_spirit'  :'_1_3.zip',
    'common_by_game'    :'_3_0.zip',
    'fkby'              :'_23_0.zip',
    'classic'           :'_7_0.zip',
    'djs'               :'_6_0.zip',
    'lwmj'              :'_7_0.zip',
    'monkey'            :'_6_0.zip',
    'public'            :'_7_0.zip',
    'public_fkby_scene' :'_2_0.zip',
    'sgdk'              :'_5_7.zip',
    'bxgh'              :'_2_0.zip',
    'res_bxgh'          :'_1_0.zip',
    'res_chaoji'        :'_1_0.zip',
    'res_fuhao'         :'_1_0.zip',
    'res_longwangmijing':'_1_0.zip',
    'res_monkeyking'    :'_1_0.zip',
    'res_xinshou'       :'_1_0.zip',
    'res_zhizun'        :'_1_0.zip',
}



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
