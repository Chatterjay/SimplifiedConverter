import os
import opencc
import argparse
from pathlib import Path


def convert_and_save(input_path, output_path, conversion_type):
    """根据指定的转换类型将文本内容转换并保存到输出路径。"""
    converter = opencc.OpenCC(conversion_type)
    with input_path.open('r', encoding='utf-8') as file:
        content = file.read()

    converted_content = converter.convert(content)

    with output_path.open('w', encoding='utf-8') as file:
        file.write(converted_content)


def process_item(item, output_parent, conversion_type, preserve_source=False):
    """处理单个文件或递归处理文件夹中的每个文件。"""
    if item.is_dir():
        output_dir = output_parent / item.name
        output_dir.mkdir(parents=True, exist_ok=True)
        for subitem in item.iterdir():
            process_item(subitem, output_dir, conversion_type, preserve_source)
    else:
        new_output_path = output_parent / get_new_name(item.name, preserve_source)
        convert_and_save(item, new_output_path, conversion_type)
        print(f"文件 '{item}' 已转换并保存为 '{new_output_path}'")


def get_new_name(original_name, preserve_source=False):
    """根据是否保留源文件来获取新名称。"""
    if preserve_source:
        name, ext = os.path.splitext(original_name)
        return f"{name}_converted{ext}"
    return original_name


def main():
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
    parser.add_argument("-d", "--default-folder", type=Path, dest="default_folder",
                        help="选择文件或者文件夹的默认文件夹")
    parser.add_argument("-p", "--preserve-source", action="store_true",
                        help="不对源文件操作而是新建同名但是有特殊标识的文件")

    args = parser.parse_args()

    path = args.path or args.default_folder
    if not path or not path.exists():
        print("请提供有效的文件或文件夹路径，或设置默认文件夹。")
        return

    # 确定输出路径，默认情况下在同一目录下创建新文件
    output_parent = args.output or (path.parent if args.preserve_source else path)

    try:
        process_item(path, output_parent, args.conversion_type, args.preserve_source)
    except Exception as e:
        print(f"处理过程中出现错误: {e}")


if __name__ == "__main__":
    main()