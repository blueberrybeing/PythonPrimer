  # -*- coding: utf-8 -*-
# zip.py
import sys
import shutil
import zipfile
import os
import requests
import pysvn
import json

pathSVN = ""
svnVerA = "" 
svnVerB = ""
mypath = ""
outpath = ""
Path = ""
majorVer = "_20_0.zip"

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
}

skins = ["skins_12489", "skins_10001"]
# skins = ["skins_12489"]
# skins = ["skins_10001"]

def svnGetCurVersion(path):
  return pysvn.Client().info(path).commit_revision.number

def svnUp(path):
  pysvn.Client().update(path)

def svnLog(path,start,end):
  ret = pysvn.Client().log(path,revision_start=pysvn.Revision( pysvn.opt_revision_kind.number, start),revision_end=pysvn.Revision( pysvn.opt_revision_kind.number, end))
  for k in ret:
    print(k.message)

def copy_res():
    if os.path.exists(mypath):
        shutil.rmtree(mypath)
    if os.path.exists(outpath):
        shutil.rmtree(outpath)
    bat_diff = os.path.join(Path,'diffolder.bat')
    os.system(bat_diff)

def generate_pub():
    for tempfile in os.listdir(outpath):
        tempvalue = names.get(tempfile, -1)
        if tempvalue != -1:
            temp_child_dir = os.path.join(mypath, tempfile)
            print(os.path.join(outpath, tempfile),temp_child_dir)
            
            if tempvalue == majorVer or tempvalue == "_19_0.zip":
                shutil.copytree(os.path.join(pathSVN, tempfile),temp_child_dir)
            else:
                shutil.copytree(os.path.join(outpath, tempfile),temp_child_dir)

            temp_version_file = os.path.join(temp_child_dir, "version.json")
            # assert(os.path.isfile(temp_version_file), "version file is not exist")

            if os.path.isfile(temp_version_file):
                vjson = json.loads(open(temp_version_file).read())
                game_name = vjson["game_name"]
                major = vjson["major"] 
                minor = vjson["minor"] 
                zip_name = '%s%s' %(tempfile, tempvalue)
                version_name = '%s_%s_%s.zip' %(game_name, major, minor)
                if zip_name != version_name:
                    print("-----------version number and zip number is different!!!--------")
                    print("zip_version :" + zip_name)
                    print("version.json:" + version_name)
                    print("----------------------------------------------------------------")
                    return True
            else:
                print("===========version.json file is not exist=========")
                return True

#shutil.copytree dst_path目录已经存在时拷贝会报错
def my_copy_tree(src_path, dst_path):
    if not os.path.exists(dst_path):
        os.makedirs(dst_path)

    if os.path.exists(src_path):        
        for node_name in os.listdir(src_path):
            full_path = os.path.join(src_path, node_name)
            if os.path.isfile(full_path):
                shutil.copy(full_path, os.path.join(dst_path, node_name))
            else:
                my_copy_tree(full_path, os.path.join(dst_path, node_name))
    else:
        print(src_path+" is not exist!")

#生成皮的pub下对应文件夹，且该方法必须在generate_pub后调用
#以确保主线的更改以拷到pub，方便之后的皮的覆盖
def generate_pub_skin():
    #修复换皮这边没有改动但主皮肤有改动时换皮包不能生成问题
    for valSkin in skins:
        skinDir = os.path.join(outpath, valSkin)
        if not os.path.exists(skinDir):
            os.makedirs(skinDir)
            main_hall_dir = os.path.join(outpath, "hall")
            if os.path.exists(main_hall_dir):
                skin_hall_dir = os.path.join(skinDir, "hall")
                my_copy_tree(main_hall_dir, skin_hall_dir)

    for tmpskin in os.listdir(outpath):
        if tmpskin in skins :
            print("skin_dir:"+tmpskin) 
            for tempfile in os.listdir(os.path.join(outpath,tmpskin)):
                tempvalue = names.get(tempfile, -1)
                if tempvalue != -1:
                    skin_channel = tmpskin.replace("skins", "")
                    temp_main_child_dir = os.path.join(mypath, tempfile)
                    temp_child_dir = os.path.join(os.path.join(mypath, tmpskin), tempfile)#os.path.join(mypath, tempfile+skin_channel)
                    my_copy_tree(temp_main_child_dir, temp_child_dir)
                    print(os.path.join(outpath, tempfile),temp_child_dir)
                    
                    if tempvalue == majorVer:
                        my_copy_tree(os.path.join(os.path.join(pathSVN, tmpskin),tempfile),temp_child_dir)
                    else:
                        my_copy_tree(os.path.join(os.path.join(outpath, tmpskin),tempfile),temp_child_dir)

                    temp_version_file = os.path.join(temp_child_dir, "version.json")
                    # assert(os.path.isfile(temp_version_file), "version file is not exist")

                    if os.path.isfile(temp_version_file):
                        vjson = json.loads(open(temp_version_file).read())
                        game_name = vjson["game_name"]
                        major = vjson["major"] 
                        minor = vjson["minor"] 
                        zip_name = '%s%s' %(tempfile, tempvalue)
                        version_name = '%s_%s_%s.zip' %(game_name, major, minor)
                        if zip_name != version_name:
                            print("-----------version number and zip number is different!!!--------")
                            print("zip_version :" + zip_name)
                            print("version.json:" + version_name)
                            print("----------------------------------------------------------------")
                            return True
                    else:
                        print("===========version.json file is not exist=========")
                        return True

