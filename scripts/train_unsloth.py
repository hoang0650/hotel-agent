import os
# Ép Python phải nhìn thấy thư mục chứa file libnvJitLink.so.13 của CUDA
os.environ["LD_LIBRARY_PATH"] = "/usr/local/cuda/lib64:" + os.environ.get("LD_LIBRARY_PATH", "")
import torch
from unsloth import FastLanguageModel
from unsloth.chat_templates import get_chat_template
from datasets import load_dataset, concatenate_datasets
from trl import SFTTrainer
from transformers import TrainingArguments

# ==========================================
# 1. CẤU HÌNH CƠ BẢN VÀ TẢI MODEL GỐC
# ==========================================
max_seq_length = 2048
dtype = None 
load_in_4bit = False

print("Đang tải model gốc Llama-3-8B-Instruct...")
# SỬ DỤNG MODEL BASE CỦA UNSLOTH ĐỂ TRÁNH LỖI XUNG ĐỘT ADAPTER
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "unsloth/llama-3-8b-Instruct-bnb-4bit",
    max_seq_length = max_seq_length,
    dtype = dtype,
    load_in_4bit = load_in_4bit,
)

# Bây giờ hàm này sẽ chạy mượt mà vì model gốc chưa có LoRA nào cả
model = FastLanguageModel.get_peft_model(
    model,
    r = 16, 
    target_modules = ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    lora_alpha = 16,
    lora_dropout = 0, 
    bias = "none",    
    use_gradient_checkpointing = "unsloth",
    random_state = 3407,
    use_rslora = False,
)

tokenizer = get_chat_template(
    tokenizer,
    chat_template = "llama-3",
    mapping = {"role": "role", "content": "content", "user": "user", "assistant": "assistant"}
)

def formatting_prompts_func(examples):
    convos = examples["conversations"]
    texts = [tokenizer.apply_chat_template(convo, tokenize = False, add_generation_prompt = False) for convo in convos]
    return { "text" : texts }

# ==========================================
# 2. XỬ LÝ VÀ CHUẨN HÓA CÁC DATASET
# ==========================================
print("Đang tải và chuẩn hóa các dataset...")

local_dataset = load_dataset("json", data_files="data/hotel_dataset.json", split="train")

dolly_raw = load_dataset("databricks/databricks-dolly-15k", split="train")
def format_dolly(example):
    prompt = example["instruction"]
    if example["context"]:
        prompt += f"\n\nContext:\n{example['context']}"
    return {"conversations": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": example["response"]}
    ]}
dolly_formatted = dolly_raw.map(format_dolly, remove_columns=dolly_raw.column_names)
dolly_formatted = dolly_formatted.shuffle(seed=42).select(range(2000))

oasst_raw = load_dataset("timdettmers/openassistant-guanaco", split="train")
def format_oasst(example):
    text = example["text"]
    parts = text.split("### Assistant:")
    user_part = parts[0].replace("### Human:", "").strip()
    assistant_part = parts[1].split("### Human:")[0].strip() if len(parts) > 1 else "I can help with that."
    return {"conversations": [
        {"role": "user", "content": user_part},
        {"role": "assistant", "content": assistant_part}
    ]}
oasst_formatted = oasst_raw.map(format_oasst, remove_columns=oasst_raw.column_names)
oasst_formatted = oasst_formatted.shuffle(seed=42).select(range(1500))

woz_hotel_raw = load_dataset("vidhikatkoria/DA_MultiWOZ_hotel", split="train")
def format_woz_hotel(example):
    return {"conversations": [
        {"role": "user", "content": example["context"].replace("User:", "").strip()},
        {"role": "assistant", "content": example["response"].replace("Agent:", "").strip()}
    ]}
woz_hotel_formatted = woz_hotel_raw.map(format_woz_hotel, remove_columns=woz_hotel_raw.column_names)
woz_hotel_formatted = woz_hotel_formatted.shuffle(seed=42).select(range(1500))

print("Đang trộn dữ liệu (Data Mixing)...")
mixed_dataset = concatenate_datasets([
    local_dataset, 
    dolly_formatted, 
    oasst_formatted, 
    woz_hotel_formatted
])

mixed_dataset = mixed_dataset.shuffle(seed=42)
final_dataset = mixed_dataset.map(formatting_prompts_func, batched = True, remove_columns=mixed_dataset.column_names)

# ==========================================
# 3. TIẾN HÀNH HUẤN LUYỆN VÀ LƯU MODEL
# ==========================================
trainer = SFTTrainer(
    model = model,
    tokenizer = tokenizer,
    train_dataset = final_dataset,
    dataset_text_field = "text",
    max_seq_length = max_seq_length,
    dataset_num_proc = 2,
    packing = False, 
    args = TrainingArguments(
        per_device_train_batch_size = 2,
        gradient_accumulation_steps = 4,
        warmup_steps = 10,
        max_steps = 500, 
        learning_rate = 2e-4,
        fp16 = not torch.cuda.is_bf16_supported(),
        bf16 = torch.cuda.is_bf16_supported(),
        logging_steps = 10,
        optim = "adamw_torch",
        weight_decay = 0.01,
        lr_scheduler_type = "linear",
        seed = 3407,
        output_dir = "outputs",
    ),
)

print("Bắt đầu huấn luyện...")
trainer_stats = trainer.train()

model_save_path = "hotel_agent_lora_model"
print(f"Lưu model tại: {model_save_path}")
model.save_pretrained(model_save_path)
tokenizer.save_pretrained(model_save_path)

print("Huấn luyện thành công!")