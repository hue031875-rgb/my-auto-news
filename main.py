import feedparser
import requests
import os
import urllib.parse

def get_news():
    queries = [
        '오토헤럴드 when:2d',
        '모터그래프 when:2d',
        '현대차 "투자" OR "전략" when:2d'
    ]
    
    all_entries = []
    for q in queries:
        encoded_query = urllib.parse.quote(q)
        rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=ko&gl=KR&ceid=KR:ko"
        feed = feedparser.parse(rss_url)
        all_entries.extend(feed.entries)

    if not all_entries:
        return []

    high_priority = []
    normal_news = []
    seen_links = set()

    for entry in all_entries[:60]:
        if entry.link in seen_links: continue
        seen_links.add(entry.link)
            
        news_item = f"▶ {entry.title}\n🔗 {entry.link}"
        if any(media in entry.title for media in ['오토헤럴드', '모터그래프', '오토데일리']) or \
           any(key in entry.title for key in ['투자', '전략', '분석', '기획', '전망', '공시', 'SDV']):
            high_priority.append(news_item)
        else:
            normal_news.append(news_item)

    # 메시지를 구성합니다.
    final_chunks = []
    
    if high_priority:
        chunk = "🎯 [전문지 및 핵심 분석] 🎯\n\n" + "\n\n".join(high_priority[:15])
        final_chunks.append(chunk)
        
    if normal_news:
        chunk = "📰 [주요 업계 동향] 📰\n\n" + "\n\n".join(normal_news[:10])
        final_chunks.append(chunk)
        
    return final_chunks

def send_telegram():
    token = str(os.environ.get('BOT_TOKEN', '')).strip()
    chat_id = str(os.environ.get('USER_ID', '')).strip()
    chunks = get_news()
    
    if not chunks:
        print("전송할 뉴스가 없습니다.")
        return

    for message in chunks:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        # 글자 수 제한 안전장치: 혹시 모르니 한 번 더 자릅니다.
        payload = {"chat_id": chat_id, "text": message[:4000], "disable_web_page_preview": True}
        response = requests.post(url, data=payload)
        print(f"전송 결과: {response.status_code}")

if __name__ == "__main__":
    send_telegram()