def add_svn_file():
    hall_script_dir = os.path.join(mypath, "hall\script")
    if os.path.isdir(hall_script_dir):
        svn_file = os.path.join(hall_script_dir, "svn.lua") 
        with open(svn_file, 'w') as f:
            f.write('return "svn   {0}" '.format(svnVerB))

def encrypt_files():
    if os.path.isdir(Path):
        bat = os.path.join(Path,'encrypt_game.bat');
    if os.path.isfile(bat):
        print(mypath)
        for tempfile in os.listdir(mypath):
            print(tempfile)
            if os.path.isdir(os.path.join(mypath,tempfile)):
                os.system(bat+" "+tempfile);

def ZipAllLeafFile(Path,tempfile):
    if os.path.isdir(Path):
        model_name = tempfile
        # for tmp_skin in skins:
        #     skin_channel = tmp_skin.replace("skins", "")
        #     if skin_channel in model_name:
        #         model_name = model_name.replace(skin_channel, "")

        tempvalue = names.get(model_name, -1)
        if tempvalue != -1:
            FileCtl = zipfile.ZipFile(tempfile + tempvalue, 'w', zipfile.ZIP_DEFLATED)
            os.chdir(Path)
            for file in os.listdir('.'):
                FileCtl.write(file)
                if os.path.isdir(file):
                    # ZipAllLeafFile(FileCtl,file)
                    for dirpath, dirnames, filenames in os.walk(os.path.join('.', file)):
                        for filename in filenames:
                            FileCtl.write(os.path.join(dirpath, filename))

            FileCtl.close()
            os.chdir('..')

def generate_zips():
    for tempfile in os.listdir(mypath):
        os.chdir(mypath)
        if os.path.isdir(os.path.join(mypath, tempfile)):
            is_skin_dir = False
            for tmp_skin in skins:
                if tmp_skin in tempfile:
                    is_skin_dir = True
            

            if is_skin_dir:
                for tmpdir in os.listdir(os.path.join(mypath, tempfile)):
                    os.chdir(os.path.join(mypath, tempfile))
                    ZipAllLeafFile(os.path.join(os.path.join(mypath, tempfile), tmpdir),tmpdir)
            else:
                ZipAllLeafFile(os.path.join(mypath, tempfile),tempfile)
            
    for tempfile in os.listdir(mypath):
        os.chdir(mypath)
        if os.path.isdir(os.path.join(mypath, tempfile)):
            is_skin_dir = False
            for tmp_skin in skins:
                if tmp_skin in tempfile:
                    is_skin_dir = True

            if is_skin_dir:
                for tmpdir in os.listdir(os.path.join(mypath, tempfile)):
                    os.chdir(os.path.join(mypath, tempfile))
                    if os.path.isdir(os.path.join(os.path.join(mypath, tempfile), tmpdir)):
                        shutil.rmtree(os.path.join(os.path.join(mypath, tempfile), tmpdir))
            else:
                shutil.rmtree(os.path.join(mypath, tempfile))

def generate_cdn_list():
    filename = mypath +"\cdn_list.lua"
    pre_str = "https://www.dafuhao-ol.com/JspUpDownTest/myfiles/"
    with open(filename, 'w') as f:    
        for key, value in names.items():
            cdn_path = pre_str + key + value + "\n"
            f.write(cdn_path)

if __name__ == '__main__':
    os.chdir("C:\Workspace\pub_formal")    
    pathSVN = os.path.join(os.getcwd(),"dev")
    svnVerA = svnGetCurVersion(pathSVN)
    svnUp(pathSVN)
    svnVerB = svnGetCurVersion(pathSVN)
    print(svnVerA, svnVerB)    

    mypath = os.path.join(os.getcwd(),"pub")
    outpath = os.path.join(os.getcwd(),"out")
    Path = os.getcwd()
    copy_res()

    is_error = generate_pub()
    if is_error :
        os.system("pause")
    else:
        is_error = generate_pub_skin() 
        if is_error:
            os.system("pause") 
        if os.path.exists(mypath):        
            add_svn_file()
            encrypt_files()
            generate_zips()
            print "success"
            os.system("pause")
        else:
            print("no [pub] dir!!!")

