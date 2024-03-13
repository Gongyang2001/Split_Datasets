import xml.etree.ElementTree as ET
import os
import random
import shutil

# 获取整个数据集类别
def get_class_num(xml_path):
    # 指定包含XML文件的文件夹路径
    xml_files = os.listdir(xml_path)
    xml_filename = set()

    # 循环遍历文件夹中的每个XML文件
    for filename in xml_files:
        if filename.endswith('.xml'):
            xml_file_path = os.path.join(xml_path, filename)

            # 解析XML文件
            tree = ET.parse(xml_file_path)
            root = tree.getroot()

            # 遍历XML文件的第三层子标签，提取name标签的值
            for element in root.iter():
                if element.tag == 'name':
                    xml_filename.add(element.text)
    class_num = len((list(xml_filename)))
    print("共有%d个类别" %(class_num) + ": ", list(xml_filename))
    return list(xml_filename)

def convert(size, box):
    dw = 1. / (size[0])
    dh = 1. / (size[1])
    x = (box[0] + box[1]) / 2.0 - 1
    y = (box[2] + box[3]) / 2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    x = round(x, 6)
    w = round(w, 6)
    y = round(y, 6)
    h = round(h, 6)
    return x, y, w, h

def convert_annotation(xml_filepath, output_path):
    # try:
    in_file = open("{}.xml".format(xml_filepath), 'r', encoding='utf-8')
    # out_file = open("{}.txt".format(output_path), 'w', encoding='utf-8')
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
    for obj in root.iter('object'):
        # difficult = obj.find('Difficult').text
        # if difficult == 0:
        #     print(image_id)
        cls = obj.find('name').text
        if cls not in classes:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
             float(xmlbox.find('ymax').text))
        b1, b2, b3, b4 = b
        # 标注越界修正
        if b2 > w:
            b2 = w
        if b4 > h:
            b4 = h

        b = (b1, b2, b3, b4)
        bb = convert((w, h), b)
        with open("{}.txt".format(output_path), 'w+', encoding='utf-8') as file:
            file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

# 划分数据集
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
        image_train_basename = os.path.splitext(os.path.basename(image_train))[0]  # 获取标签文件的前缀，不带后缀.png或者其他的格式
        label_train_path = root_labels_path + "\\" + f"{image_train_basename}" + ".txt"  # 得到未分割前的标签文件路径
        if label_train_path in labels_list:
            if os.path.isfile(label_train_path):  # 判断是否为文件
                # 将未分割前的标签文件拷贝到目标标签文件夹train中
                shutil.copy(label_train_path, target_labels_train_path)
        else:
            print(label_train_path + " 不是文件！")

    for image_val in images_val:
        if len(target_images_val_path) == 0:  # 判断分割后的val文件夹是否为空
            print(target_images_val_path + " 文件夹为空！")
        image_val_basename = os.path.splitext(os.path.basename(image_val))[0]  # 获取标签文件的前缀，不带后缀.png或者其他的格式
        label_val_path = root_labels_path + "\\" + f"{image_val_basename}" + ".txt"  # 得到未分割前的标签文件路径
        if label_val_path in labels_list:
            if os.path.isfile(label_val_path):  # 判断是否为文件
                # 将未分割前的标签文件拷贝到目标标签文件夹val中
                shutil.copy(label_val_path, target_labels_val_path)
        else:
            print(label_val_path + " 不是文件！")

    for image_test in images_test:
        if len(target_images_test_path) == 0:  # 判断分割后的test文件夹是否为空
            print(target_images_test_path + " 文件夹为空！")
        image_test_basename = os.path.splitext(os.path.basename(image_test))[0]  # 获取标签文件的前缀，不带后缀.png或者其他的格式
        label_test_path = root_labels_path + "\\" + f"{image_test_basename}" + ".txt"  # 得到未分割前的标签文件路径
        if label_test_path in labels_list:
            if os.path.isfile(label_test_path):  # 判断是否为文件
                # 将未分割前的标签文件拷贝到目标标签文件夹test中
                shutil.copy(label_test_path, target_labels_test_path)
        else:
            print(label_test_path + " 不是文件！")

    print("标签划分完成！")

xml_path = r"C:\Users\server\Downloads\lyh\datasets\SAR-Ship\ship_detection_online\Annotations_new"

classes = get_class_num(xml_path)

root_images_path = r'C:\Users\server\Downloads\lyh\datasets\SAR-Ship\ship_detection_online\JPEGImages'  # 未分割前图像数据
root_labels_path = r'C:\Users\server\Downloads\lyh\datasets\SAR-Ship\ship_detection_online\labels'
target_images_path = r'C:\Users\server\Downloads\lyh\datasets\SAR-Ship\ship_detection_online\target\images'  # 分割后存储图像数据目录
target_labels_path = r'C:\Users\server\Downloads\lyh\datasets\SAR-Ship\ship_detection_online\target\labels'  # 分割后存储标签数据目录

if not os.path.exists(root_labels_path):
    os.makedirs(root_labels_path)

for root, dirs, files in os.walk(xml_path):
    for file in files:
        file_path = root + "//" + file.split(".")[0]
        # print(file_path)

        convert_annotation(file_path, root_labels_path + "//" + file.split(".")[0])

split_datasets(root_images_path, target_images_path, root_labels_path, target_labels_path)

print("转换成功！")
