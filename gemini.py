import os

import google.generativeai as genai

os.environ["GEMINI_API_KEY"] = 'AIzaSyABtnr23TcoFqHMAGjeO6wiIEqZk8kFxNA'
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

generation_config = {
  "temperature": 0,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
)
response = model.generate_content("""MÔ TẢVẻ đẹp truyền thống dân gian xưa được thể hiện khéo léo trên chiếc yếm lệch tà. Hình ảnh tranh Đông Hồ được thêu lắc tay trên nền vải lụa Tafta toát lên nét đẹp của nghệ thuật văn hoá đương thời kết hợp với kiểu dáng yếm cách tân vừa lạ vừa quen. Yếm được lấy ý tưởng từ chiếc yếm truyền thống của người Việt Nam thời xưa. Hoạ tiết tranh thêu thủ công lắc tay được lấy trong bộ tranh vẽ về kiến trúc đình chùa thời kỳ An Nam của miền Bắc.Bộ tranh vẽ chỉ có hai bản gốc hiện đang lưu trữ ở bảo tàng bên Pháp và bảo tàng Mỹ Thuật Vietnam.KÍCH CỠFreesizeCHẤT LIỆUChất liệu vải chính: Lụa taftaVải mỏng cảm giác nhẹ nhàng, thoáng mát, không co giãn.XUẤT XỨViệt Nam
phân tích ra cho tôi các thông tin MÔ TẢ, MÀU SẮC, KÍCH CỠ, CHẤT LIỆU, XUẤT XỨ, HƯỚNG DẪN BẢO QUẢN, output dưới dạng dict, thông tin nào không có thì để trống""")
print(response.text)
