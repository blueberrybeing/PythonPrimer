# -*- coding: utf-8 -*-
import shutil
import os
import sys
import json
import re
def foreach_dir(root_path, rel_path, process):
    root_rel_path = os.path.join(root_path, rel_path)
    if not os.path.exists(root_rel_path):
        return
    process(root_path, rel_path, "", "folder")

    node_names = os.listdir(root_rel_path)

    for node_name in node_names:
        #print("mmmmm==:",node_name)
        root_rel_node_name = os.path.join(root_rel_path, node_name)

        if os.path.isfile(root_rel_node_name):
            node_type = "file"
            process(root_path, rel_path, node_name, node_type)
        if os.path.isdir(root_rel_node_name):
            node_type = "folder"
        
        if node_type == "folder":
            foreach_dir(root_path, os.path.join(rel_path, node_name), process)
            
#先序遍历#
def preorder_foreach_dir(root_path, rel_path, process):
    root_rel_path = os.path.join(root_path, rel_path)
    if not os.path.exists(root_rel_path):
        return
    node_names = os.listdir(root_rel_path)
    for node_name in node_names:
        root_rel_node_name = os.path.join(root_rel_path, node_name)
        if os.path.isdir(root_rel_node_name):
            preorder_foreach_dir(root_path, os.path.join(rel_path, node_name), process)
            process(root_path, rel_path, node_name, "folder")
    for node_name in node_names:
        root_rel_node_name = os.path.join(root_rel_path, node_name)
        if os.path.isfile(root_rel_node_name):
            process(root_path, rel_path, node_name, "file")

   

def read_file(full_path):

    file=open(full_path,"rb")
    if not file or file.closed:
        print("read_file: open file fail:"+full_path)
        return

    content=file.read()   
    file.close()
    return content

def write_file(full_path,content):
    with open(full_path,"wb") as write_f:
        write_f.write(content)

#sb python...S
def copy_all(src,dst):
    def process(root_path, rel_path, node_name, node_type):
        full_path=os.path.join(root_path,rel_path,node_name)
        dst_path=os.path.join(dst,rel_path)
        if node_type=="folder":
            if not os.path.exists(dst_path):
                os.makedirs(dst_path)
            return
        ###file###
       
        shutil.copyfile(full_path,os.path.join(dst_path,node_name))
        
    foreach_dir(src, "", process)

#如果传入正则表达式，则清空文件夹时会保留与except_pattern匹配的项#
def clear_dir(root_path,except_pattern=None):
    #root_rel_path = root_path
    if not os.path.exists(root_path):
        return

    node_names = os.listdir(root_path)
    for node_name in node_names:
        root_rel_node_name = os.path.join(root_path, node_name)
        if os.path.isfile(root_rel_node_name):
            if not except_pattern or not re.search(except_pattern,root_rel_node_name):
                os.remove(root_rel_node_name)

        if os.path.isdir(root_rel_node_name) and not (except_pattern and re.search(except_pattern,root_rel_node_name)):
            clear_dir(root_rel_node_name,except_pattern)

    if len(os.listdir(root_path))==0:
        shutil.rmtree(root_path)      

def replace_contents(content,content_patterns_map,pattern_flag):
    for kv in content_patterns_map.items():
        content=re.sub(kv[0],kv[1],content,0,pattern_flag)
    return content

def replace_file_content(full_path,content_patterns_map,pattern_flag,checker=None):
    content1=read_file(full_path)
    if not checker or (checker and checker(content1)):
        content2=replace_contents(content1,content_patterns_map,pattern_flag)
        if content1!=content2:
            write_file(full_path,content2)

#在指定的目录下对满足条件的所有文件的文件内容执行正则表达式替换#
#root_dir:目录路径
#file_name_pattern:文件名正则表达式条件#
#content_patterns_map：对每个文件执行一系列是替换操作#
#pattern_flag:re.IGNORECASE
def replace_file_contents(root_dir,file_name_pattern,content_patterns_map,pattern_flag=re.IGNORECASE,checker=None,ignore_list=None):
    def process(root_path, rel_path, node_name, node_type):
        if node_type!="file" or not re.search(file_name_pattern,node_name,pattern_flag):
           return
        full_path=os.path.join(root_path,rel_path,node_name)
        if ignore_list != None and (node_name in ignore_list):
            print("!!!Ignore file:",node_name)
            return
        replace_file_content(full_path,content_patterns_map,pattern_flag,checker)
    foreach_dir(root_dir,"",process)    


def replace_file_names(root_dir,file_name_pattern,content_patterns_map,pattern_flag):
    def process(root_path, rel_path, node_name, node_type):
        if node_type!="file" or not re.search(file_name_pattern,node_name,pattern_flag):
           return
        full_path=os.path.join(root_path,rel_path,node_name)
        full_relative_path1=os.path.join(rel_path,node_name)
        full_relative_path2=replace_contents(full_relative_path1,content_patterns_map,pattern_flag)

        if full_relative_path1!=full_relative_path2:
            full_path_new_name=os.path.join(root_path,full_relative_path2)
            os.rename(full_path,full_path_new_name) 

    foreach_dir(root_dir,"",process)  