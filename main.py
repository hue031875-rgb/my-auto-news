import feedparser
import requests
import os

def get_news():
    query = "현대차|테슬라|BYD|SDV|자율주행|자동차투자"
    rss_url = f"https://news.google.com/rss/search?q={query}&hl=ko&gl=KR&ceid=KR:ko"
    feed = feedparser.parse(rss_url)
    all_news = []
    filter_words = ['중고차', '렌트', '리스', '할부', '시승기', '판매합니다']

    for entry in feed.entries[:15]:
        if not any(word in entry.title for word in filter_words):
            all_news.append(f"▶ {entry.title}\n🔗 {entry.link}")
            if len(all_news) >= 6:
                break
    return all_news

def send_telegram():
    # .strip()을 붙여서 혹시 모를 눈에 안 보이는 찌꺼기 문자를 강제로 제거합니다.
    token = str(os.environ.get('BOT_TOKEN')).strip()
    chat_id = str(os.environ.get('USER_ID')).strip()
    
    news_list = get_news()
    message = "🚗 [자동차 산업 트렌드 요약] 🚗\n\n" + "\n\n".join(news_list) if news_list else "오늘의 뉴스가 없습니다."

    # 가장 안전한 방식으로 URL을 생성합니다.
    url = "https://api.telegram.org/bot" + token + "/sendMessage"
    
    # 전송 시도
    response = requests.post(url, data={"chat_id": chat_id, "text": message})
    
    print("-" * 30)
    print(f"사용된 토큰 앞글자: {token[:5]}***") # 보안상 앞부분만 출력해서 확인
    print(f"텔레그램 응답: {response.text}")
    print("-" * 30)

if __name__ == "__main__":
    send_telegram()
