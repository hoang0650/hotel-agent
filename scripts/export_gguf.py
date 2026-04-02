from unsloth import FastLanguageModel

# ==========================================
# 1. TẢI LẠI MODEL VỪA TRAIN XONG
# ==========================================
print("Đang tải lại model từ thư mục hotel_agent_lora_model...")
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "hotel_agent_lora_model", # Thư mục chứa kết quả train của bạn
    max_seq_length = 1024,
    dtype = None,
    load_in_4bit = False, # Để False để quá trình gộp (merge) diễn ra chính xác nhất
)

# ==========================================
# 2. GỘP LORA VÀ NÉN GGUF
# ==========================================
print("Bắt đầu nén GGUF (Chế độ Q4_K_M - Tối ưu nhất cho CPU)...")
print("Quá trình này có thể mất 5-10 phút, vui lòng không tắt máy!")

# Unsloth sẽ tự động tải llama.cpp về và nén model giúp bạn
model.save_pretrained_gguf(
    "hotel_agent_model", # Tên file xuất ra
    tokenizer, 
    quantization_method = "q4_k_m"
)

print("🎉 Hoàn tất! Bạn có thể lấy file .gguf để mang lên Railway sử dụng.")