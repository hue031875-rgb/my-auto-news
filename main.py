import feedparser
import requests
import os

def get_news():
    # 수집하고 싶은 키워드를 설정합니다.
    query = "현대차|테슬라|BYD|SDV|자율주행|자동차투자"
    rss_url = f"https://news.google.com/rss/search?q={query}&hl=ko&gl=KR&ceid=KR:ko"
    feed = feedparser.parse(rss_url)
    all_news = []
    
    # 제외하고 싶은 단어가 포함된 뉴스는 거릅니다.
    filter_words = ['중고차', '렌트', '리스', '할부', '시승기', '판매합니다']

    for entry in feed.entries[:15]:
        if not any(word in entry.title for word in filter_words):
            all_news.append(f"▶ {entry.title}\n🔗 {entry.link}")
            if len(all_news) >= 6: # 최대 6개까지만 가져옵니다.
                break
    return all_news

def send_telegram():
    # GitHub Secrets에서 새 이름으로 저장한 값을 가져옵니다.
    token = os.environ.get('BOT_TOKEN')
    chat_id = os.environ.get('USER_ID')
    
    news_list = get_news()
    
    if not news_list:
        message = "오늘의 주요 자동차 산업 뉴스가 없습니다."
    else:
        message = "🚗 [자동차 산업 트렌드 요약] 🚗\n\n" + "\n\n".join(news_list)

    # 텔레그램 메시지 전송 주소를 생성합니다.
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    # 메시지를 전송하고 결과를 로그에 남깁니다.
    response = requests.post(url, data={"chat_id": chat_id, "text": message})
    
    print("-" * 30)
    print(f"텔레그램 응답 결과: {response.text}")
    print("-" * 30)

if __name__ == "__main__":
    send_telegram()
