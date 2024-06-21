import io
import os
import tempfile
import zipfile
from typing import Tuple, List


def generate_playbook_paths(zip_file_object: io.BytesIO) -> Tuple[str, str, str, str, List[str]]:
    entry_file= "site.yml"
    inventory_file = "inventories" + str(os.sep) + "inventory.ini"
    global_var_file = "global.yml"

    temp_dir = tempfile.TemporaryDirectory()
    zip_dir_name = os.listdir(temp_dir)[0]
    playbook_dir = os.path.join(temp_dir, zip_dir_name)
    role_names = [os.listdir(playbook_dir)]
    entry_file_path = os.path.join(playbook_dir, entry_file)
    inventory_file_path = os.path.join(playbook_dir, inventory_file)
    global_var_file_path = os.path.join(playbook_dir, global_var_file)

    with zipfile.ZipFile(zip_file_object, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)

    return temp_dir, inventory_file_path, entry_file_path, global_var_file_path, role_names


