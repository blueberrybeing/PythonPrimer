# -*- coding: utf-8 -*-
# zip.py
import sys
import shutil
import zipfile
import os
import requests
import pysvn
import json
import re 
import FileUtil

pathSVN = ""
svnVerA = "" 
svnVerB = ""
mypath = ""
outpath = ""
Path = ""

names = {
    # 'hall'              :'_24_2.zip',
    # 'common'            :'_24_1.zip',
    # 'platform_default'  :'_24_1.zip',

    # 'festivity55'       :'_21_9.zip',
    # # 'zhd_bsmz'          :'_19_1.zip',
    # # 'zhd_jfjs'          :'_20_4.zip',
    # 'guide'             :'_24_1.zip',
    # 'card'              :'_24_1.zip',
    # 'activityNewUser'   :'_24_0.zip',

    # 'common_jj'         :'_19_8.zip',
    # 'fkzww'             :'_18_8.zip',
    # 'xxl'               :'_21_9.zip',
    # # 'shbz'              :'_21_9.zip',
    # 'jzsc'              :'_22_3.zip',

    # 'common_qp'         :'_18_12.zip',
    # 'fkjh'              :'_18_15.zip',
    # 'ddz'               :'_24_1.zip',
    # # 'sgzb'              :'_18_12.zip',
    # 'fkmj'              :'_19_10.zip',

    # 'paths'             :'_2_0.zip',
    # 'xfish'             :'_24_2.zip',
    # 'xmxxl'             :'_24_1.zip',
    # 'hwby'              :'_24_0.zip',

    # 'common_by'         :'_25_0.zip',
    # 'shby'              :'_23_0.zip',
    # 'fishing'           :'_22_0.zip',
    # # 'common_by_spirit'  :'_1_3.zip',
    # 'common_by_game'    :'_3_0.zip',
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

skins = ["skins_12489", "skins_10001","skins_10002","skins_10003","skins_10004","skins_10005"]
# skins = ["skins_10002"]
# skins = ["skins_10003"]
# skins = ["skins_10005"]
# skins=[]
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

# 是否为大版本，需要更新整包
# _xx_0.zip 为大版本，否则不是大版本
def is_major_ver(versionVal):
    verPart = versionVal.split(".")
    numPart = verPart[0].split("_")
    if numPart[len(numPart)-1] == "0":
        return True

    return False

#删除协议注释文件
def remove_protocol_explain():
    my_protocal_scheme = os.path.join(mypath, "common/script/config/my_protocal_schemas.lua")    
    if os.path.isfile(my_protocal_scheme):
        FileUtil.replace_file_content(my_protocal_scheme, {",\s*\"(rem|explain)\"\s*:\s*\"[^\"]*\"": ""}, re.I)

def generate_pub():
    for tempfile in os.listdir(outpath):
        tempvalue = names.get(tempfile, -1)
        if tempvalue != -1:
            temp_child_dir = os.path.join(mypath, tempfile)
            print(os.path.join(outpath, tempfile),temp_child_dir)
            
            if is_major_ver(tempvalue):
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

def rm_fkby_sub_modules():
    fkby_path = os.path.join(mypath, "fkby")
    if not os.path.exists(fkby_path):
        return 
    for tempfile in os.listdir(fkby_path):
        if os.path.isdir(os.path.join(fkby_path, tempfile)) and tempfile != "res" and tempfile != "script":
            shutil.rmtree(os.path.join(fkby_path, tempfile))

def generate_pub_fkby_sub_modules():
    outpath_fkby = os.path.join(outpath,"fkby")
    src_dir_fkby = os.path.join(pathSVN,"fkby")

    for tempfile in os.listdir(outpath_fkby):
        tempvalue = names.get(tempfile, -1)
        if tempvalue != -1:
            temp_child_dir = os.path.join(mypath, tempfile)
            print("copy files to pub:" + temp_child_dir)
            
            if is_major_ver(tempvalue):
                shutil.copytree(os.path.join(src_dir_fkby, tempfile),temp_child_dir)
            else:
                shutil.copytree(os.path.join(outpath_fkby, tempfile),temp_child_dir)

            temp_version_file = os.path.join(temp_child_dir, "version.json")
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

# 换皮这边没有改动的情况下拷贝加入有效性检测
# 有效性检测规则：1、不允许皮肤分支有自己的独立素材时被主皮肤同名覆盖（因为这个会导致杂揉）
#                    出现这种情况以错误级别处理
#                 2、新增资源，以警告级别提示（需要确认能否使用）
def skin_dir_copy_tree_with_check(src_path, dst_path, skin_dir):
    if not os.path.exists(dst_path):
        os.makedirs(dst_path)

    if os.path.exists(src_path):        
        for node_name in os.listdir(src_path):
            full_path = os.path.join(src_path, node_name)
            full_dev_skin_path = os.path.join(skin_dir, node_name)
            if os.path.isfile(full_path):
                if os.path.exists(full_dev_skin_path):
                    # print("")
                    print("XX ERROR XX :skin own this file("+full_dev_skin_path+"),but replace by main")
                    # shutil.copy(full_path, os.path.join(dst_path, node_name))
                else:
                    findPos = full_path.find("\\res\\")
                    # if findPos != -1:
                        # print("!!! WARN !!!:skin no this file("+full_path+"), is main new add file!")
                    shutil.copy(full_path, os.path.join(dst_path, node_name))
            else:
                skin_dir_copy_tree_with_check(full_path, os.path.join(dst_path, node_name), os.path.join(skin_dir, node_name))
    else:
        print(src_path+" is not exist!")

#换皮这边没有改动但主皮肤有改动时
def skin_no_change_cp(skin_name, model_name):
    skinDir = os.path.join(outpath, skin_name)
    skin_model_dir = os.path.join(skinDir, model_name)
    if not os.path.exists(skin_model_dir):
        main_model_dir = os.path.join(outpath, model_name)
        if os.path.exists(main_model_dir):
            skin_dev_dir = os.path.join(pathSVN, skin_name)
            skin_dev_dir = os.path.join(skin_dev_dir, model_name)
            skin_dir_copy_tree_with_check(main_model_dir, skin_model_dir, skin_dev_dir)

def main_skin_merge(skin_name, model_name):
    skin_dev_dir = os.path.join(pathSVN, skin_name)
    skin_dev_dir = os.path.join(skin_dev_dir, model_name)

    # for tempfile in os.listdir(os.path.join(outpath,skin_name)):
    tempfile = model_name
    tempvalue = names.get(model_name, -1)
    if tempvalue != -1:
        skin_channel = skin_name.replace("skins", "")
        temp_main_child_dir = os.path.join(mypath, tempfile)
        temp_child_dir = os.path.join(os.path.join(mypath, skin_name), tempfile)#os.path.join(mypath, tempfile+skin_channel)
        skin_dir_copy_tree_with_check(temp_main_child_dir, temp_child_dir, skin_dev_dir)
        print(os.path.join(outpath, tempfile),temp_child_dir)
        
        if is_major_ver(tempvalue):
            my_copy_tree(os.path.join(os.path.join(pathSVN, skin_name),tempfile), temp_child_dir)
        else:
            my_copy_tree(os.path.join(os.path.join(outpath, skin_name),tempfile), temp_child_dir)

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
            # return True

#生成皮的pub下对应文件夹，且该方法必须在generate_pub后调用
#以确保主线的更改以拷到pub，方便之后的皮的覆盖
def generate_pub_skin():
    #修复换皮这边没有改动但主皮肤有改动时换皮包不能生成问题
    for valSkin in skins:
        skin_no_change_cp(valSkin, "hall")
        skin_no_change_cp(valSkin, "platform_default")

    for tmpskin in os.listdir(outpath):
        if tmpskin in skins :
            print("skin_dir:" + tmpskin) 
            main_skin_merge(tmpskin, "hall")
            main_skin_merge(tmpskin, "platform_default")


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
    # svnVerA = svnGetCurVersion(pathSVN)
    # svnUp(pathSVN)
    # svnVerB = svnGetCurVersion(pathSVN)
    # print(svnVerA, svnVerB)    

    mypath = os.path.join(os.getcwd(),"pub")
    outpath = os.path.join(os.getcwd(),"out")
    Path = os.getcwd()
    copy_res()

    is_error = generate_pub()
    rm_fkby_sub_modules()
    is_error_fkby_sub = generate_pub_fkby_sub_modules()
    
    if is_error or is_error_fkby_sub :
        os.system("pause")
    else:
        is_error = generate_pub_skin() 
        if is_error:
            os.system("pause") 
        if os.path.exists(mypath):        
            add_svn_file()
            remove_protocol_explain()
            encrypt_files()
            generate_zips()
            print "success"
            os.system("pause")
        else:
            print("no [pub] dir!!!")

