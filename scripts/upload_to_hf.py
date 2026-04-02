import os
from unsloth import FastLanguageModel

# 1. Cấu hình thông tin Hugging Face của bạn
HF_TOKEN = os.getenv("HF_TOKEN") # Lấy token từ huggingface.co/settings/tokens (Quyền Write)
USERNAME = "phgrouptechs"
REPO_NAME = "hotel-agent" # Tên model bạn muốn đặt trên HF

MODEL_SAVE_PATH = "hotel_agent_lora_model" # Thư mục chứa model vừa train xong ở bước trước
HF_HUB_PATH = f"{USERNAME}/{REPO_NAME}"

# 2. Tải lại model từ thư mục Local
print(f"Đang tải model từ thư mục {MODEL_SAVE_PATH}...")
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = MODEL_SAVE_PATH,
    max_seq_length = 2048,
    dtype = None,
    load_in_4bit = True,
)

# 3. Đẩy lên Hugging Face
print(f"Đang đẩy model lên Hugging Face: https://huggingface.co/{HF_HUB_PATH}")

# Đẩy LoRA adapters (Nhẹ, tải lên rất nhanh)
model.push_to_hub(HF_HUB_PATH, token = HF_TOKEN)
tokenizer.push_to_hub(HF_HUB_PATH, token = HF_TOKEN)

# (Tùy chọn) Nếu bạn muốn gộp LoRA vào model gốc và tải lên file GGUF để chạy Ollama/LMStudio:
# print("Đang xuất và đẩy model GGUF (Q4_K_M) lên Hugging Face...")
# model.push_to_hub_gguf(HF_HUB_PATH, tokenizer, quantization_method = "q4_k_m", token = HF_TOKEN)

print("Đã tải lên thành công!")