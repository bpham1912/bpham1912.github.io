# Trưa Nay Ăn Gì 🍜

CS-style lunch roulette — open a case, choose lunch.

**Main website:** https://truanayangi.com (Cloudflare + GCP).  
**GitHub Pages entry point:** https://truanayangi-com.github.io/truanayangi/ → https://truanayangi.com/

This repository was transferred from `nagisanzenin/truanayangi`, preserving its Git history and community. The current application is a static frontend with **no account, login, backend or production API dependency**. Preferences, custom dishes and browser-local spin totals use versioned cookies, not server storage. Clearing cookies resets them. The historical global community count belongs to the main website, not this local app.

## Chạy local / Run locally

```sh
git clone https://github.com/truanayangi-com/truanayangi.git
cd truanayangi
pnpm install --frozen-lockfile
pnpm start
```

Mở **http://127.0.0.1:5173**. Nếu cổng đang bận, dùng `pnpm start --port 5188` rồi mở http://127.0.0.1:5188. Không cần `.env`, OAuth client, database, tài khoản cloud hay backend. Dùng Node.js 22.12+ và phiên bản pnpm ghi trong package.json.

Ứng dụng tự lưu bộ lọc, ngôn ngữ, âm thanh, danh sách món, món gần nhất và lượt quay bằng cookie. Thay đổi danh sách món được lưu ngay, không có nút đăng nhập hoặc yêu cầu bấm lưu. Lượt quay chỉ thuộc trình duyệt này. Nếu cookie bị chặn hoặc dữ liệu quá lớn, giao diện báo chưa lưu.

The dev and preview servers bind to **127.0.0.1** and use fixed ports. After dependencies are installed, the app needs no remote API: scripts, images and sounds are served locally. Maps, GrabFood and GitHub links only open external websites when clicked.

```sh
pnpm test
pnpm build
pnpm preview
```

The production build can be previewed at http://127.0.0.1:4173. Use a local HTTP server rather than opening `index.html` with `file://`, so browser cookies and JavaScript modules work correctly.

## GitHub Pages

GitHub Pages remains a redirect to https://truanayangi.com/. Publish **only `pages-redirect/`** to `gh-pages`; never deploy the local app build there. The actual production website stays on Cloudflare + GCP and uses the three private repositories. There is no custom Actions pipeline, Entire integration or GitHub Projects requirement.

## Storage

Cookies are host-only, scoped to the application path, `SameSite=Lax`, `Secure` on HTTPS, and expire after one year. Each encoded value is bounded to 3,500 bytes; oversized custom pools are rejected without replacing the previous saved pool. Some browser storage policies can shorten retention. Save only meal preferences, never sensitive personal data. Cookie contents are sent with requests to the static host by the browser. There is no cross-device sync or shared global counter in this version.

The three production repositories (`web`, `server`, `infrastructure`) remain private. No production database, secrets or private Git history is included here. Backend files can still be found in the preserved historical commits, but are not used or deployed by this app.

See [ATTRIBUTION.md](ATTRIBUTION.md) for original authorship and third-party assets.
