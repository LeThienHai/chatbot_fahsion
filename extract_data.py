from bs4 import BeautifulSoup

html_content = '''
<div class="product_description">
        <div class="fw-400 fz-16 mw-100 overflow-hidden text-left">
          <p dir="ltr" style="line-height:1.38;background-color:#ffffff;margin-top:0pt;margin-bottom:0pt;"><span style="font-size:10pt;font-family:Arial,sans-serif;color:#000000;background-color:#ffffff;font-weight:700;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;">MÔ TẢ</span></p><p dir="ltr" style="line-height:1.38;background-color:#ffffff;margin-top:0pt;margin-bottom:0pt;"><span style="font-size:10pt;font-family:Arial,sans-serif;color:#081c36;background-color:#ffffff;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;">Áo croptop tay dài xếp ly</span></p><p dir="ltr" style="line-height:1.38;background-color:#ffffff;margin-top:0pt;margin-bottom:0pt;"><span style="font-size:10pt;font-family:Arial,sans-serif;color:#081c36;background-color:#ffffff;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"><br></span></p><p dir="ltr" style="line-height:1.38;background-color:#ffffff;margin-top:0pt;margin-bottom:0pt;"><span style="font-size:10pt;font-family:Arial,sans-serif;color:#000000;background-color:#ffffff;font-weight:700;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;">MÀU SẮC&nbsp;</span></p><p dir="ltr" style="line-height:1.38;background-color:#ffffff;margin-top:0pt;margin-bottom:0pt;"><span style="font-size:10pt;font-family:Arial,sans-serif;color:#000000;background-color:#ffffff;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;">White</span></p><p dir="ltr" style="line-height:1.38;background-color:#ffffff;margin-top:0pt;margin-bottom:0pt;"><span style="font-size:10pt;font-family:Arial,sans-serif;color:#000000;background-color:#ffffff;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"><br></span></p><p dir="ltr" style="line-height:1.38;background-color:#ffffff;margin-top:0pt;margin-bottom:0pt;"><span style="font-size: 10pt; font-family: Arial, sans-serif; color: rgb(0, 0, 0); background-color: rgb(255, 255, 255); font-style: normal; font-variant: normal; text-decoration: none; vertical-align: baseline; white-space: pre-wrap;"><b>CHẤT LIỆU</b></span></p><p dir="ltr" style="line-height:1.38;background-color:#ffffff;margin-top:0pt;margin-bottom:0pt;"><font face="Arial, sans-serif"><span style="font-size: 13.3333px; white-space-collapse: preserve;">Cotton</span></font></p><p dir="ltr" style="line-height:1.38;background-color:#ffffff;margin-top:0pt;margin-bottom:0pt;"><font face="Arial, sans-serif"><span style="font-size: 13.3333px; white-space-collapse: preserve;"><br></span></font></p><p dir="ltr" style="line-height:1.38;background-color:#ffffff;margin-top:0pt;margin-bottom:0pt;"><span style="font-size:10pt;font-family:Arial,sans-serif;color:#000000;background-color:#ffffff;font-weight:700;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;">KÍCH CỠ</span></p><p dir="ltr" style="line-height:1.38;background-color:#ffffff;margin-top:0pt;margin-bottom:0pt;"><span style="font-size:10pt;font-family:Arial,sans-serif;color:#000000;background-color:#ffffff;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;">S, M, L</span></p><p dir="ltr" style="line-height:1.38;background-color:#ffffff;margin-top:0pt;margin-bottom:0pt;"><span style="font-size:10pt;font-family:Arial,sans-serif;color:#000000;background-color:#ffffff;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"><br></span></p><p dir="ltr" style="line-height:1.38;background-color:#ffffff;margin-top:0pt;margin-bottom:0pt;"><span style="font-size:10pt;font-family:Arial,sans-serif;color:#000000;background-color:#ffffff;font-weight:700;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;">XUẤT XỨ</span></p><p dir="ltr" style="line-height:1.38;background-color:#ffffff;margin-top:0pt;margin-bottom:0pt;"><span style="font-family: Arial, sans-serif; font-size: 10pt; white-space-collapse: preserve;">Việt Nam </span></p>        </div>
      </div>
'''  # Đoạn mã HTML của bạn ở đây

soup = BeautifulSoup(html_content, 'html.parser')

# Select the div with class 'product_description'
div = soup.select_one('.product_description')

# Get all text content
text_content = div.get_text(strip=True)

print(text_content)

import re

def parse_product_description(text):
    patterns = {
        'description': r'MÔ TẢ(.*?)MÀU SẮC',
        'color': r'MÀU SẮC(.*?)CHẤT LIỆU',
        'material': r'CHẤT LIỆU(.*?)KÍCH CỠ',
        'size': r'KÍCH CỠ(.*?)XUẤT XỨ',
        'origin': r'XUẤT XỨ(.*)'
    }

    result = {}

    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.DOTALL)
        if match:
            result[key] = match.group(1).strip()

    return result

# Example usage
# text_content = "MÔ TẢÁo croptop tay dài xếp lyMÀU SẮCWhiteCHẤT LIỆUCottonKÍCH CỠS, M, LXUẤT XỨViệt Nam"
print(parse_product_description(text_content))
