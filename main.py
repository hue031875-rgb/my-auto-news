    import feedparser
import requests
import os

def get_news():
    # 검색 키워드 최적화 (파이프 기호 '|'를 사용하여 공백 문제 해결)
    query = "현대차|테슬라|BYD|SDV|자율주행|자동차투자"
    rss_url = f"https://news.google.com/rss/search?q={query}&hl=ko&gl=KR&ceid=KR:ko"
    
    feed = feedparser.parse(rss_url)
    all_news = []
    
    # 광고 및 불필요한 키워드 필터링
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
    
    news_list = get_news()
    
    # 기존 if/else 문을 싹 지우고 아래 한 줄만 남겨보세요.
message = "텔레그램 연결 성공! 이제 뉴스만 받으면 됩니다."

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, data={"chat_id": chat_id, "text": message})

if __name__ == "__main__":
    send_telegram()
