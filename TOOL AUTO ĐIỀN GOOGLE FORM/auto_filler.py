# -*- coding: utf-8 -*-
"""
Module xử lý logic sinh câu trả lời và tự động gửi Google Form
Hỗ trợ Form mới: TEST TINH DẦU THUẦN TRÀM (1FAIpQLScs3jWikhQq5GAWnIiZkGfIySrp5veY9fY1HoFDjMXnJ-WSlg)
Và Form đầy đủ: TINH DẦU THUẦN TRÀM (1FAIpQLSdsQtBys6Wa4UjKoQW6xt_JyR7q0nWhb3X9py3TBYd-mISa9w)
"""

import urllib.request
import urllib.parse
import re
import random
import time
import ssl

# Form mới (Mặc định)
DEFAULT_FORM_ID = "1FAIpQLScs3jWikhQq5GAWnIiZkGfIySrp5veY9fY1HoFDjMXnJ-WSlg"
FORM_VIEW_URL = f"https://docs.google.com/forms/d/e/{DEFAULT_FORM_ID}/viewform"
FORM_POST_URL = f"https://docs.google.com/forms/d/e/{DEFAULT_FORM_ID}/formResponse"

DESKTOP_USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
]

try:
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
except Exception:
    ssl_context = None

_cached_fbzx = ""
_last_fbzx_time = 0

def extract_form_id(url):
    """Trích xuất Google Form ID từ đường link bất kỳ"""
    match = re.search(r'/forms/d/e/([a-zA-Z0-9_-]+)', url)
    if match:
        return match.group(1)
    match_d = re.search(r'/forms/d/([a-zA-Z0-9_-]+)', url)
    if match_d:
        return match_d.group(1)
    return DEFAULT_FORM_ID

def get_fbzx_token(view_url=FORM_VIEW_URL, timeout=10, force_refresh=False):
    """Lấy token fbzx mới từ trang viewform, có cache 5 phút để tối ưu tốc độ"""
    global _cached_fbzx, _last_fbzx_time
    now = time.time()
    if not force_refresh and _cached_fbzx and (now - _last_fbzx_time < 300):
        return _cached_fbzx

    req = urllib.request.Request(
        view_url,
        headers={'User-Agent': random.choice(DESKTOP_USER_AGENTS)}
    )
    try:
        kwargs = {"timeout": timeout}
        if ssl_context:
            kwargs["context"] = ssl_context
        with urllib.request.urlopen(req, **kwargs) as response:
            html = response.read().decode('utf-8', errors='ignore')
            match = re.search(r'name="fbzx"\s+value="([^"]+)"', html)
            if match:
                _cached_fbzx = match.group(1)
                _last_fbzx_time = now
                return _cached_fbzx
    except Exception:
        pass

    if _cached_fbzx:
        return _cached_fbzx
    return "-7809642075571005138"

def generate_response_for_new_test_form():
    """
    Sinh câu trả lời cho form TEST (link: https://docs.google.com/forms/d/e/1FAIpQLScs3jWikhQq5GAWnIiZkGfIySrp5veY9fY1HoFDjMXnJ-WSlg/viewform)
    Gồm 3 câu hỏi:
    1. Độ tuổi (entry.915254597)
    2. Vị trí trong gia đình (entry.1605022628)
    3. Nơi mua (entry.1450783826 - Checkbox)
    """
    age = random.choices(
        ['26 đến 35 tuổi', '22 đến 25 tuổi', 'trên 36 tuổi', 'Dưới 22 tuổi'],
        weights=[55, 25, 12, 8]
    )[0]

    family_role = random.choices(
        ['Mẹ', 'Bố', 'Anh/ chị', 'Ông/ bà', 'Khác'],
        weights=[55, 25, 10, 6, 4]
    )[0]

    buy_places_pool = [
        'Các nhà thuốc',
        'Các cửa hàng mẹ và bé',
        'Các trang thương mại điện tử (Shopee, Tiktok shop, Lazada,...)',
        'Các cửa hàng trực tuyến trên mạng xã hội (Facebook, Instagram,...)',
        'Mua qua người quen/đại lý'
    ]
    num_places = random.choices([1, 2, 3], weights=[35, 50, 15])[0]
    buy_places = random.sample(buy_places_pool, k=num_places)

    return {
        "form_type": "test_form_3q",
        "age": age,
        "family_role": family_role,
        "buy_places": buy_places
    }

