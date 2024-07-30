import requests
from bs4 import BeautifulSoup
import re
import json
import google.generativeai as genai
import pandas as pd
import os
import warnings
import time
warnings.filterwarnings("ignore")

# Cấu hình API Key và mô hình AI
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
)

def get_product_info(url):
    # Gửi yêu cầu GET đến trang web
    response = requests.get(url)
    # print(response)
    if response.status_code != 200:
        print(f"Không thể truy cập URL: {url}")
        return None
    # Phân tích nội dung HTML của trang với BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    product_brand_div = soup.find('div', class_='product_brand')
    brand_name = product_brand_div.find_all('p')[1].text
    product_title = soup.find('h1', class_='product_title').text.strip()
    product_description_div = soup.select_one('.product_description')
    text_content = product_description_div.get_text(strip=True)
    prompt = f"""{text_content} phân tích ra cho tôi các thông tin MÔ TẢ, MÀU SẮC, KÍCH CỠ (chi tiết nếu có), CHẤT LIỆU, XUẤT XỨ, HƯỚNG DẪN BẢO QUẢN, output dưới dạng chuỗi json, không xuống dòng, không chứa ký tự /n thông tin nào không có thì để trống"""
    response = model.generate_content(prompt).text
    response = response.replace('json', '')

    # Chuyển đổi output từ JSON string sang dict
    product_info = json.loads(response)

    # Chuyển đổi các khóa từ tiếng Việt sang tiếng Anh
    result = {
        "brand": brand_name,
        "product_name": product_title,
        "description": product_info.get("MÔ TẢ", ""),
        "color": product_info.get("MÀU SẮC", ""),
        "size": product_info.get("KÍCH CỠ", ""),
        "material": product_info.get("CHẤT LIỆU", ""),
        "origin": product_info.get("XUẤT XỨ", ""),
        "care_instructions": product_info.get("HƯỚNG DẪN BẢO QUẢN", ""),
        "url": url
    }

    # Xử lý thông tin giá
    price_div = soup.find('div', id='static_price_div')
    text_content = price_div.get_text(strip=True)
    
    orginal_price = 0
    discount_price = 0
    discount_percent = 0
    
    if "/g" in text_content or '/kg' in text_content or '/G' in text_content or '/pc' in text_content:
        discount_price = int(re.search(r'\d{1,3}(?:,\d{3})*', text_content).group().replace(',', ''))
        orginal_price = discount_price
        discount_percent = 0
    else:
        price = re.findall(r'\d{1,3}(?:,\d{3})*', text_content)
        discount_price = int(price[1].replace(',', ''))
        orginal_price = int(price[0].replace(',', ''))
        discount_percent = round((-(discount_price - orginal_price) / orginal_price) * 100)
    
    result["orginal_price"] = str(orginal_price) + " VND"
    result["discount_price"] = str(discount_price) + " VND"
    result["discount_percent"] = str(discount_percent) + "%"
    
    time.sleep(10)
    return result

def read_urls_from_file(file_path):
    with open(file_path, 'r') as file:
        urls = file.readlines()
    return [url.strip() for url in urls]

def save_to_excel(product_data, output_file):
    df = pd.DataFrame(product_data)
    df.to_excel(output_file, index=False)

def main():
    url_file = 'product_links.txt'  # Đường dẫn đến file chứa danh sách URL
    output_file = 'products_2.xlsx'  # Đường dẫn đến file Excel kết quả
    
    urls = read_urls_from_file(url_file)
    # urls = ['https://www.cosmodern.vn/product/i-lng-necklace-fmfsx']
    # Danh sách để chứa thông tin sản phẩm tạm thời
    product_data = []

    for url in urls:
        try:
            product_info = get_product_info(url)
            if product_info is None:
                continue
            product_data.append(product_info)
            
            # Lưu thông tin sản phẩm vào file Excel sau khi thêm vào danh sách
            save_to_excel(product_data, output_file)
            print(f"Đã lưu thông tin sản phẩm từ URL: {url}")
        except Exception as e:
            print(f"Lỗi khi lấy thông tin sản phẩm từ URL: {url}")
            print(e)

    print(f"Thông tin sản phẩm đã được lưu vào {output_file}")

if __name__ == "__main__":
    main()
