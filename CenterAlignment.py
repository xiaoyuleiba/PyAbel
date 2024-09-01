file_path = 'c:\\Users\\Xiao\\Desktop\\463985.img'
width, height = 1920, 1200
radius = 512
new_size = 1024
output_path_rgb = 'output_rgb_white.bmp'
output_path_cropped = 'cropped_image_white.bmp'
output_path_txt = 'centered_data.txt'





import numpy as np
from PIL import Image

def read_binary_data(file_path, width, height):
    with open(file_path, 'rb') as f:
        data = f.read()
        separator = b'UserComment=""'  # 假设 UTF-8 数据以 'aaa,' 结尾
        index = data.find(separator)
        if index == -1:
            raise ValueError("Separator not found in the file")
        binary_start = index + len(separator)
        binary_data = data[binary_start:]
    return np.frombuffer(binary_data, dtype=np.uint16).reshape((height, width))

def find_circle_center(matrix, radius):
    y_coords, x_coords = np.where(matrix > 0)
    center_x = int(np.mean(x_coords))
    center_y = int(np.mean(y_coords))
    return center_x, center_y

def shift_circle_to_center(matrix, center_x, center_y, width, height, new_size):
    new_matrix = np.full((new_size, new_size), fill_value=0, dtype=np.uint16)
    y_start = max(center_y - new_size // 2, 0)
    y_end = min(center_y + new_size // 2, matrix.shape[0])
    x_start = max(center_x - new_size // 2, 0)
    x_end = min(center_x + new_size // 2, matrix.shape[1])

    new_matrix[
        :y_end - y_start,
        :x_end - x_start
    ] = matrix[
        y_start:y_end,
        x_start:x_end
    ]

    return new_matrix

def convert_to_rgb(matrix, width, height):
    rgb_image = np.ones((height, width, 3), dtype=np.uint8) * 255  # 设置为白底
    normalized_matrix = np.clip(matrix, 0, 255).astype(np.uint8)
    rgb_image[..., 0] = np.where(normalized_matrix > 0, normalized_matrix, 255)
    rgb_image[..., 1] = np.where(normalized_matrix > 0, 0, 255)
    rgb_image[..., 2] = np.where(normalized_matrix > 0, 0, 255)
    return rgb_image

def save_text_file(matrix, output_path):
    np.savetxt(output_path, matrix, fmt='%d', delimiter=' ')

def crop_and_save_circle(image, center_x, center_y, radius, output_path):
    width, height = image.size
    crop_box = (center_x - radius, center_y - radius, center_x + radius, center_y + radius)
    cropped_image = image.crop(crop_box)
    
    # Create a new 1024x1024 image and paste the cropped image
    new_image = Image.new('RGB', (1024, 1024), (255, 255, 255))  # 白底
    new_image.paste(cropped_image, (0, 0))
    new_image.save(output_path)

# 文件路径


# 读取数据并重建矩阵
matrix = read_binary_data(file_path, width, height)
# 查找圆心位置
center_x, center_y = find_circle_center(matrix, radius)
print(f'圆心位置: ({center_x}, {center_y})')
# 将圆形区域移动到图像中心
centered_matrix = shift_circle_to_center(matrix, center_x, center_y, width, height, new_size)
# 转换为 RGB 图像，背景为白色
rgb_image = Image.fromarray(convert_to_rgb(centered_matrix, new_size, new_size), mode='RGB')
rgb_image.save(output_path_rgb)

# 裁剪圆形区域并保存为 1024x1024 图像
crop_and_save_circle(rgb_image, new_size // 2, new_size // 2, radius, output_path_cropped)

# 保存中心化后的数据为文本文件
save_text_file(centered_matrix, output_path_txt)