def generate_random_response(form_url=None):
    """
    Tự động nhận diện form và sinh câu trả lời phù hợp.
    """
    form_id = extract_form_id(form_url) if form_url else DEFAULT_FORM_ID

    # Nếu là Form TEST 3 câu hỏi
    if form_id == "1FAIpQLScs3jWikhQq5GAWnIiZkGfIySrp5veY9fY1HoFDjMXnJ-WSlg":
        return generate_response_for_new_test_form()

    # Nếu là Form khảo sát gốc 17 câu hỏi
    age = random.choices(
        ['26 đến 35 tuổi', '22 đến 25 tuổi', 'trên 36 tuổi', 'Dưới 22 tuổi'],
        weights=[55, 25, 12, 8]
    )[0]
    has_child = random.choices(
        ['Có con từ 1 đến dưới 3 tuổi', 'Có con dưới 1 tuổi', 'Có con trên 3tuổi', 'Chưa có con'],
        weights=[40, 30, 18, 12]
    )[0]
    job = random.choices(
        ['Nhân viên văn phòng', 'Mẹ bỉm toàn thời gian', 'Lao động phổ thông', 'Khác'],
        weights=[45, 28, 15, 12]
    )[0]
    child_in_family = 'Có' if has_child != 'Chưa có con' else random.choices(['Có', 'Không'], weights=[40, 60])[0]
    family_role = 'Mẹ' if job == 'Mẹ bỉm toàn thời gian' else random.choices(
        ['Mẹ', 'Bố', 'Anh/ chị', 'Ông/ bà', 'Khác'], weights=[58, 22, 12, 5, 3]
    )[0]
    ever_used = random.choices(['Thường xuyên', 'Thỉnh thoảng', 'Đã từng', 'Chưa từng'], weights=[40, 38, 18, 4])[0]

    buy_places_pool = [
        'Các nhà thuốc',
        'Các cửa hàng mẹ và bé',
        'Các trang thương mại điện tử (Shopee, Tiktok shop, Lazada,...)',
        'Các cửa hàng trực tuyến trên mạng xã hội (Facebook, Instagram,...)',
        'Mua qua người quen/đại lý'
    ]
    buy_places = random.sample(buy_places_pool, k=random.choices([1, 2, 3], weights=[35, 50, 15])[0])

    use_cases_pool = [
        'Dùng để giữ ấm cơ thể khi thay đổi thời tiết, sau khi tắm, khi đi ra ngoài',
        'Dùng để phòng côn trùng đốt, xua đuổi muỗi',
        'Xông mũi giải cảm, giảm ngạt mũi',
        'Dùng để xông phòng tạo hương thơm thư giãn'
    ]
    use_cases = random.sample(use_cases_pool, k=random.choices([1, 2, 3], weights=[20, 50, 30])[0])

    concern = random.choices(
        [
            'Sợ mua phải hàng giả/hàng kém chất lượng',
            'Tinh dầu gây nóng, rát, kích ứng da em bé',
            'Bao bì không rõ ràng, thông tin không đầy đủ',
            'Giá bán quá cao'
        ],
        weights=[52, 28, 12, 8]
    )[0]

    situation = random.choices(
        [
            'Không biết sản phẩm có phải tinh dầu tràm thật hay không',
            'Không gặp phải trường hợp nào',
            'Không biết nên sử dụng như thế nào',
            'Không biết cách sử dụng'
        ],
        weights=[48, 26, 14, 12]
    )[0]

    priority_pool = [
        'An toàn cho trẻ nhỏ', 'Nguồn gốc  rõ ràng', 'Được đánh giá tốt',
        'Có thương hiệu uy tín', 'Giấy tờ pháp lý rõ ràng', 'Giá cả hợp lý'
    ]
    priorities = random.sample(priority_pool, k=random.choices([1, 2, 3], weights=[15, 50, 35])[0])

    product_care_pool = [
        'Thành phần an toàn, thiên nhiên', 'Được kiểm nghiệm đầy đủ', 'Thông tin nguồn gốc rõ ràng',
        'Có mã QR truy suất sản phẩm', 'Hướng dẫn sử dụng dễ hiểu', 'Giá cả hợp lý',
        'Nắp dạng nhỏ giọt tiện dụng', 'Thiết kế sản phẩm hài hoà, bắt mắt'
    ]
    product_cares = random.sample(product_care_pool, k=random.choices([2, 3, 4], weights=[40, 45, 15])[0])

    interest_level = random.choices(
        ['Rất quan tâm', 'Hơi quan tâm', 'Bình thường', 'Hơi không quan tâm', 'Không quan tâm'],
        weights=[68, 24, 6, 1, 1]
    )[0]

    price_range = random.choices(
        ['100.000 vnd - 159.000 vnd', 'Dưới 100.000 vnd', '160.000 vnd - 189.000 vnd', 'Trên 190.000 vnd'],
        weights=[48, 28, 18, 6]
    )[0]

    criteria_pool = [
        'Thành phần nguồn gốc thiên nhiên', 'Được chứng nhận/kiểm nghiệm an toàn',
        'Có nhiều đánh giá tốt', 'Thương hiệu uy tín', 'Được người quen giới thiệu', 'Giá cả hợp lý'
    ]
    criterias = random.sample(criteria_pool, k=random.choices([2, 3, 1], weights=[50, 35, 15])[0])

    return {
        "form_type": "full_form_17q",
        "age": age,
        "has_child": has_child,
        "job": job,
        "child_in_family": child_in_family,
        "family_role": family_role,
        "ever_used": ever_used,
        "buy_places": buy_places,
        "use_cases": use_cases,
        "concern": concern,
        "situation": situation,
        "priorities": priorities,
        "product_cares": product_cares,
        "interest_level": interest_level,
        "price_range": price_range,
        "criterias": criterias
    }

