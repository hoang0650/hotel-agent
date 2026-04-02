import os
from huggingface_hub import HfApi

# ==========================================
# CẤU HÌNH THÔNG TIN
# ==========================================
HF_TOKEN = os.getenv("HF_TOKEN") # Điền token của bạn (nhớ cấp quyền Write)
REPO_NAME = "phgrouptechs/hotel-agent"       # Ví dụ: "nguyenvana/hotel-agent-8b-gguf"

# Tên file GGUF bạn đang có trên máy RunPod
LOCAL_FILE_PATH = "hotel_agent_model_gguf/llama-3-8b-instruct.Q4_K_M.gguf"

# Tên file khi hiển thị trên Hugging Face (thường để giống tên gốc)
PATH_IN_REPO = "hotel_agent_model.Q4_K_M.gguf"
# ==========================================
# TIẾN HÀNH UPLOAD
# ==========================================
api = HfApi()

print(f"Đang kiểm tra/tạo repository '{REPO_NAME}' trên Hugging Face...")
# Tự động tạo Repo nếu nó chưa tồn tại (để private=False nếu muốn public)
api.create_repo(repo_id=REPO_NAME, token=HF_TOKEN, exist_ok=True, private=False)

print(f"Đang đẩy file {LOCAL_FILE_PATH} lên Hugging Face...")
print("Quá trình này tùy thuộc vào tốc độ mạng, vui lòng chờ...")

# Lệnh Upload
api.upload_file(
    path_or_fileobj=LOCAL_FILE_PATH,
    path_in_repo=PATH_IN_REPO,
    repo_id=REPO_NAME,
    token=HF_TOKEN,
)

print(f"🎉 Upload thành công! Truy cập model của bạn tại: https://huggingface.co/{REPO_NAME}")