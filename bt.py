import os
import opencc

def convert_file(input_file_path, output_file_path):
    # 初始化OpenCC转换器
    converter = opencc.OpenCC('t2s')

    # 读取文件内容
    with open(input_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 转换内容
    converted_content = converter.convert(content)

    # 写入转换后的内容
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(converted_content)

def process_item(path):
    # 检查路径是否存在
    if not os.path.exists(path):
        print(f"指定的路径 '{path}' 不存在。")
        return

    # 确定转换后的文件存放目录
    base_path = os.path.dirname(path)
    converted_dir = os.path.join(base_path, 'converted_files')
    os.makedirs(converted_dir, exist_ok=True)

    # 根据路径类型进行处理
    if os.path.isfile(path):
        # 单个文件的处理
        filename = os.path.basename(path)
        convert_file(path, os.path.join(converted_dir, filename))
        print(f"文件 '{filename}' 已转换并保存到 '{converted_dir}'")
    elif os.path.isdir(path):
        # 文件夹的处理
        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)
            if os.path.isfile(file_path):
                convert_file(file_path, os.path.join(converted_dir, filename))
                print(f"文件 '{filename}' 已转换并保存到 '{converted_dir}'")
    else:
        print(f"指定的路径 '{path}' 不是一个文件或目录。")

def main():
    while True:
        path = input("请输入文件或文件夹的路径（输入 'exit' 退出）：")
        if path.lower() == 'exit':
            print("退出程序。")
            break
        process_item(path)

if __name__ == "__main__":
    main()