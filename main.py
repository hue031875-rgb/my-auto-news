import feedparser
import requests
import os

def get_news():
    query = "현대차|테슬라|BYD|SDV|자율주행|자동차투자"
    rss_url = f"https://news.google.com/rss/search?q={query}&hl=ko&gl=KR&ceid=KR:ko"
    feed = feedparser.parse(rss_url)
    all_news = []
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
    
    if not news_list:
        message = "오늘의 주요 자동차 산업 뉴스가 없습니다."
    else:
        message = "🚗 [자동차 산업 트렌드 요약] 🚗\n\n" + "\n\n".join(news_list)

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    response = requests.post(url, data={"chat_id": chat_id, "text": message})
    
    # 이 부분이 핵심입니다! 실행 후 로그에서 결과를 확인할 수 있게 해줍니다.
    print(f"텔레그램 응답 결과: {response.text}")

if __name__ == "__main__":
    send_telegram()
