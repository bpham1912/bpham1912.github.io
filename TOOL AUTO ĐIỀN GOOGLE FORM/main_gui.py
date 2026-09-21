# -*- coding: utf-8 -*-
"""
Giao diện đồ họa (GUI) Tool Tự Động Điền Google Form
Khảo sát: Tinh dầu thuần tràm
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time
import random
import sys
import os

from auto_filler import submit_form, generate_random_response, DEFAULT_FORM_ID

class AutoFillApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TOOL TỰ ĐỘNG ĐIỀN GOOGLE FORM")
        self.root.geometry("820x680")
        self.root.minsize(780, 620)

        # Style & Color Palette
        self.bg_color = "#f4f6f9"
        self.card_bg = "#ffffff"
        self.primary_color = "#1a73e8"
        self.success_color = "#1e8e3e"
        self.danger_color = "#d93025"
        self.text_color = "#202124"
        self.border_color = "#dadce0"

        self.root.configure(bg=self.bg_color)

        # State Variables
        self.is_running = False
        self.is_paused = False
        self.stop_requested = False
        self.worker_thread = None

        self.success_count = 0
        self.fail_count = 0
        self.current_index = 0
        self.total_target = 0
        self.start_time = 0

        self.setup_ui()

    def setup_ui(self):
        # 1. Header Banner
        header_frame = tk.Frame(self.root, bg=self.primary_color, height=75)
        header_frame.pack(fill="x", side="top")
        header_frame.pack_propagate(False)

        title_lbl = tk.Label(
            header_frame,
            text="✨ TOOL AUTO ĐIỀN GOOGLE FORM",
            font=("Segoe UI", 15, "bold"),
            fg="#ffffff",
            bg=self.primary_color
        )
        title_lbl.pack(pady=(12, 2))

        sub_lbl = tk.Label(
            header_frame,
            text="Tự động nhận diện cấu trúc form • Tốc độ cao • Mô phỏng chuẩn người dùng",
            font=("Segoe UI", 9),
            fg="#e8f0fe",
            bg=self.primary_color
        )
        sub_lbl.pack()

        # 2. Main Container
        main_container = tk.Frame(self.root, bg=self.bg_color, padx=15, pady=12)
        main_container.pack(fill="both", expand=True)

        # Config Card
        config_card = tk.LabelFrame(
            main_container,
            text=" ⚙️ Cài đặt gửi phản hồi ",
            font=("Segoe UI", 10, "bold"),
            fg=self.text_color,
            bg=self.card_bg,
            bd=1,
            relief="solid",
            padx=12,
            pady=10
        )
        config_card.pack(fill="x", pady=(0, 10))

        # Row 1: Form Link
        row1 = tk.Frame(config_card, bg=self.card_bg)
        row1.pack(fill="x", pady=4)
        tk.Label(row1, text="Link Google Form:", font=("Segoe UI", 9, "bold"), bg=self.card_bg, width=16, anchor="w").pack(side="left")
        self.url_var = tk.StringVar(value=f"https://docs.google.com/forms/d/e/{DEFAULT_FORM_ID}/viewform")
        self.url_entry = ttk.Entry(row1, textvariable=self.url_var, font=("Segoe UI", 9))
        self.url_entry.pack(side="left", fill="x", expand=True, padx=(5, 0))

        # Row 2: Target count & Delay
        row2 = tk.Frame(config_card, bg=self.card_bg)
        row2.pack(fill="x", pady=6)

        tk.Label(row2, text="Số lượng gửi:", font=("Segoe UI", 9, "bold"), bg=self.card_bg, width=16, anchor="w").pack(side="left")
        self.count_var = tk.IntVar(value=50)
        self.count_spin = ttk.Spinbox(row2, from_=1, to=10000, textvariable=self.count_var, width=10, font=("Segoe UI", 9))
        self.count_spin.pack(side="left", padx=(5, 20))

        tk.Label(row2, text="Thời gian nghỉ giữa mỗi lần (giây):", font=("Segoe UI", 9, "bold"), bg=self.card_bg).pack(side="left")
        self.delay_min_var = tk.DoubleVar(value=1.5)
        self.delay_max_var = tk.DoubleVar(value=3.5)
        self.min_spin = ttk.Spinbox(row2, from_=0.1, to=60.0, increment=0.5, textvariable=self.delay_min_var, width=6, font=("Segoe UI", 9))
        self.min_spin.pack(side="left", padx=(5, 2))
        tk.Label(row2, text="đến", font=("Segoe UI", 9), bg=self.card_bg).pack(side="left", padx=2)
        self.max_spin = ttk.Spinbox(row2, from_=0.2, to=60.0, increment=0.5, textvariable=self.delay_max_var, width=6, font=("Segoe UI", 9))
        self.max_spin.pack(side="left", padx=(2, 0))

        # 3. Stats Dashboard Cards
        stats_frame = tk.Frame(main_container, bg=self.bg_color)
        stats_frame.pack(fill="x", pady=(0, 10))

        self.card_total = self.create_stat_box(stats_frame, "MỤC TIÊU", "0", "#1a73e8")
        self.card_success = self.create_stat_box(stats_frame, "THÀNH CÔNG", "0", "#1e8e3e")
        self.card_fail = self.create_stat_box(stats_frame, "THẤT BÀI", "0", "#d93025")
        self.card_remain = self.create_stat_box(stats_frame, "CÒN LẠI", "0", "#f2994a")

        # 4. Progress Bar
        progress_frame = tk.Frame(main_container, bg=self.bg_color)
        progress_frame.pack(fill="x", pady=(0, 10))
        
        self.prog_lbl = tk.Label(progress_frame, text="Tiến trình: 0%", font=("Segoe UI", 9, "bold"), bg=self.bg_color, fg=self.text_color)
        self.prog_lbl.pack(anchor="w", pady=(0, 2))

        self.progress_bar = ttk.Progressbar(progress_frame, orient="horizontal", mode="determinate")
        self.progress_bar.pack(fill="x", ipady=3)

        # 5. Buttons Frame
        btn_frame = tk.Frame(main_container, bg=self.bg_color)
        btn_frame.pack(fill="x", pady=(0, 10))

        self.start_btn = tk.Button(
            btn_frame,
            text="▶ BẮT ĐẦU CHẠY",
            font=("Segoe UI", 10, "bold"),
            bg="#1e8e3e",
            fg="#ffffff",
            activebackground="#15732e",
            activeforeground="#ffffff",
            bd=0,
            padx=18,
            pady=7,
            cursor="hand2",
            command=self.start_process
        )
        self.start_btn.pack(side="left", padx=(0, 8))

        self.pause_btn = tk.Button(
            btn_frame,
            text="⏸ TẠM DỪNG",
            font=("Segoe UI", 10, "bold"),
            bg="#f2994a",
            fg="#ffffff",
            activebackground="#d47d2f",
            activeforeground="#ffffff",
            bd=0,
            padx=14,
            pady=7,
            cursor="hand2",
            state="disabled",
            command=self.toggle_pause
        )
        self.pause_btn.pack(side="left", padx=(0, 8))

        self.stop_btn = tk.Button(
            btn_frame,
            text="⏹ DỪNG HẲN",
            font=("Segoe UI", 10, "bold"),
            bg="#d93025",
            fg="#ffffff",
            activebackground="#b3261e",
            activeforeground="#ffffff",
            bd=0,
            padx=14,
            pady=7,
            cursor="hand2",
            state="disabled",
            command=self.stop_process
        )
        self.stop_btn.pack(side="left", padx=(0, 8))

        self.clear_log_btn = tk.Button(
            btn_frame,
            text="🗑 Xóa Log",
            font=("Segoe UI", 9),
            bg="#ffffff",
            fg=self.text_color,
            bd=1,
            relief="solid",
            padx=10,
            pady=6,
            cursor="hand2",
            command=self.clear_log
        )
        self.clear_log_btn.pack(side="right")

        # 6. Live Log Box
        log_frame = tk.LabelFrame(
            main_container,
            text=" 📝 Nhật ký gửi (Live Logs) ",
            font=("Segoe UI", 10, "bold"),
            fg=self.text_color,
            bg=self.card_bg,
            bd=1,
            relief="solid",
            padx=8,
            pady=6
        )
        log_frame.pack(fill="both", expand=True)

        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            font=("Consolas", 9),
            bg="#1e1e1e",
            fg="#d4d4d4",
            insertbackground="#ffffff",
            bd=0
        )
        self.log_text.pack(fill="both", expand=True)

        self.log_text.tag_config("SUCCESS", foreground="#4ec9b0")
        self.log_text.tag_config("ERROR", foreground="#f44747")
        self.log_text.tag_config("INFO", foreground="#569cd6")
        self.log_text.tag_config("WARN", foreground="#ce9178")
        self.log_text.tag_config("TIMESTAMP", foreground="#858585")

        self.append_log("INFO", "Hệ thống sẵn sàng! Đã nạp link Google Form mới.")

    def create_stat_box(self, parent, title, initial_val, color):
        box = tk.Frame(parent, bg="#ffffff", bd=1, relief="solid", padx=10, pady=8)
        box.pack(side="left", fill="both", expand=True, padx=4)

        lbl_title = tk.Label(box, text=title, font=("Segoe UI", 8, "bold"), fg="#5f6368", bg="#ffffff")
        lbl_title.pack()

        lbl_val = tk.Label(box, text=initial_val, font=("Segoe UI", 16, "bold"), fg=color, bg="#ffffff")
        lbl_val.pack(pady=(2, 0))

        return lbl_val

    def append_log(self, tag, message):
        now = time.strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{now}] ", "TIMESTAMP")
        self.log_text.insert(tk.END, f"[{tag}] ", tag)
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)

    def clear_log(self):
        self.log_text.delete("1.0", tk.END)

    def update_stats(self):
        self.card_total.config(text=str(self.total_target))
        self.card_success.config(text=str(self.success_count))
        self.card_fail.config(text=str(self.fail_count))
        remain = max(0, self.total_target - (self.success_count + self.fail_count))
        self.card_remain.config(text=str(remain))

        total_done = self.success_count + self.fail_count
        if self.total_target > 0:
            percent = int((total_done / self.total_target) * 100)
            self.progress_bar["value"] = percent
            self.prog_lbl.config(text=f"Tiến trình: {percent}% ({total_done}/{self.total_target})")

    def start_process(self):
        try:
            target = int(self.count_var.get())
            if target <= 0:
                messagebox.showerror("Lỗi", "Vui lòng nhập số lượng lớn hơn 0!")
                return
        except ValueError:
            messagebox.showerror("Lỗi", "Số lượng gửi không hợp lệ!")
            return

        min_d = float(self.delay_min_var.get())
        max_d = float(self.delay_max_var.get())
        if min_d > max_d:
            messagebox.showerror("Lỗi", "Thời gian delay nhỏ nhất không thể lớn hơn delay lớn nhất!")
            return

        target_url = self.url_var.get().strip()
        if not target_url:
            messagebox.showerror("Lỗi", "Link Google Form không được để trống!")
            return

        self.total_target = target
        self.success_count = 0
        self.fail_count = 0
        self.is_running = True
        self.is_paused = False
        self.stop_requested = False
        self.start_time = time.time()

        self.update_stats()
        self.start_btn.config(state="disabled")
        self.pause_btn.config(state="normal", text="⏸ TẠM DỪNG")
        self.stop_btn.config(state="normal")
        self.url_entry.config(state="disabled")
        self.count_spin.config(state="disabled")

        self.append_log("INFO", f"Bắt đầu quy trình gửi {target} phản hồi...")

        self.worker_thread = threading.Thread(target=self.run_worker, args=(target_url,), daemon=True)
        self.worker_thread.start()

    def toggle_pause(self):
        if not self.is_running:
            return
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.pause_btn.config(text="▶ TIẾP TỤC", bg="#1a73e8")
            self.append_log("WARN", "Quy trình đang tạm dừng. Nhấn 'TIẾP TỤC' để tiếp tục.")
        else:
            self.pause_btn.config(text="⏸ TẠM DỪNG", bg="#f2994a")
            self.append_log("INFO", "Tiếp tục gửi phản hồi...")

    def stop_process(self):
        if not self.is_running:
            return
        self.stop_requested = True
        self.append_log("WARN", "Đang dừng quy trình theo yêu cầu của bạn...")
        self.stop_btn.config(state="disabled")

    def run_worker(self, target_url):
        min_delay = float(self.delay_min_var.get())
        max_delay = float(self.delay_max_var.get())

        for i in range(1, self.total_target + 1):
            if self.stop_requested:
                break

            while self.is_paused:
                if self.stop_requested:
                    break
                time.sleep(0.3)

            if self.stop_requested:
                break

            # 1. Sinh dữ liệu phù hợp với link form
            resp_data = generate_random_response(target_url)

            if resp_data.get("form_type") == "test_form_3q":
                summary = f"Lượt #{i}: Tuổi: {resp_data['age']} | Vị trí: {resp_data['family_role']} | Nơi mua: {', '.join(resp_data['buy_places'])}"
            else:
                summary = f"Lượt #{i}: Tuổi: {resp_data['age']} | Con: {resp_data['has_child']} | Nghề: {resp_data['job']}"

            # 2. Gửi form
            ok, msg, _ = submit_form(resp_data, form_url=target_url)

            if ok:
                self.success_count += 1
                self.root.after(0, self.append_log, "SUCCESS", f"{summary} -> {msg}")
            else:
                self.fail_count += 1
                self.root.after(0, self.append_log, "ERROR", f"Lượt #{i} thất bại: {msg}")

            self.root.after(0, self.update_stats)

            # Nghỉ ngẫu nhiên trước lượt tiếp theo
            if i < self.total_target and not self.stop_requested:
                wait_sec = round(random.uniform(min_delay, max_delay), 2)
                time.sleep(wait_sec)

        self.is_running = False
        self.root.after(0, self.on_finished)

    def on_finished(self):
        elapsed = round(time.time() - self.start_time, 1)
        self.start_btn.config(state="normal")
        self.pause_btn.config(state="disabled", text="⏸ TẠM DỪNG", bg="#f2994a")
        self.stop_btn.config(state="disabled")
        self.url_entry.config(state="normal")
        self.count_spin.config(state="normal")

        if self.stop_requested:
            self.append_log("WARN", f"Đã dừng. Tổng cộng: {self.success_count} thành công, {self.fail_count} thất bại ({elapsed}s).")
            messagebox.showinfo("Đã dừng", f"Quy trình đã dừng.\nThành công: {self.success_count}\nThất bại: {self.fail_count}")
        else:
            self.append_log("SUCCESS", f"🎉 HOÀN THÀNH TOÀN BỘ {self.total_target} LƯỢT GỬI TRONG {elapsed} GIÂY!")
            messagebox.showinfo("Hoàn tất", f"Đã hoàn thành gửi form!\n- Thành công: {self.success_count}/{self.total_target}\n- Thất bại: {self.fail_count}\n- Thời gian: {elapsed}s")

def main():
    root = tk.Tk()
    app = AutoFillApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
