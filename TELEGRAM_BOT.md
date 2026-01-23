# Telegram Support Bot - Render.com Setup Guide

## Overview
Bot endi Render.com'da to'liq avtomatik ishlaydi. Har safar deploy qilganingizda FAQ ma'lumotlari avtomatik yuklanadi.

## Render.com'da sozlash

1. **Environment Variables**:
   Render dashboard'da quyidagi o'zgaruvchini qo'shing:
   - `BOT_TOKEN`: `8484894535:AAGE2gQ3ujvnKxzK7Jhn0QK5rvl5c4xCIaA`

2. **Deploy**:
   GitHub'ga push qiling. `build.sh` avtomatik ravishda:
   - Kutubxonalarni o'rnatadi
   - Bazani yangilaydi (`migrate`)
   - FAQ ma'lumotlarini yuklaydi (`load_faq`)

3. **Webhook ulanishi**:
   Deploy tugagandan so'ng, ushbu URL'ni brauzerda bir marta oching (O'z URL'ingiz bilan):
   `https://api.telegram.org/bot8484894535:AAGE2gQ3ujvnKxzK7Jhn0QK5rvl5c4xCIaA/setWebhook?url=https://SIZNING_APP_NOMINGIZ.onrender.com/webhook/`

## Muhim eslatma
Agar bot javob bermasa, Render logs bo'limini tekshiring. `BOT_TOKEN` to'g'ri o'rnatilganiga ishonch hosil qiling.
