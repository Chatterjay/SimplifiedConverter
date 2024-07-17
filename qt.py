import os
import opencc
import sys

def convert_text(text):
    converter = opencc.OpenCC('t2s')
    return converter.convert(text)

def process_item(path, is_file):
    directory = os.path.dirname(path)
    base_name = os.path.basename(path)
    converted_dir = os.path.join(directory, '转换后的文件')
    os.makedirs(converted_dir, exist_ok=True)
    
    if is_file:
        # 处理单个文件
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()
        converted_content = convert_text(content)
        converted_file_path = os.path.join(converted_dir, base_name)
        with open(converted_file_path, 'w', encoding='utf-8') as file:
            file.write(converted_content)
        print(f"转换后的文件已保存到 {converted_file_path}")
    else:
        # 处理文件夹中的所有文件
        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)
            if os.path.isfile(file_path):
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                converted_content = convert_text(content)
                converted_file_path = os.path.join(converted_dir, filename)
                with open(converted_file_path, 'w', encoding='utf-8') as file:
                    file.write(converted_content)
                print(f"转换后的文件已保存到 {converted_file_path}")

def main():
    if len(sys.argv) < 2:
        print("用法：将文件或文件夹拖放到此可执行文件上。")
        return
    
    input_path = sys.argv[1]
    if os.path.isdir(input_path):
        process_item(input_path, False)
    elif os.path.isfile(input_path):
        process_item(input_path, True)
    else:
        print("提供的路径不是文件或目录。")

if __name__ == "__main__":
    main()