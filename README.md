### 化繁为简

#### 使用 `slc.py` 文件进行繁体与简体转换

- **编译器中执行**：在 `slc.py` 编译器中直接执行繁转简和简转繁操作。
- **命令行参数**：
  - `-cn` 或 `--simplified`：转换为简体中文（默认）。
  - `-hk` 或 `--traditional`：转换为繁体中文。
  - `-o` 或 `--output`：指定输出文件或文件夹路径。
  - `-d` 或 `--default-folder`：选择文件或文件夹的默认文件夹。
  - `-p` 或 `--preserve-source`：不对源文件操作，而是新建同名但带有特殊标识的文件。

##### 示例用法

1. **转换单个文件**：
   ```sh
   slc.py -cn input.txt -o output.txt
   ```


2. **转换文件夹中的所有文件**：
   ```sh
   slc.py -cn input_folder -o output_folder
   ```


3. **使用默认文件夹**：
   ```sh
   slc.py -cn -d default_folder
   ```


4. **保留源文件**：
   ```sh
   slc.py -cn input.txt -o output.txt -p
   ```


##### 该翻译不会改变文件内容的结构，也不会改变原有的文件命名，仅会将文件内容中的繁体字转换成简体字。

