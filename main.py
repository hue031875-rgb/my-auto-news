import feedparser
import requests
import os

def get_news():
    # 검색 키워드 최적화
    query = "현대차|테슬라|BYD|SDV|자율주행|자동차투자"
    rss_url = f"https://news.google.com/rss/search?q={query}&hl=ko&gl=KR&ceid=KR:ko"
    
    feed = feedparser.parse(rss_url)
    all_news = []
    
    # 필터링 단어
    filter_words = ['중고차', '렌트', '리스', '할부', '시승기', '판매합니다']

    for entry in feed.entries[:12]:
        if not any(word in entry.title for word in filter_words):
            all_news.append(f"▶ {entry.title}\n🔗 {entry.link}")
            if len(all_news) >= 6:
                break
    
    return all_news

def send_telegram():
    token = os.environ.get('TELEGRAM_TOKEN')
    chat_id = os.environ.get('CHAT_ID')
    
    # 텔레그램 연결 확인을 위한 테스트용 메시지입니다.
    message = "텔레그램 연결 성공! 이제 뉴스만 받으면 됩니다."

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, data={"chat_id": chat_id, "text": message})

if __name__ == "__main__":
    send_telegram()