def submit_form(data=None, form_url=None, timeout=12):
    """
    Gửi 1 lượt phản hồi lên Google Form (tự động phát hiện form đang dùng).
    Trả về: (success: bool, message: str, data_used: dict)
    """
    form_id = extract_form_id(form_url) if form_url else DEFAULT_FORM_ID
    post_url = f"https://docs.google.com/forms/d/e/{form_id}/formResponse"
    view_url = f"https://docs.google.com/forms/d/e/{form_id}/viewform"

    if data is None:
        data = generate_random_response(view_url)

    fbzx = get_fbzx_token(view_url, timeout=timeout)

    form_payload = []

    # Xây dựng payload tùy theo loại form
    if form_id == "1FAIpQLScs3jWikhQq5GAWnIiZkGfIySrp5veY9fY1HoFDjMXnJ-WSlg" or data.get("form_type") == "test_form_3q":
        # Form TEST mới (3 câu hỏi, 1 trang duy nhất)
        form_payload.append(('entry.915254597', data['age']))
        form_payload.append(('entry.1605022628', data['family_role']))
        for place in data['buy_places']:
            form_payload.append(('entry.1450783826', place))

        form_payload.extend([
            ('fvv', '1'),
            ('partialResponse', f'[null,null,"{fbzx}"]'),
            ('pageHistory', '0'),
            ('fbzx', fbzx)
        ])
    else:
        # Form khảo sát đầy đủ (17 câu hỏi, 3 trang)
        form_payload.extend([
            ('entry.51667176', data['age']),
            ('entry.229257125', data['has_child']),
            ('entry.927851092', data['job']),
            ('entry.1906236938', data['child_in_family']),
            ('entry.1529778664', data['family_role']),
            ('entry.1771134438', data['ever_used'])
        ])
        for place in data['buy_places']:
            form_payload.append(('entry.1038662519', place))
        for case in data['use_cases']:
            form_payload.append(('entry.446775100', case))

        form_payload.append(('entry.378765434', data['concern']))
        form_payload.append(('entry.1489529101', data['situation']))

        for pri in data['priorities']:
            form_payload.append(('entry.857795582', pri))
        for care in data['product_cares']:
            form_payload.append(('entry.600899757', care))

        form_payload.append(('entry.1461365996', data['interest_level']))
        form_payload.append(('entry.1470425196', data['price_range']))

        for cri in data['criterias']:
            form_payload.append(('entry.1602111775', cri))

        form_payload.extend([
            ('fvv', '1'),
            ('partialResponse', f'[null,null,"{fbzx}"]'),
            ('pageHistory', '0,1,2'),
            ('fbzx', fbzx)
        ])

    user_agent = random.choice(DESKTOP_USER_AGENTS)
    encoded_data = urllib.parse.urlencode(form_payload).encode('utf-8')
    headers = {
        'User-Agent': user_agent,
        'Referer': view_url
    }

    req = urllib.request.Request(post_url, data=encoded_data, headers=headers)

    start_time = time.time()
    try:
        kwargs = {"timeout": timeout}
        if ssl_context:
            kwargs["context"] = ssl_context
        with urllib.request.urlopen(req, **kwargs) as resp:
            elapsed = round(time.time() - start_time, 2)
            if resp.status == 200:
                return True, f"Thành công (HTTP 200, {elapsed}s)", data
            else:
                return False, f"Lỗi HTTP {resp.status}", data
    except urllib.error.HTTPError as e:
        get_fbzx_token(view_url, timeout=timeout, force_refresh=True)
        return False, f"Lỗi HTTP {e.code}: {e.reason}", data
    except Exception as e:
        return False, f"Lỗi kết nối: {str(e)}", data
