import streamlit as st
import os
import cv2
import numpy as np
from ultralytics import YOLO
from glob import glob

st.set_page_config(layout="wide")
st.title("📸 Dataset Creator for License Plate Recognition")

# Load model 1 lần duy nhất
model = YOLO(r"D:/Project/DetectionAndRecognition/Models/Yolov8/runs/detect/train/weights/best.pt")

# Setup folder
data_folder = st.sidebar.text_input("📁 Nhập đường dẫn đến thư mục ảnh gốc", r"D:\Project\DetectionAndRecognition\Upload_Kaggle_Dataset\LicensePlateVN\test\images")
save_folder = r"D:\Project\DetectionAndRecognition\Upload_Kaggle_Dataset\LicensePlateBoundingBoxes"
save_image_path = r"D:\Project\DetectionAndRecognition\Upload_Kaggle_Dataset\LicensePlateBoundingBoxes\Images"

os.makedirs(save_folder, exist_ok=True)
label_file_path = os.path.join(save_folder, "label_recognition.txt")

# Lấy danh sách ảnh
image_paths = sorted(glob(os.path.join(data_folder, "*.jpg")) + glob(os.path.join(data_folder, "*.png")))

# Session state
if "img_idx" not in st.session_state:
    st.session_state.img_idx = 0

if "sub_img_idx" not in st.session_state:
    st.session_state.sub_img_idx = 0

if "detections" not in st.session_state:
    st.session_state.detections = []

if "basename" not in st.session_state:
    st.session_state.basename = ""

if "sub_img_count" not in st.session_state:
    st.session_state.sub_img_count = 0

# Hàm xử lý ảnh
def load_image(image_path):
    img = cv2.imread(image_path)
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Predict
def predict_image(img):
    results = model(img)
    bboxes = results[0].boxes.xyxy.cpu().numpy().astype(int)
    return results[0].plot(), bboxes  # plot (BGR), bbox ndarray

# Reset sub ảnh
def reset_sub_imgs():
    st.session_state.sub_img_idx = 0
    st.session_state.sub_img_count = 0

# Xử lý ảnh hiện tại
if 0 <= st.session_state.img_idx < len(image_paths):
    image_path = image_paths[st.session_state.img_idx]
    basename = os.path.basename(image_path)
    st.session_state.basename = os.path.splitext(basename)[0]

    img = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Predict nếu chưa có kết quả
    if 'predicted' not in st.session_state or not st.session_state.predicted:
        img_result, bboxes = predict_image(img_rgb)
        st.session_state.detections = bboxes
        st.session_state.img_result = img_result
        st.session_state.predicted = True

    # Hiển thị ảnh gốc và predict song song
    col1, col2 = st.columns(2)
    with col1:
        st.image(image_path, caption="📷 Ảnh gốc")
    with col2:
        st.image(st.session_state.img_result, caption="🤖 Ảnh predict", channels="BGR")

    # Các nút predict và next ở giữa 2 ảnh
    st.markdown("---")
    col_center1, col_center2, col_center3 = st.columns([1, 1, 1])
    with col_center1:
        if st.button("🔄 Predict lại"):
            st.session_state.predicted = False  # Đánh dấu cần predict lại
    with col_center2:
        if st.button("➡️ Next ảnh"):
            st.session_state.img_idx += 1
            reset_sub_imgs()
            st.session_state.predicted = False
    st.markdown("---")

        # Sub-image bên trái, các nút bên phải
    if len(st.session_state.detections) > 0:
        total_sub_imgs = len(st.session_state.detections)
        sub_idx = st.session_state.sub_img_idx

        # Kiểm tra xem đã vượt số lượng sub ảnh chưa
        if sub_idx >= total_sub_imgs:
            st.info("✅ Đã duyệt hết sub_image.")
        else:
            bbox = st.session_state.detections[sub_idx]
            x1, y1, x2, y2 = bbox
            sub_img = img[y1:y2, x1:x2]

            # Resize và pad giữ nguyên tỉ lệ
            def resize_with_padding(image, target_size=(244, 244), pad_value=255):
                h, w = image.shape[:2]
                target_w, target_h = target_size

                scale = min(target_w / w, target_h / h)
                new_w, new_h = int(w * scale), int(h * scale)

                resized = cv2.resize(image, (new_w, new_h))
                pad_left = (target_w - new_w) // 2
                pad_right = target_w - new_w - pad_left
                pad_top = (target_h - new_h) // 2
                pad_bottom = target_h - new_h - pad_top

                padded = cv2.copyMakeBorder(resized, pad_top, pad_bottom, pad_left, pad_right,
                                            cv2.BORDER_CONSTANT, value=pad_value)
                return padded

            resized = resize_with_padding(sub_img)
            sub_img_display = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)

            col_sub1, col_sub2 = st.columns([1, 2])
            with col_sub1:
                st.image(sub_img_display, caption=f"🧱 Sub Image {sub_idx + 1}/{total_sub_imgs}", width=256)

            with col_sub2:
                label_input = st.text_input("📝 Nhập label cho biển số:", key=f"label_{st.session_state.img_idx}_{sub_idx}")
                st.markdown(f"🔢 **Sub image: {sub_idx + 1}/{total_sub_imgs}**")

                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    if st.button("✅ Accept"):
                        sub_img_name = f"{st.session_state.basename}_{st.session_state.sub_img_count}.jpg"
                        cv2.imwrite(os.path.join(save_image_path, sub_img_name), resized)

                        with open(label_file_path, "a", encoding="utf-8") as f:
                            f.write(f"{sub_img_name} {label_input.strip()}\n")

                        st.success(f"Đã lưu {sub_img_name} với label: {label_input.strip()}")
                        st.session_state.sub_img_count += 1

                with col_btn2:
                    if st.button("➡️ Next sub image"):
                        if sub_idx + 1 < total_sub_imgs:
                            st.session_state.sub_img_idx += 1
                        else:
                            st.info("✅ Đã duyệt hết sub_image.")

    else:
        st.warning("⚠️ Ảnh không xuất hiện biển số.")
