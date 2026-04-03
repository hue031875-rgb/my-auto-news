import feedparser
import requests
import os

def get_news():
    # 검색어 보강: 전문 매체와 핵심 키워드를 조합합니다.
    query = "(현대차 OR 테슬라 OR SDV OR 자율주행 OR 자동차투자) (투자 OR 전략 OR 분석 OR 전망 OR 기획)"
    rss_url = f"https://news.google.com/rss/search?q={query}&hl=ko&gl=KR&ceid=KR:ko"
    feed = feedparser.parse(rss_url)
    
    high_priority = []  # 고급 정보 (투자, 전략 등)
    normal_news = []    # 일반 정보
    
    # 우선순위 키워드 설정
    priority_keywords = ['투자', '전략', '분석', '기획', '전망', '리포트', '특징주']
    # 제외 키워드
    filter_words = ['중고차', '렌트', '리스', '할부', '시승기', '판매합니다', '이벤트']

    for entry in feed.entries[:20]:
        if any(word in entry.title for word in filter_words):
            continue
            
        news_item = f"▶ {entry.title}\n🔗 {entry.link}"
        
        # 제목에 우선순위 키워드가 있으면 상단 그룹으로
        if any(key in entry.title for key in priority_keywords):
            high_priority.append(news_item)
        else:
            normal_news.append(news_item)

    # 상단 3개, 하단 4개 정도로 구성 (최대 7개)
    final_message = []
    if high_priority:
        final_message.append("🎯 [핵심 투자/전략 분석] 🎯")
        final_message.extend(high_priority[:4])
        final_message.append("\n" + "="*20 + "\n") # 구분선
        
    if normal_news:
        final_message.append("📰 [주요 업계 동향] 📰")
        final_message.extend(normal_news[:4])
        
    return final_message

def send_telegram():
    token = str(os.environ.get('BOT_TOKEN')).strip()
    chat_id = str(os.environ.get('USER_ID')).strip()
    
    news_list = get_news()
    
    if not news_list:
        message = "오늘의 업데이트된 자동차 뉴스가 없습니다."
    else:
        message = "🚗 [자동차 산업 고퀄리티 요약] 🚗\n\n" + "\n\n".join(news_list)

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    # 메시지가 너무 길면 텔레그램에서 잘릴 수 있어 나눠서 보낼 수 있도록 설정
    response = requests.post(url, data={"chat_id": chat_id, "text": message, "disable_web_page_preview": True})
    
    print("-" * 30)
    print(f"텔레그램 응답: {response.text}")
    print("-" * 30)

if __name__ == "__main__":
    send_telegram()
