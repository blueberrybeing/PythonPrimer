import os
import sys
import hashlib
import shutil
import walker

def md5file(filename):
    with open(filename, "rb") as file:
        return hashlib.md5(file.read()).hexdigest()

def copyfile(in1_rel_filename, out_rel_filename, rel_path):
    out_rel = os.path.join(out, rel_path)
    if not os.path.exists(out_rel):
        os.makedirs(out_rel)
    shutil.copy(in1_rel_filename, out_rel_filename)
    
def node_process(root_path, rel_path, node_name, node_type):
    #print(root_path, rel_path, node_name, node_type)
    if node_type == "file":
        in1_rel_filename = os.path.join(in1, rel_path, node_name)
        in2_rel_filename = os.path.join(in2, rel_path, node_name)
        out_rel_filename = os.path.join(out, rel_path, node_name)
        if os.path.exists(in2_rel_filename):
            if md5file(in1_rel_filename) == md5file(in2_rel_filename):
                pass
            else:
                copyfile(in1_rel_filename, out_rel_filename, rel_path)
                print("mod {0}".format(os.path.join(rel_path, node_name)))
                if node_name.endswith(".png"):
                    relatefile = node_name.replace(".png",".plist")
                    in1_rel_relatefile = os.path.join(in1, rel_path, relatefile)
                    out_rel_relatefile = os.path.join(out, rel_path, relatefile)
                    if os.path.exists(in1_rel_relatefile):
                        copyfile(in1_rel_relatefile, out_rel_relatefile, rel_path)
                        print("relate {0}".format(os.path.join(rel_path, relatefile)))
                if node_name.endswith(".plist"):
                    relatefile = node_name.replace(".plist",".png")
                    in1_rel_relatefile = os.path.join(in1, rel_path, relatefile)
                    out_rel_relatefile = os.path.join(out, rel_path, relatefile)
                    if os.path.exists(in1_rel_relatefile):
                        copyfile(in1_rel_relatefile, out_rel_relatefile, rel_path)
                        print("relate {0}".format(os.path.join(rel_path, relatefile)))      
        else:
            copyfile(in1_rel_filename, out_rel_filename, rel_path)
            print("add {0}".format(os.path.join(rel_path, node_name)))
    
def node_filter(root_path, rel_path, node_name, node_type):
    if not '.svn' in node_name and not '.idea' in node_name:
        node_process(root_path, rel_path, node_name, node_type)

if __name__ == "__main__":
    in1 = "dev"
    in2 = "base"
    out = "out"
    print in1,in2,out
    if os.path.exists(out):
        shutil.rmtree(out)
        os.makedirs(out)
                    
    walker.walk(in1, "", node_filter)
