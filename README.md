# Hotel AI Agent Training - RunPod Guide

Dự án này sử dụng Unsloth để fine-tune model `phgrouptechs/Denglish-8B-Instruct` thành một Sale Agent khách sạn dựa trên tập dữ liệu ShareGPT.

## Bước 1: Thuê máy trên RunPod
1. Đăng nhập RunPod, vào mục **Pods** -> **Deploy**.
2. Chọn GPU: **1x RTX 3090**, **1x RTX 4090** hoặc **1x A5000** (Dung lượng VRAM 24GB là dư sức).
3. Chọn Template: **RunPod Pytorch 2.1** (hoặc bản Pytorch mới nhất).
4. Storage: Đặt Volume Disk khoảng **50GB** (để chứa model và data).
5. Bấm Deploy và đợi Pod chạy (khoảng 1-2 phút). Sau đó bấm **Connect** -> Bật **Jupyter Lab**.

## Bước 2: Tải code và cài đặt môi trường
Mở Terminal trong Jupyter Lab (hoặc qua SSH) và chạy lần lượt các lệnh sau:

```bash
# 1. Clone dự án (nếu bạn để trên Github) hoặc upload thẳng folder dự án lên Jupyter Lab
# Thay 'url-git-cua-ban' bằng link git của bạn, hoặc bỏ qua bước này nếu bạn kéo thả folder từ máy tính vào.
git clone <url-git-cua-ban> hotel-agent-training
cd hotel-agent-training

# 2. Cài đặt các thư viện lõi
pip install -r requirements.txt
```

## Bước 3: Đưa Dataset vào Storage
Đảm bảo bạn đã upload file data của mình (chuẩn cấu trúc ShareGPT) vào đường dẫn:
`sale-agent/data/hotel_dataset.json`

## Bước 4: Chạy quá trình huấn luyện
Chỉ cần chạy lệnh sau và đi uống cafe. Script đã tự động handle việc tải base model, mapping dataset, và sử dụng QLoRA để không bị tràn RAM.
```bash
python scripts/train_unsloth.py
python scripts/upload_to_hf.py
```
## Bước 5: Lấy kết quả
Sau khi Terminal báo "Huấn luyện thành công!", bạn sẽ thấy một thư mục mới xuất hiện tên là `hotel_agent_lora_model`.

Thư mục này chứa các file Adapter (`adapter_model.safetensors`, `adapter_config.json`...).
Để sử dụng, bạn chỉ cần tải thư mục này về máy hoặc nén lại:
```bash
tar -czvf hotel_model_ready.tar.gz hotel_agent_lora_model/
```
Sau đó chuột phải vào file .tar.gz trong Jupyter Lab và chọn Download.
---

### Cách sử dụng bộ khung này
1. Bạn tạo một folder trên máy tính, ném 3 file code (`requirements.txt`, `train_unsloth.py`, `README.md`) vào đúng vị trí thư mục.
2. Ném file data của bạn vào thư mục `data`.
3. Nén toàn bộ folder đó lại dưới dạng `.zip`, lên RunPod (mở Jupyter Lab) kéo thả file zip đó vào là xong.
4. Mở terminal trên RunPod, giải nén và làm y hệt theo từng dòng lệnh trong `README.md`.
