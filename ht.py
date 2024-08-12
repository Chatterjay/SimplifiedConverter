import os
import opencc
import sys


def convert_text_in_file(input_file_path, output_file_path, conversion_type):
    """根据指定的转换类型将文件内容转换并保存到新文件中。"""
    converter = opencc.OpenCC(conversion_type)  # 初始化OpenCC转换器

    with open(input_file_path, 'r', encoding='utf-8') as file:
        content = file.read()  # 读取文件内容

    converted_content = converter.convert(content)  # 转换内容

    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(converted_content)  # 写入转换后的内容


def rename_item(original_path):
    """重命名文件或文件夹，并返回新路径和原始名称。"""
    original_name = os.path.basename(original_path)
    new_name = f"{original_name}_{original_name[0]}"
    new_path = os.path.join(os.path.dirname(original_path), new_name)

    os.rename(original_path, new_path)  # 重命名文件或文件夹
    print(f"源文件或文件夹 '{original_name}' 已重命名为 '{new_name}'")

    return new_path, original_name


def handle_path_input(path, conversion_type):
    """处理用户输入的路径，去除多余的引号，并检查路径是否存在。"""
    path = path.strip('"')  # 去除路径前后的双引号

    if not os.path.exists(path):
        print(f"指定的路径 '{path}' 不存在。")
        return

    process_path(path, conversion_type)


def process_path(path, conversion_type):
    """根据路径类型（文件或文件夹）处理相应内容。"""
    new_path, original_name = rename_item(path)
    base_path = os.path.dirname(new_path)

    if os.path.isfile(new_path):
        # 处理单个文件
        output_file_path = os.path.join(base_path, original_name)
        convert_text_in_file(new_path, output_file_path, conversion_type)
        print(f"文件 '{original_name}' 已转换并保存为 '{output_file_path}'")
    elif os.path.isdir(new_path):
        # 处理文件夹
        output_dir = os.path.join(base_path, original_name)
        os.makedirs(output_dir, exist_ok=True)
        process_directory(new_path, output_dir, conversion_type)


def process_directory(directory_path, output_dir, conversion_type):
    """处理文件夹中的每个文件，将其内容转换并保存到新文件夹中。"""
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):
            output_file_path = os.path.join(output_dir, filename)
            convert_text_in_file(file_path, output_file_path, conversion_type)
            print(f"文件 '{filename}' 已转换并保存到 '{output_dir}'")


def main():
    if len(sys.argv) < 2:
        print("用法：将文件或文件夹拖放到此可执行文件上。")
        return

    input_path = sys.argv[1]
    conversion_type = 's2t'

    if os.path.isdir(input_path):
        process_path(input_path, conversion_type)
    elif os.path.isfile(input_path):
        process_path(input_path, conversion_type)
    else:
        print("提供的路径不是文件或目录。")


if __name__ == "__main__":
    main()
