import feedparser
import requests
import os
import urllib.parse

def get_news():
    # 1. 여러 개의 쿼리를 나누어 검색하여 수집 확률을 극대화합니다.
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
        print("경고: 모든 쿼리에서 수집된 뉴스가 없습니다.")
        return []

    high_priority = []
    normal_news = []
    
    priority_keywords = ['투자', '전략', '분석', '기획', '전망', '공시', 'SDV']
    special_media = ['오토헤럴드', '모터그래프', '오토데일리']

    # 중복 제거를 위한 링크 저장소
    seen_links = set()

    for entry in all_entries[:60]:
        if entry.link in seen_links:
            continue
        seen_links.add(entry.link)
            
        news_item = f"▶ {entry.title}\n🔗 {entry.link}"
        
        is_special = any(media in entry.title for media in special_media)
        is_priority = any(key in entry.title for key in priority_keywords)
        
        if is_special or is_priority:
            high_priority.append(news_item)
        else:
            normal_news.append(news_item)

    final_message = []
    if high_priority:
        final_message.append("🎯 [전문지 및 핵심 분석] 🎯")
        final_message.extend(high_priority[:10])
        final_message.append("\n" + "="*20 + "\n")
        
    if normal_news:
        final_message.append("📰 [주요 업계 동향] 📰")
        final_message.extend(normal_news[:5])
        
    return final_message

def send_telegram():
    token = str(os.environ.get('BOT_TOKEN', '')).strip()
    chat_id = str(os.environ.get('USER_ID', '')).strip()
    
    news_list = get_news()
    
    if not news_list:
        print("전송할 뉴스가 없어 종료합니다.")
        return

    message = "🚗 [자동차 산업 리포트] 🚗\n\n" + "\n\n".join(news_list)
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    response = requests.post(url, data={"chat_id": chat_id, "text": message, "disable_web_page_preview": True})
    
    print(f"텔레그램 전송 시도 결과: {response.status_code}")
    if response.status_code != 200:
        print(f"에러 메시지: {response.text}")

if __name__ == "__main__":
    send_telegram()
