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
    # 'hall':'_17_1.zip',
    # 'common':'_18_0.zip',

    # 'bcbm':'_17_0.zip',
    # 'fkszg':'_17_0.zip',
    # 'fruit':'_17_0.zip',
    # 'hhmf':'_17_0.zip',
    # 'jlbd':'_17_0.zip',
    # 'phoenix':'_17_0.zip',
    # 'shz':'_17_0.zip',
    # 'slwh':'_17_0.zip',
    # 'slwh3D':'_17_0.zip',
    # 'xyzb':'_17_0.zip',

    # 'fkjh':'_17_0.zip',
    # 'brnn':'_17_0.zip',
    # 'ddz':'_17_0.zip',
    # 'xydz':'_17_0.zip',
    'sgzb':'_17_0.zip',
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
            if tempvalue == '_18_0.zip' or tempvalue == '_17_0.zip':
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
    os.chdir("C:\Workspace\pubToLine")
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
