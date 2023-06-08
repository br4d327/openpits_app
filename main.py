import streamlit as st
from ultralytics import YOLO
from PIL import Image
import io
import os
import torch
from datetime import datetime


@st.cache_resource()
def load_model():
    return YOLO('models/best.pt')


def image_input():
    image_file = st.file_uploader("Upload An Image", type=['png', 'jpeg', 'jpg'])

    if image_file is not None:

        ts = datetime.timestamp(datetime.now())
        img_path = os.path.join(r'data\uploads', str(ts) + image_file.name)

        with open(img_path, mode="wb") as f:
            f.write(image_file.getbuffer())

        return img_path


def load_image():
    uploaded_file = st.file_uploader(label='Выберите изображение для распознавания')
    if uploaded_file is not None:
        image_data = uploaded_file.getvalue()
        st.image(image_data)
        return Image.open(io.BytesIO(image_data))
    else:
        return None


st.title('Stone detector')

if __name__ == '__main__':

    if torch.cuda.is_available():
        deviceoption = st.sidebar.radio("Select compute Device.", ['cpu', 'cuda'], disabled=False, index=1)
    else:
        deviceoption = st.sidebar.radio("Select compute Device.", ['cpu', 'cuda'], disabled=True, index=0)

    # call Model prediction--
    model = load_model()
    img_dir = image_input()

    col1, col2 = st.columns(2)
    result = 0
    if img_dir is not None:
        img = Image.open(img_dir)
        with col1:
            st.image(img, caption='Uploaded Image', use_column_width='always')

        result = st.button('Detect stones!!!')
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

        # --Display predicton
        img_ = Image.open(latest_file)
        with col2:
            st.image(img_, caption='Model Prediction', use_column_width='always')
        print('#' * 30)
        print(os.path.join(r'data\results', img_dir.split('\\')[-1]))






