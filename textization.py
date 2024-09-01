import struct

def process_file(file_path):
    # 读取文件
    with open(file_path, 'rb') as f:
        content = f.read()

    # 查找 UTF-8 文本部分的结束标志
    utf8_end_marker = b'UserComment=""'  # 假设这个是 UTF-8 部分的结束标志
    utf8_end_index = content.find(utf8_end_marker)
    
    if utf8_end_index == -1:
        raise ValueError("UTF-8 文本部分结束标志未找到")

    # 二进制数据从 utf8 结束标志之后开始
    binary_data = content[utf8_end_index + len(utf8_end_marker):]

    # 读取 2 字节整数并填入矩阵
    width, height = 1920, 1200
    num_integers = width * height
    
    # 检查二进制数据长度是否与预期匹配
    if len(binary_data) < num_integers * 2:
        raise ValueError(f"二进制数据长度不足预期值 {num_integers * 2}")

    # 读取 2 字节整数
    integers = []
    for i in range(num_integers):
        start = i * 2
        end = start + 2
        int_bytes = binary_data[start:end]
        value, = struct.unpack('<H', int_bytes)  # '<H' 表示小端无符号 2 字节整数
        integers.append(value)

    # 将数据格式化为指定的矩阵形式
    formatted_data = []
    for i in range(height):
        row = integers[i * width:(i + 1) * width]
        formatted_data.append(' '.join(f'{num:5d}' for num in row))
    
    # 将结果保存到新文件
    output_path = file_path + '.processed'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(formatted_data).replace(' ' * 5, ' '))  # 将每5个空格替换为一个空格
    
    print(f"处理完成，结果保存为 {output_path}")

# 示例用法
process_file('c:\\Users\\Xiao\\Desktop\\463985.img')
