import os
import zipfile


def zip_folder_with_password(folder_path, output_path):
    """
    将指定文件夹压缩为加密的 ZIP 文件

    Args:
        folder_path (str): 要压缩的文件夹路径
        output_path (str): 输出的 ZIP 文件路径
    """
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zip_file.write(file_path, os.path.relpath(file_path, folder_path))


def unzip_file_with_password(zip_path, output_path):
    """
    解压缩加密的 ZIP 文件

    Args:
        zip_path (str): 要解压缩的 ZIP 文件路径
        output_path (str): 解压缩文件的输出路径
    """
    with zipfile.ZipFile(zip_path, 'r') as zip_file:
        zip_file.extractall(output_path)


# 示例用法
folder_to_zip = r'E:\tmp\test'
zip_file_path = r'E:\tmp\output.zip'

# 压缩文件夹并加密
zip_folder_with_password(folder_to_zip, zip_file_path)

# 解压缩加密的 ZIP 文件
output_folder = r'E:\tmp\test1'
# unzip_file_with_password(zip_file_path, output_folder, de_password="password")