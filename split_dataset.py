import os
import shutil
import random

# 경로 설정
root_path = r"C:\Users\sinya\OneDrive\Documents\GitHub\Object-Detection_project\New_Sample"
#C:\Users\sinya\OneDrive\Desktop\WOD\New_Sample\unlabeled_data\TS1_indoor_big_parking_lot\indoor\big_lot
source_root = os.path.join(root_path, r"source_data\TS1\indoor\big_lot")
label_root = os.path.join(root_path, r"labeled_data\TL1\indoor\big_lot")
output_root = os.path.join(root_path, r"split_data")

# 하위 폴더 목록
subfolders = ["big_lot_001", "big_lot_002", "big_lot_004"]

# 데이터셋 분할 비율
train_ratio = 0.7
val_ratio = 0.2
test_ratio = 0.1

# 출력 경로 설정
output_dirs = {
    "train": os.path.join((output_root), "train"),
    "validation": os.path.join((output_root), "validation"),
    "test": os.path.join((output_root), "test")
}

# 출력 경로 생성
for split in output_dirs.values():
    os.makedirs(os.path.join(split, "images"), exist_ok=True)
    os.makedirs(os.path.join(split, "labels"), exist_ok=True)

# 이미지-라벨 쌍을 모아 분할
all_data_pairs = []

for folder in subfolders:
    image_folder = os.path.join(source_root, folder, "Camera")
    label_folder = os.path.join(label_root, folder, "label")

    for file_name in os.listdir(image_folder):
        if file_name.endswith('.jpg'):
            image_path = os.path.join(image_folder, file_name)
            label_path = os.path.join(label_folder, file_name.replace('.jpg', '.json'))
            if os.path.exists(label_path):  # 라벨 파일이 존재하는 경우만 추가
                all_data_pairs.append((image_path, label_path))

# 데이터셋 무작위 셔플
random.shuffle(all_data_pairs)

# 분할 인덱스 계산
num_total = len(all_data_pairs)
num_train = int(num_total * train_ratio)
num_val = int(num_total * val_ratio)

# 데이터셋 분할
train_data = all_data_pairs[:num_train]
val_data = all_data_pairs[num_train:num_train + num_val]
test_data = all_data_pairs[num_train + num_val:]

# 이미지와 라벨 파일을 각각의 폴더로 이동
def move_files(data, split):
    for image_path, label_path in data:
        # 이미지와 라벨 파일의 새로운 경로
        new_image_path = os.path.join(output_dirs[split], "images", os.path.basename(image_path))
        new_label_path = os.path.join(output_dirs[split], "labels", os.path.basename(label_path))

        # 파일 복사
        shutil.copy2(image_path, new_image_path)
        shutil.copy2(label_path, new_label_path)

# 파일 이동
move_files(train_data, "train")
move_files(val_data, "validation")
move_files(test_data, "test")