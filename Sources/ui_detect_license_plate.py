import streamlit as st
import numpy as np
import cv2
from ultralytics import YOLO

def create_input():
    with st.container():
        imgin = st.file_uploader('Upload a photo', type=['jpg', 'jpeg', 'png'])
    if imgin:
        with col1:
            st.image(imgin)
    return imgin

col1, col2 = st.columns(2)

def run(imgin):
    # Load model (chỉ load 1 lần nếu có thể, đặt ngoài hàm sẽ tốt hơn)
    model = YOLO("D:/Project/DetectionAndRecognition/Models/Yolov8/runs/detect/train/weights/best.pt")

    # Đọc ảnh từ bytes upload
    img_bytes = imgin.read()
    nparr = np.frombuffer(img_bytes, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Dự đoán với model ultralytics
    results = model(frame)

    # Lấy ảnh có vẽ bbox và nhãn (ultralytics hỗ trợ sẵn)
    img_result = results[0].plot()  # trả về numpy array BGR

    return img_result

if __name__ == '__main__':
    imgin = create_input()
    if imgin:
        if st.button("Predict"):
            imgout = run(imgin)
            with col2:
                st.image(imgout, channels="BGR")
