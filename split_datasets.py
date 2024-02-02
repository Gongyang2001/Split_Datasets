import os
import random
import shutil


def split_datasets(root_images_path, target_images_path, root_labels_path, target_labels_path):
    # 读取图片数据路径，判断图片数据集是否存在
    if os.path.exists(root_images_path) == False:
        print("图片数据集不存在！")
    # 创建列表用于存储图片文件名，str类型 /Users/wangqi/Documents/datasets/personandcar/images/513.png
    images_list = []
    # 读取文件目录下的所有文件将其存储到列表中
    for dirpath, dirnames, filenames in os.walk(root_images_path):
        for file in filenames:
            file_path = os.path.join(dirpath, file)
            images_list.append(file_path)

    # 将列表顺序打乱
    random.shuffle(images_list)

    # 将打乱后的列表按6:2:2的比例划分为训练集、验证集和测试集，列表切片需整数
    images_size = len(images_list)
    images_train = images_list[0:round(images_size * 0.6)]
    images_val = images_list[round(
        images_size * 0.6):round(images_size * 0.8)]
    images_test = images_list[round(images_size * 0.8):]
    # print(len(images_train), len(images_val), len(images_test))

    # 判断目标目录是否存在train、val、test三个文件夹，不存在则在目标目录下创建train、val、test三个文件夹
    target_images_train_path = target_images_path + "/train"
    target_images_val_path = target_images_path + "/val"
    target_images_test_path = target_images_path + "/test"

    if not os.path.exists(target_images_train_path):  # 判断目标文件夹train是否存在，不存在则创建
        os.makedirs(target_images_train_path)
    if not os.path.exists(target_images_val_path):  # 判断目标文件夹val是否存在，不存在则创建
        os.makedirs(target_images_val_path)
    if not os.path.exists(target_images_test_path):  # 判断目标文件夹test是否存在，不存在则创建
        os.makedirs(target_images_test_path)

    # train、val、test文件夹初始化
    for root, dirs, files in os.walk(target_images_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            # 删除文件
            os.remove(file_path)
            # print(f"已删除文件: {file_path}")

    for image_train in images_train:  # 遍历列表将分割后的图片拷贝至目标文件夹中
        if os.path.isfile(image_train):
            # 将文件拷贝到train文件夹下
            shutil.copy(image_train, target_images_train_path)
        else:
            print(image_train + " 不是文件！")

    for image_val in images_val:  # 遍历列表将分割后的图片拷贝至目标文件夹中
        if os.path.isfile(image_val):
            shutil.copy(image_val, target_images_val_path)  # 将文件拷贝到val文件夹下
        else:
            print(images_val + " 不是文件！")

    for image_test in images_test:  # 遍历列表将分割后的图片拷贝至目标文件夹中
        if os.path.isfile(image_test):
            shutil.copy(image_test, target_images_test_path)  # 将文件拷贝到test文件夹下
        else:
            print(image_test + " 不是文件！")
    print("图片分割完毕！")

    # 读取标签数据路径，判断标签数据集是否存在
    if os.path.exists(root_labels_path) == False:
        print("标签数据集不存在！")

    # 创建labels_list用于存储标签，类型为str /Users/wangqi/Documents/datasets/personandcar/labels/445.txt
    labels_list = []
    for dirpath, dirnames, filenames in os.walk(root_labels_path):
        for file in filenames:
            label_file_path = os.path.join(dirpath, file)
            labels_list.append(label_file_path)

    target_labels_train_path = target_labels_path + "/train"  # 在目标标签目录下创建train文件夹
    target_labels_val_path = target_labels_path + "/val"  # 在目标标签目录下创建val文件夹
    target_labels_test_path = target_labels_path + "/test"  # 在目标标签目录下创建test文件夹

    if not os.path.exists(target_labels_train_path):  # 判断目标文件夹train是否存在，不存在则创建
        os.makedirs(target_labels_train_path)
    if not os.path.exists(target_labels_val_path):  # 判断目标文件夹train是否存在，不存在则创建
        os.makedirs(target_labels_val_path)
    if not os.path.exists(target_labels_test_path):  # 判断目标文件夹train是否存在，不存在则创建
        os.makedirs(target_labels_test_path)

    # train、val、test文件夹初始化
    for root, dirs, files in os.walk(target_labels_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            # 删除文件
            os.remove(file_path)
            # print(f"已删除文件: {file_path}")

    for image_train in images_train:
        if len(target_images_train_path) == 0:  # 判断分割后的train文件夹是否为空
            print(target_images_train_path + " 文件夹为空！")
        image_train_basename = os.path.splitext(
            os.path.basename(image_train))[0]  # 获取标签文件的前缀，不带后缀.png或者其他的格式
        label_train_path = root_labels_path + \
            "/" + f"{image_train_basename}" + ".txt"  # 得到未分割前的标签文件路径
        if label_train_path in labels_list:
            if os.path.isfile(label_train_path):  # 判断是否为文件
                # 将未分割前的标签文件拷贝到目标标签文件夹train中
                shutil.copy(label_train_path, target_labels_train_path)
        else:
            print(label_train_path + " 不是文件！")

    for image_val in images_val:
        if len(target_images_val_path) == 0:  # 判断分割后的val文件夹是否为空
            print(target_images_val_path + " 文件夹为空！")
        image_val_basename = os.path.splitext(os.path.basename(image_val))[
            0]  # 获取标签文件的前缀，不带后缀.png或者其他的格式
        label_val_path = root_labels_path + \
            "/" + f"{image_val_basename}" + ".txt"  # 得到未分割前的标签文件路径
        if label_val_path in labels_list:
            if os.path.isfile(label_val_path):  # 判断是否为文件
                # 将未分割前的标签文件拷贝到目标标签文件夹val中
                shutil.copy(label_val_path, target_labels_val_path)
        else:
            print(label_val_path + " 不是文件！")

    for image_test in images_test:
        if len(target_images_test_path) == 0:  # 判断分割后的test文件夹是否为空
            print(target_images_test_path + " 文件夹为空！")
        image_test_basename = os.path.splitext(os.path.basename(image_test))[
            0]  # 获取标签文件的前缀，不带后缀.png或者其他的格式
        label_test_path = root_labels_path + \
            "/" + f"{image_test_basename}" + ".txt"  # 得到未分割前的标签文件路径
        if label_test_path in labels_list:
            if os.path.isfile(label_test_path):  # 判断是否为文件
                # 将未分割前的标签文件拷贝到目标标签文件夹test中
                shutil.copy(label_test_path, target_labels_test_path)
        else:
            print(label_test_path + " 不是文件！")

    print("标签划分完成！")


if __name__ == '__main__':
    root_images_path = '/Users/wangqi/Documents/datasets/personandcar/images'  # 未分割前图像数据
    root_labels_path = '/Users/wangqi/Documents/datasets/personandcar/labels'  # 未分割前标签数据
    target_images_path = '/Users/wangqi/Documents/datasets/personandcar/target/images'  # 分割后存储图像数据目录
    target_labels_path = '/Users/wangqi/Documents/datasets/personandcar/target/labels'  # 分割后存储标签数据目录
    split_datasets(root_images_path, target_images_path,
                    root_labels_path, target_labels_path)
