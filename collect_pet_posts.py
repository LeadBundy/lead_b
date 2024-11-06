import requests
import pandas as pd
import time

TOKEN = 'ваш_токен_доступа'
GROUP_ID = 'идентификатор_группы'
COUNT = 100  # Число постов для анализа

def get_posts(offset=0):
    url = f"https://api.vk.com/method/wall.get?owner_id=-{GROUP_ID}&count={COUNT}&offset={offset}&access_token={TOKEN}&v=5.131"
    response = requests.get(url).json()
    if 'response' in response:
        return response['response']['items']
    return []

def analyze_posts(posts):
    stats = {'date': [], 'likes': [], 'reposts': [], 'comments': [], 'geo': []}
    for post in posts:
        stats['date'].append(post['date'])
        stats['likes'].append(post['likes']['count'])
        stats['reposts'].append(post['reposts']['count'])
        stats['comments'].append(post['comments']['count'])
        geo = post.get('geo', {}).get('coordinates')  # геолокация, если есть
        stats['geo'].append(geo if geo else 'Unknown')
    return pd.DataFrame(stats)

# Сбор данных с постраничной загрузкой для больших объёмов данных
all_posts = []
for i in range(0, 1000, COUNT):
    all_posts.extend(get_posts(i))
    time.sleep(0.5)  # Уменьшение нагрузки на API
stats_df = analyze_posts(all_posts)
print(stats_df.head())  # Отображение собранной статистики
