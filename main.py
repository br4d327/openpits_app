import streamlit as st
from ultralytics import YOLO
from PIL import Image
import pandas as pd
import os
import torch
from datetime import datetime
import numpy as np
H = 518
W = 409

@st.cache_resource()
def load_model():
    return YOLO('models/best.pt')


def img_summary(l_path):
    with open(l_path, 'r') as f:
        file = f.read()
    total_stones = len(file.split('\n')) - 1
    stones = file.split('\n')[:-1]
    avg_width = np.mean([float(stone.split(' ')[3]) * W for stone in stones])
    avg_height = np.mean([float(stone.split(' ')[4]) * H for stone in stones])
    print(l_path)
    t = pd.DataFrame([{'file_name': l_path.split('_')[-1][:-4],
                       'total_stones': total_stones,
                       'avg_width': avg_width,
                       'avg_height': avg_height}])
    return t


def image_input(mult_files):
    image_file = st.file_uploader("Upload An Image", type=['png', 'jpeg', 'jpg'], accept_multiple_files=mult_files)
    images_path = []
    print(image_file)
    if mult_files and image_file is not None:
        for img_f in image_file:
            ts = datetime.timestamp(datetime.now())
            img_path = os.path.join(r'data\uploads', str(ts) + '_' + img_f.name)

            with open(img_path, mode="wb") as f:
                f.write(img_f.getbuffer())
            images_path.append(img_path)
        print("I'm returning multiple files")
        return images_path

    elif image_file is not None:
            ts = datetime.timestamp(datetime.now())
            img_path = os.path.join(r'data\uploads', str(ts) + '_' + image_file.name)

            with open(img_path, mode="wb") as f:
                f.write(image_file.getbuffer())
            return img_path


st.title('Stone detector')

if __name__ == '__main__':

    detection_mode = st.sidebar.radio("Select detection mode.", ['Single file', 'Multiple files'], disabled=False, index=0)
    detection_mode = 1 if detection_mode == 'Multiple files' else 0

    if torch.cuda.is_available():
        deviceoption = st.sidebar.radio("Select compute Device.", ['cpu', 'cuda'], disabled=False, index=1)
    else:
        deviceoption = st.sidebar.radio("Select compute Device.", ['cpu', 'cuda'], disabled=True, index=0)

    # call Model prediction--
    model = load_model()
    img_dir = image_input(detection_mode)
    print('*'*10)
    print(img_dir)
    print('*'*10)
    col1, col2 = st.columns(2)
    result = 0
    mult_res = 0
    if img_dir is not None and not detection_mode:
        img = Image.open(img_dir)
        with col1:
            st.image(img, caption='Uploaded Image', use_column_width='always')

        result = st.button('Detect stones')
    elif img_dir is not None and detection_mode:
        mult_res = st.button('Detect stones')
    # start
    if result:
        dev = 'cpu' if deviceoption == 'cpu' else 1

        model.predict(img_dir,
                      save=True,
                      save_txt=True,
                      device=dev,
                      hide_conf=True,
                      hide_labels=True)

        all_sub_dirs = ['./runs/detect/'+d for d in os.listdir('./runs/detect')]
        latest_dir = max(all_sub_dirs, key=os.path.getctime)
        all_sub_files = [latest_dir + '/' + d for d in os.listdir(latest_dir)]
        latest_file = max(all_sub_files, key=os.path.getctime)

        all_label_files =[latest_dir+'/labels/' + d for d in os.listdir(latest_dir+'/labels')]
        latest_label_path = max(all_label_files, key=os.path.getctime)

        # --Display predicton
        img_ = Image.open(latest_file)

        sum_table = img_summary(latest_label_path)
        st.table(sum_table)

        with col2:
            st.image(img_, caption='Model Prediction', use_column_width='always')

    if mult_res:
        dev = 'cpu' if deviceoption == 'cpu' else 1

        for file in img_dir:
            model.predict(file,
                          save=True,
                          save_txt=True,
                          device=dev,
                          hide_conf=True,
                          hide_labels=True)

        all_sub_dirs = ['./runs/detect/' + d for d in os.listdir('./runs/detect')]
        latest_dir = max(all_sub_dirs, key=os.path.getctime)
        label_latest_dir = latest_dir + '/labels/'
        print(img_dir)
        print('#'*10)

        current_uploaded_img = [file.split('\\')[-1][:-4] for file in img_dir]
        print(current_uploaded_img)

        res_table = pd.DataFrame()
        for file in os.listdir(label_latest_dir):
            print(file)
            if file.split('/')[-1][:-4] in current_uploaded_img:
                print(label_latest_dir + file)
                table = img_summary(label_latest_dir + file)
                res_table = pd.concat([res_table, table])

        res_table.reset_index(drop=True, inplace=True)
        st.table(res_table)
        st.text('Summary')
        st.table(pd.DataFrame([{'total_files': len(res_table),
                                'avg_stones': res_table.total_stones.mean(),
                                'avg_width': res_table.avg_width.mean(),
                                'avg_height': res_table.avg_height.mean()}]))





