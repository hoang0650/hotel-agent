import json
import random
import uuid

# ==========================================
# 1. KHO DỮ LIỆU ĐỘNG (RUỘT RỖNG)
# ==========================================
hotel_names = ["hotel_name"]
streets = ["street"]
cities = ["city"]
room_types = ["room_type"]
descriptions = ["descriptions"]
suitable_fors = ["suitable_for"]
amenities_list = ["amenities_list"]

# ==========================================
# 2. CẤU HÌNH NHÓM CÂU HỎI & KỊCH BẢN (10,000 MẪU)
# ==========================================
intents_config = {
    "Inquiry": {
        "count": 2000,
        "questions": [
            "Báo giá cho tôi {room_type}",
            "Phòng {room_type} bên mình giá sao em?",
            "Cho chị hỏi thông tin {room_type} với."
        ],
        "answers": [
            "Dạ chào anh/chị, giá của {room_type} tại {hotel_name} là: {price}/đêm ạ. Căn phòng này rất phù hợp cho trải nghiệm {suitable_for} của mình đấy ạ.",
            "Dạ {room_type} bên em đang có mức giá tham khảo là {price}/đêm. Phòng được trang bị sẵn {amenities} ạ."
        ]
    },
    "Booking": {
        "count": 2000,
        "questions": [
            "Anh muốn đặt {room_type} cuối tuần này.",
            "Chốt cho chị {room_type} nhé, thủ tục sao em?",
            "Cho mình book {room_type} giá {price}."
        ],
        "answers": [
            "Dạ tuyệt vời ạ. Để tiến hành giữ {room_type} với mức giá {price}, anh/chị vui lòng liên hệ hotline {hotline} hoặc email {email_support} để bộ phận Lễ tân hỗ trợ nhanh nhất nhé.",
            "Dạ em xác nhận yêu cầu đặt {room_type}. Hệ thống bên em cần thông tin chi tiết, anh/chị gọi qua {hotline} giúp em để chốt phòng an toàn nhé ạ."
        ]
    },
    "Upsell": {
        "count": 1500,
        "questions": [
            "Anh thấy {room_type} hơi bé, có phòng nào xịn hơn không?",
            "Chị đi {suitable_for} muốn ở rộng rãi xíu.",
            "Còn hạng nào view đẹp hơn không em?"
        ],
        "answers": [
            "Dạ nếu anh/chị muốn không gian thoải mái hơn cho {suitable_for}, em rcm mình nâng cấp lên hạng {room_type} ạ. Giá chỉ {price}/đêm nhưng có đầy đủ {amenities} và {description} luôn ạ.",
            "Dạ bên em đang có hạng {room_type} cao cấp cực kỳ hot. Chỉ với {price}/đêm, mình sẽ tận hưởng {amenities} tuyệt vời ạ. Anh/chị chốt luôn hạng này nhé?"
        ]
    },
    "Objection": {
        "count": 1500,
        "questions": [
            "Sao {room_type} giá tận {price}, trên Agoda rẻ hơn em ơi.",
            "Giá {price} hơi chát nhỉ, có bớt không em?",
            "Bên khách sạn A gần đó bán rẻ hơn bên em."
        ],
        "answers": [
            "Dạ em hiểu băn khoăn của anh/chị ạ. Tuy nhiên mức giá {price} cho {room_type} khi đặt trực tiếp bên {hotel_name} đã bao gồm đầy đủ {amenities} và cam kết không phát sinh phụ phí ẩn như trên các app OTA đâu ạ.",
            "Dạ tiền nào của nấy anh/chị ơi. Với {price}, mình được trải nghiệm {description} cực kỳ xứng đáng cho {suitable_for} luôn ạ. Em giữ phòng cho mình nhé?"
        ]
    },
    "Follow-up": {
        "count": 1000,
        "questions": [
            "Để chị hỏi lại ông xã đã nhé.",
            "Giá cũng được, để anh xem lại lịch rồi báo.",
            "(Khách đã xem và im lặng)"
        ],
        "answers": [
            "Dạ vâng ạ, hạng {room_type} bên em hiện trống không còn nhiều. Anh/chị cân nhắc sớm và báo lại qua hotline {hotline} để em giữ phòng cho mình nhé.",
            "Dạ {hotel_name} luôn sẵn sàng phục vụ ạ. Cần hỗ trợ thêm thông tin gì về {room_type} anh/chị cứ nhắn em nhé."
        ]
    },
    "Support": {
        "count": 1000,
        "questions": [
            "Cho anh hỏi mấy giờ được nhận phòng?",
            "Địa chỉ khách sạn mình ở đâu vậy em?",
            "Khách sạn nằm trên đường nào?"
        ],
        "answers": [
            "Dạ {hotel_name} có địa chỉ tại {street}, {city} ạ. Giờ Check-in tiêu chuẩn là {check_in_time} và Check-out là {check_out_time} anh/chị nhé.",
            "Dạ bên em nằm ở {street}, trung tâm {city} ạ. Anh/chị đến nhận phòng từ {check_in_time} nhé. Hotline lễ tân là {hotline} ạ."
        ]
    },
    "Edge_cases": {
        "count": 1000,
        "questions": [
            "Bot ngu quá, hỏi không trả lời được à?",
            "Tối nay đề về bao nhiêu em?",
            "Alo alo có ai không?"
        ],
        "answers": [
            "Dạ em là trợ lý ảo của {hotel_name}, em có thể chưa hiểu ý anh/chị, mong anh/chị thông cảm ạ. Em có thể hỗ trợ anh/chị kiểm tra giá hoặc đặt phòng tại {city} không ạ?",
            "Dạ xin lỗi anh/chị, em chỉ được đào tạo để tư vấn dịch vụ của {hotel_name} thôi ạ. Anh/chị có nhu cầu tìm phòng {room_type} không em báo giá cho mình nhé?"
        ]
    }
}

