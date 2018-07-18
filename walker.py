import os

def print_process(root_path, rel_path, node_name, node_type):
        print("root_path={0}, rel_path={1}, node_name={2}, node_type={3}".format(root_path,rel_path,node_name,node_type))
    
def walk(root_path, rel_path, process):
    root_rel_path = os.path.join(root_path, rel_path)
    node_names = os.listdir(root_rel_path)

    for node_name in node_names:
        if node_name != ".svn":
            root_rel_node_name = os.path.join(root_rel_path, node_name)

            if os.path.isfile(root_rel_node_name):
                node_type = "file"
            if os.path.isdir(root_rel_node_name):
                node_type = "folder"
            
            process(root_path, rel_path, node_name, node_type)

            if node_type == "folder":
                walk(root_path, os.path.join(rel_path, node_name), process)
