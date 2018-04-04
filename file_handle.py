import os  
import random
import string

def random_file_name():
    return ''.join(random.sample(string.ascii_letters + string.digits, 8))

file_dict = {}
def traverse(f):
    fs = os.listdir(f)
    for f1 in fs:
        tmp_path = os.path.join(f, f1)
        if not os.path.isdir(tmp_path):
            newname = random_file_name()
            file_dict[f1] = newname
            os.rename(tmp_path, os.path.join(f, newname))
        else:
            traverse(tmp_path)
path = '/Users/hx/Desktop/res_name/res'
traverse(path)

def write_to_lua():
    with open('file_dict.lua', 'w') as f:
        f.write("local file_dict = {\n")
        for key,value in file_dict.items():
            print('key is %s, value is %s' %(key, value))
            temp = key + '=' + value + '\n'
            f.write(temp)
        f.write("}\n")
        f.write("return file_dict\n")

write_to_lua()


# for x in range(100):
#   salt = random_file_name()
#   print(salt)