# ==========================================
# 3. HÀM TẠO HỘI THOẠI "RUỘT RỖNG"
# ==========================================
def generate_conversation(intent, config):
    # Sinh ngẫu nhiên Context cho Tenant
    hotel_name = random.choice(hotel_names)
    street = random.choice(streets)
    city = random.choice(cities)
    check_in_time = f"09:00"
    check_out_time = f"12:00"
    room_type = random.choice(room_types)
    price = f"1000 VND"
    description = random.choice(descriptions)
    suitable_for = random.choice(suitable_fors)
    amenities = random.choice(amenities_list)
    hotline = f"09hotline"
    email_support = f"email_support"

    # Lấy câu hỏi & câu trả lời ngẫu nhiên theo Intent
    q_template = random.choice(config["questions"])
    a_template = random.choice(config["answers"])

    # Format biến vào câu hỏi của khách
    question = q_template.format(
        room_type=room_type, price=price, suitable_for=suitable_for
    )

    # Format biến vào mẫu trả lời (Đóng vai trò là Template do chủ khách sạn cấu hình)
    filled_answer = a_template.format(
        hotel_name=hotel_name, street=street, city=city, 
        check_in_time=check_in_time, check_out_time=check_out_time, 
        room_type=room_type, price=price, description=description, 
        suitable_for=suitable_for, amenities=amenities, 
        hotline=hotline, email_support=email_support
    )

    # Xây dựng System Prompt ép model làm theo kịch bản
    system_prompt = f"""Bạn là Sale Agent AI của {hotel_name}. Bạn BẮT BUỘC tư vấn theo thông tin sau:
[THÔNG TIN KHÁCH SẠN]
- Địa chỉ: {street}, {city}, Việt Nam
- Check-in: {check_in_time} | Check-out: {check_out_time}
- Hotline: {hotline} | Email: {email_support}

[THÔNG TIN PHÒNG]
- Hạng phòng: {room_type}
- Giá: {price}/đêm
- Mô tả: {description}
- Phù hợp cho: {suitable_for}
- Tiện ích: {amenities}

[LUẬT XỬ LÝ - {intent.upper()}]
Tình huống khách: "{question}"
Cách xử lý BẮT BUỘC từ hệ thống: "{filled_answer}"
Nhiệm vụ của bạn là đưa ra câu trả lời dựa trên cách xử lý trên, văn phong tự nhiên, lịch sự."""

    # Assistant tuân thủ luật
    assistant_prompt = filled_answer

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question},
        {"role": "assistant", "content": assistant_prompt}
    ]

# ==========================================
# 4. THỰC THI TẠO 10.000 DATASET
# ==========================================
conversations_dataset = {"conversations": []}

print("Đang tiến hành sinh Dataset...")
for intent, config in intents_config.items():
    count = config["count"]
    print(f"- Đang tạo {count} mẫu cho nhóm {intent}...")
    for _ in range(count):
        conversations_dataset["conversations"].append(generate_conversation(intent, config))

# Xáo trộn toàn bộ 10.000 mẫu để model không học theo thứ tự nhóm
random.shuffle(conversations_dataset["conversations"])

# Lưu file JSON
output_file = 'hotel_agent_10k_dataset.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(conversations_dataset, f, ensure_ascii=False, indent=2)

print(f"\n✅ Hoàn tất! Đã lưu 10.000 mẫu dữ liệu vào file '{output_file}'")