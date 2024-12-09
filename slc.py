import os
import opencc
import argparse
from pathlib import Path
import logging

# 设置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def convert_text(content, conversion_type):
    """根据指定的转换类型将文本内容进行转换。"""
    try:
        converter = opencc.OpenCC(conversion_type)
        return converter.convert(content)
    except Exception as e:
        logging.error(f"转换过程中出现错误: {e}")
        raise

def save_file(output_path, content):
    """将内容保存到指定路径。"""
    try:
        with output_path.open('w', encoding='utf-8') as file:
            file.write(content)
    except IOError as e:
        logging.error(f"文件读写错误: {e}")
        raise

def get_unique_output_dir(output_parent, item_name, key):
    """获取唯一的输出目录，避免同名冲突。"""
    output_dir = output_parent / item_name
    counter = 1
    while output_dir.exists():
        output_dir = output_parent / f"{item_name}_{key}_{counter}"
        counter += 1
    return output_dir

def get_new_name(original_name, preserve_source):
    """根据是否保留源文件来获取新名称。"""
    if preserve_source:
        name, ext = os.path.splitext(original_name)
        return f"{name}_converted{ext}"
    return original_name

def process_file(file_path, output_path, conversion_type):
    """处理单个文件。"""
    try:
        with file_path.open('r', encoding='utf-8') as file:
            content = file.read()
        converted_content = convert_text(content, conversion_type)
        save_file(output_path, converted_content)
        logging.info(f"文件 '{file_path}' 已转换并保存为 '{output_path}'")
    except Exception as e:
        logging.error(f"处理文件 '{file_path}' 时出现错误: {e}")

def process_directory(directory_path, output_parent, conversion_type, key, preserve_source):
    """递归处理文件夹中的每个文件。"""
    output_dir = get_unique_output_dir(output_parent, directory_path.name, key)
    output_dir.mkdir(parents=True, exist_ok=True)
    for subitem in directory_path.iterdir():
        if subitem.is_dir():
            process_directory(subitem, output_dir, conversion_type, key, preserve_source)
        else:
            new_output_path = output_dir / get_new_name(subitem.name, preserve_source)
            process_file(subitem, new_output_path, conversion_type)

def process_item(item, output_parent, conversion_type, key, preserve_source):
    """处理单个文件或递归处理文件夹中的每个文件。"""
    if item.is_dir():
        process_directory(item, output_parent, conversion_type, key, preserve_source)
    else:
        new_output_path = output_parent / get_new_name(item.name, preserve_source)
        process_file(item, new_output_path, conversion_type)

def setup_arg_parser():
    """设置命令行参数解析器。"""
    parser = argparse.ArgumentParser(description="转换文本文件中的繁简体中文")
    parser.add_argument("path", nargs='?', type=Path,
                        help="输入文件或文件夹的路径 (可选)")
    conversion_group = parser.add_mutually_exclusive_group()
    conversion_group.add_argument("-cn", "--simplified", dest="conversion_type",
                                  action="store_const", const="t2s", default="t2s",
                                  help="转换为简体中文 (默认)")
    conversion_group.add_argument("-hk", "--traditional", dest="conversion_type",
                                  action="store_const", const="s2t",
                                  help="转换为繁体中文")
    parser.add_argument("-o", "--output", type=Path, help="指定输出文件或文件夹路径")
    parser.add_argument("-f", "--default-file", type=Path, dest="default_file",
                        help="选择文件的默认文件路径")
    parser.add_argument("-d", "--default-folder", type=Path, dest="default_folder",
                        help="选择文件夹的默认文件夹路径")
    parser.add_argument("-p", "--preserve-source", action="store_true",
                        help="不对源文件操作而是新建同名但是有特殊标识的文件")
    parser.add_argument("-k", "--key", type=str, default="converted",
                        help="指定输出目录的键，默认为 'converted'")
    return parser

def determine_input_path(args):
    """根据提供的参数确定输入路径。"""
    path = args.path
    if not path:
        if args.default_file:
            path = args.default_file
        elif args.default_folder:
            path = args.default_folder
        else:
            logging.error("请提供有效的文件或文件夹路径，或设置默认文件路径或默认文件夹路径。")
            return None

    if not path.exists():
        logging.error(f"路径 '{path}' 不存在。")
        return None

    return path

def determine_output_parent(path, args):
    """根据提供的参数确定输出父路径。"""
    if args.output:
        output_parent = args.output
    elif args.preserve_source:
        output_parent = path.parent / args.key
    else:
        # 默认在同级目录下创建新文件夹
        output_parent = path.parent / f"{path.name}_{args.key}"

    if path.is_file():
        output_parent = output_parent.parent  # 如果是文件，输出路径应为文件的上级目录

    output_parent.mkdir(parents=True, exist_ok=True)
    return output_parent

def main():
    parser = setup_arg_parser()
    args = parser.parse_args()

    path = determine_input_path(args)
    if path is None:
        return

    output_parent = determine_output_parent(path, args)
    if output_parent is None:
        return

    try:
        process_item(path, output_parent, args.conversion_type, args.key, args.preserve_source)
    except Exception as e:
        logging.error(f"处理过程中出现错误: {e}")

if __name__ == "__main__":
    main()
