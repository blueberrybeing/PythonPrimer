


import sys
import os, os.path
import shutil
#coding:utf-8


def lstFilesByDir(_dir,_func=None,recursion=True):
    dirs = os.listdir(_dir)
    for item in dirs:
        fullPath = os.path.join(_dir,item)
        if os.path.isdir(fullPath):
            if recursion:
                lstFilesByDir(fullPath,_func,recursion)
        else:
            if _func:
                _func(fullPath)

def funcXXTEA(path1,path2):
    command = ""
    if sys.platform == 'win32':
        command = "call xxtea encrypt god key_file=key {0} {1}".format(path1,path2)
    else:
        command = "./xxtea encrypt god key_file=key {0} {1}".format(path1,path2)
    retCommand = os.system(command)
    if  retCommand != 0:
        raise Exception("error:{0}".format(path1))


def func(path):
    fileName = os.path.basename(path)
    arr = os.path.splitext(fileName)
    fileDir =os.path.dirname(path)
    if len(arr)!=2:
        return
    if arr[1]==".lua":
        funcXXTEA(path,os.path.join(fileDir,arr[0])+".luac")
        os.remove(path)
    elif arr[1]==".png" or arr[1]==".jpg":
        funcXXTEA(path,path)


lstFilesByDir(sys.argv[1],func)


