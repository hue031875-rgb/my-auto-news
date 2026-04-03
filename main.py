import feedparser
import requests
import os

def get_news():
    # 1. 검색 키워드 최적화 (현대차, 테슬라, SDV, 자율주행, 전기차투자 등)
    query = "현대차 OR 테슬라 OR BYD OR SDV OR 자율주행 OR 자동차투자"
    rss_url = f"https://news.google.com/rss/search?q={query}&hl=ko&gl=KR&ceid=KR:ko"
    
    feed = feedparser.parse(rss_url)
    all_news = []
    
    # 2. 광고 및 불필요한 키워드 필터링 (시승기, 렌트 등 제외)
    filter_words = ['중고차', '렌트', '리스', '할부', '시승기', '판매합니다']

    for entry in feed.entries[:12]: # 12개를 가져와서 필터링
        if not any(word in entry.title for word in filter_words):
            all_news.append(f"▶ {entry.title}\n🔗 {entry.link}")
            if len(all_news) >= 6: # 최종 6개만 선별
                break
    
    return all_news

def send_telegram():
    # GitHub Secrets에 저장한 보안 환경변수 사용
    token = os.environ.get('TELEGRAM_TOKEN')
    chat_id = os.environ.get('CHAT_ID')
    
    news_list = get_news()
    
    if not news_list:
        message = "오늘의 주요 자동차 산업 뉴스가 없습니다."
    else:
        message = "🚗 [오늘의 자동차 산업 트렌드 요약] 🚗\n\n" + "\n\n".join(news_list)

    # 텔레그램 발송
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, data={"chat_id": chat_id, "text": message})

if __name__ == "__main__":
    send_telegram()
