import os
import time
import json
import logging
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import google.generativeai as genai
import yt_dlp

# --- CẤU HÌNH TỪ BIẾN MÔI TRƯỜNG (SẼ CÀI TRÊN RENDER) ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SHEET_ID = os.getenv("SHEET_ID")
# Google Credentials sẽ được lưu dưới dạng chuỗi JSON trong biến môi trường
GOOGLE_JSON_STRING = os.getenv("GOOGLE_JSON_CREDENTIALS")

# --- CẤU HÌNH LOGGING ---
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- 1. WEB SERVER GIẢ (ĐỂ RENDER KHÔNG TẮT BOT) ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!", 200

def run_flask():
    # Render yêu cầu chạy trên cổng PORT (mặc định 10000)
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- 2. HÀM TẢI VIDEO FACEBOOK (YT-DLP) ---
def download_video(url):
    output_filename = "temp_video.mp4"
    # Xóa file cũ nếu tồn tại
    if os.path.exists(output_filename):
        os.remove(output_filename)
        
    ydl_opts = {
        'outtmpl': output_filename,
        'format': 'best[ext=mp4]', # Ưu tiên MP4
        'quiet': True,
        'no_warnings': True,
        # Fake User Agent để tránh bị FB chặn
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return output_filename
    except Exception as e:
        logging.error(f"Lỗi tải video: {e}")
        return None

# --- 3. HÀM GEMINI PHÂN TÍCH VIDEO ---
def analyze_video(video_path):
    genai.configure(api_key=GEMINI_API_KEY)
    
    # Upload video lên Gemini File API
    logging.info("Đang upload video lên Gemini...")
    video_file = genai.upload_file(path=video_path)
    
    # Chờ video xử lý (State: ACTIVE)
    while video_file.state.name == "PROCESSING":
        time.sleep(2)
        video_file = genai.get_file(video_file.name)

    if video_file.state.name == "FAILED":
        return {"product": "Lỗi xử lý video", "price": "???", "usp": "Lỗi"}

    # Phân tích
    logging.info("Đang phân tích...")
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    
    prompt = """
    Xem video này và trích xuất thông tin ra định dạng JSON (chỉ JSON thuần):
    {
        "product": "Tên sản phẩm chính",
        "price": "Giá bán (nghe âm thanh hoặc nhìn hình, ưu tiên giá KM)",
        "usp": "Điểm mạnh/Lời quảng cáo chính"
    }
    """
    
    try:
        response = model.generate_content([video_file, prompt], generation_config={"response_mime_type": "application/json"})
        # Xóa file trên Gemini sau khi xong để tiết kiệm
        genai.delete_file(video_file.name)
        return json.loads(response.text)
    except Exception as e:
        logging.error(f"Lỗi AI: {e}")
        return {"product": "Lỗi AI", "price": "???", "usp": str(e)}

# --- 4. HÀM LƯU SHEET ---
def save_to_sheet(user, fb_link, data):
    try:
        # Chuyển chuỗi JSON biến môi trường thành Dictionary
        creds_dict = json.loads(GOOGLE_JSON_STRING)
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)
        
        sheet = client.open_by_key(SHEET_ID).get_worksheet(0)
        # Cấu trúc cột: Time, User, Link FB, Tên SP, Giá, USP
        sheet.append_row([
            time.strftime("%Y-%m-%d %H:%M:%S"),
            user,
            fb_link,
            data.get('product', ''),
            data.get('price', ''),
            data.get('usp', '')
        ])
        return True
    except Exception as e:
        logging.error(f"Lỗi Sheet: {e}")
        return False

# --- 5. XỬ LÝ TIN NHẮN TELEGRAM ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    user_name = update.effective_user.first_name
    
    if "facebook.com" in user_text or "fb.watch" in user_text:
        await update.message.reply_text(f"⏳ Đang tải video từ Facebook (có thể mất 10-20s)...")
        
        # 1. Tải Video
        video_path = download_video(user_text)
        
        if video_path:
            await update.message.reply_text(f"🧠 Đang gửi cho Gemini phân tích hình ảnh & âm thanh...")
            
            # 2. Phân tích AI
            ai_result = analyze_video(video_path)
            
            # 3. Lưu Sheet
            save_to_sheet(user_name, user_text, ai_result)
            
            # 4. Báo cáo & Dọn dẹp
            msg = f"✅ **KẾT QUẢ:**\n📦 SP: {ai_result.get('product')}\n💰 Giá: {ai_result.get('price')}\n✨ USP: {ai_result.get('usp')}"
            await update.message.reply_text(msg, parse_mode='Markdown')
            
            # Xóa file tạm trên server
            if os.path.exists(video_path):
                os.remove(video_path)
        else:
            await update.message.reply_text("❌ Không tải được video. (Có thể do video Riêng tư hoặc Facebook chặn IP server).")
    else:
        await update.message.reply_text("Vui lòng gửi link Facebook.")

# --- MAIN ---
if __name__ == '__main__':
    # Chạy Flask ở luồng riêng (Background)
    threading.Thread(target=run_flask).start()
    
    # Chạy Bot Telegram
    app_tele = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app_tele.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Bot đang chạy...")
    app_tele.run_polling()