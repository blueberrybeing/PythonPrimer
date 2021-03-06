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
    # 'fkby':'_19_0.zip',
}

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
            if tempvalue == '_19_0.zip':
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
        for tempfile in os.listdir(mypath):
            if os.path.isdir(os.path.join(mypath,tempfile)):
                os.system(bat+" "+tempfile);

def ZipAllLeafFile(Path,tempfile):
    if os.path.isdir(Path):
        tempvalue = names.get(tempfile, -1)
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
            ZipAllLeafFile(os.path.join(mypath, tempfile),tempfile)
            
    for tempfile in os.listdir(mypath):
        os.chdir(mypath)
        if os.path.isdir(os.path.join(mypath, tempfile)):
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
        add_svn_file()
        encrypt_files()
        generate_zips()
        print "success"
        os.system("pause")
