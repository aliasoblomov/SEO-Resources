
import os
import pandas as pd
from googleapiclient.discovery import build

# API Key
API_KEY = '*******************************'

# ساخت کانکشن به یوتیوب API
youtube = build('youtube', 'v3', developerKey=API_KEY)

def is_persian(text):
 """
 بررسی می‌کند که آیا متن شامل کاراکترهای فارسی است یا خیر.
 """
 persian_chars = "آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی"
 return any(char in text for char in persian_chars)

def get_channel_info(channel_id):
 """
 دریافت اطلاعات کانال یوتیوب بر اساس ID.
 """
 try:
 request = youtube.channels().list(
 part="snippet,contentDetails,statistics",
 id=channel_id
 )
 response = request.execute()

 if 'items' not in response or len(response['items']) == 0:
 return None

 channel_info = response['items'][0]
 channel_url = f"https://www.youtube.com/channel/{channel_info['id']}"
 description = channel_info['snippet']['description']

 # بررسی فارسی بودن کانال بر اساس توضیحات و نام
 if not (is_persian(channel_info['snippet']['title']) or is_persian(description)):
 return None

 return {
 'Channel Name': channel_info['snippet']['title'],
 'Channel URL': channel_url,
 'Description': description,
 'Subscribers': channel_info['statistics'].get('subscriberCount', 'N/A'),
 'Video Count': channel_info['statistics'].get('videoCount', 'N/A'),
 'View Count': channel_info['statistics'].get('viewCount', 'N/A')
 }
 except Exception as e:
 print(f"⚠️ خطا در دریافت اطلاعات کانال {channel_id}: {e}")
 return None

def get_channel_list(keyword):
 """
 جستجوی کانال‌های یوتیوب مرتبط با یک کلمه کلیدی.
 """
 channels = []
 try:
 request = youtube.search().list(
 part="snippet",
 q=keyword,
 type="channel",
 maxResults=20
 )
 response = request.execute()

 for item in response.get('items', []):
 channel_id = item['snippet']['channelId']
 channel_info = get_channel_info(channel_id)
 if channel_info:
 channels.append(channel_info)

 except Exception as e:
 print(f"⚠️ خطا در جستجوی کلمه '{keyword}': {e}")

 return channels

def save_to_excel(channel_data, filename="youtube_channels_persian.xlsx"):
 """
 ذخیره اطلاعات کانال‌ها در فایل اکسل.
 """
 df = pd.DataFrame(channel_data)
 df.to_excel(filename, index=False)
 print(f"✅ اطلاعات کانال‌های فارسی در فایل '{filename}' ذخیره شد.")

# دسته‌بندی‌ها و کلمات کلیدی مربوطه
categories = {
 "آشپزی": ["آشپزی ایرانی", "دستور پخت غذاهای ایرانی", "آشپزی خانگی فارسی"],
 "لایف استایل": ["زندگی روزمره ایرانی", "لایف استایل فارسی", "مد و فشن ایرانی"],
 "سرگرمی": ["طنز ایرانی", "کمدی ایرانی", "استندآپ کمدی فارسی", "شوخی یوتیوب"]
}

# جستجو و جمع‌آوری اطلاعات کانال‌ها
all_channels = []
for category, keywords in categories.items():
 print(f"🔎 در حال جستجوی کانال‌های مرتبط با {category} ...")
 for keyword in keywords:
 channels = get_channel_list(keyword)
 for channel in channels:
 channel["Category"] = category # افزودن دسته‌بندی به اطلاعات کانال
 all_channels.extend(channels)

# ذخیره اطلاعات در اکسل
save_to_excel(all_channels)
