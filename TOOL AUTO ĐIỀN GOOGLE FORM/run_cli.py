# -*- coding: utf-8 -*-
"""
Phiên bản chạy dòng lệnh (CLI) của Tool Auto Điền Google Form
"""

import sys
import time
import random
import argparse
from auto_filler import submit_form, generate_random_response, DEFAULT_FORM_ID

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def main():
    parser = argparse.ArgumentParser(description="Tool Auto Điền Google Form - Tinh Dầu Thuần Tràm")
    parser.add_argument("-u", "--url", type=str, default=f"https://docs.google.com/forms/d/e/{DEFAULT_FORM_ID}/viewform", help="Link Google Form")
    parser.add_argument("-n", "--count", type=int, default=None, help="Số lượng lượt điền cần gửi")
    parser.add_argument("--min-delay", type=float, default=1.5, help="Thời gian nghỉ tối thiểu giữa các lần gửi (giây)")
    parser.add_argument("--max-delay", type=float, default=3.5, help="Thời gian nghỉ tối đa giữa các lần gửi (giây)")
    args = parser.parse_args()

    print("=" * 65)
    print("✨ TOOL AUTO ĐIỀN GOOGLE FORM - TINH DẦU THUẦN TRÀM (CLI)")
    print("=" * 65)
    print(f"🔗 Form URL: {args.url}")

    count = args.count
    if count is None:
        try:
            val = input("👉 Nhập số lượng phản hồi cần gửi (mặc định 20): ").strip()
            count = int(val) if val else 20
        except ValueError:
            print("❌ Số lượng không hợp lệ! Dùng mặc định 20.")
            count = 20

    print(f"\n🚀 Bắt đầu gửi {count} phản hồi...")
    print(f"⏱  Delay giữa mỗi lần: từ {args.min_delay}s đến {args.max_delay}s")
    print("-" * 65)

    success_cnt = 0
    fail_cnt = 0
    start_total = time.time()

    try:
        for i in range(1, count + 1):
            data = generate_random_response(args.url)
            if data.get("form_type") == "test_form_3q":
                info = f"Tuổi: {data['age']} | Vị trí: {data['family_role']}"
            else:
                info = f"Tuổi: {data['age']} | Con: {data['has_child']} | Nghề: {data['job']}"

            print(f"[{i}/{count}] Đang gửi... | {info}")
            
            ok, msg, _ = submit_form(data, form_url=args.url)
            if ok:
                success_cnt += 1
                print(f"   -->  [THÀNH CÔNG] {msg}")
            else:
                fail_cnt += 1
                print(f"   -->  [THẤT BẠI] {msg}")

            if i < count:
                wait_time = round(random.uniform(args.min_delay, args.max_delay), 2)
                time.sleep(wait_time)

    except KeyboardInterrupt:
        print("\n\n⚠️ Đã nhận lệnh dừng từ bàn phím (Ctrl+C)!")

    total_time = round(time.time() - start_total, 1)
    print("=" * 65)
    print("🎉 KẾT QUẢ CUỐI CÙNG:")
    print(f"   - Thành công: {success_cnt}/{count}")
    print(f"   - Thất bại:   {fail_cnt}")
    print(f"   - Tổng thời gian: {total_time} giây")
    print("=" * 65)
    input("\nNhấn Enter để thoát...")

if __name__ == "__main__":
    main()
