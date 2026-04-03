import feedparser
import requests
import os
import urllib.parse # 주소 변환을 위해 추가했습니다.

def get_news():
    # 검색어 보강: 괄호와 OR를 사용하여 더 정확하게 수집합니다.
    query = "(현대차 OR 테슬라 OR SDV OR 자율주행 OR 자동차투자) (투자 OR 전략 OR 분석 OR 전망 OR 기획)"
    
    # 띄어쓰기 등을 URL 형식에 맞게 안전하게 변환합니다.
    encoded_query = urllib.parse.quote(query)
    rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=ko&gl=KR&ceid=KR:ko"
    
    feed = feedparser.parse(rss_url)
    
    high_priority = []  # 고급 정보 (투자, 전략 등)
    normal_news = []    # 일반 정보
    
    priority_keywords = ['투자', '전략', '분석', '기획', '전망', '리포트', '특징주', '전망']
    filter_words = ['중고차', '렌트', '리스', '할부', '시승기', '판매합니다', '이벤트']

    for entry in feed.entries[:20]:
        if any(word in entry.title for word in filter_words):
            continue
            
        # 매체 정보 추출 (제목 끝에 보통 매체명이 붙습니다)
        news_item = f"▶ {entry.title}\n🔗 {entry.link}"
        
        if any(key in entry.title for key in priority_keywords):
            high_priority.append(news_item)
        else:
            normal_news.append(news_item)

    final_message = []
    if high_priority:
        final_message.append("🎯 [핵심 투자/전략 분석] 🎯")
        final_message.extend(high_priority[:4]) # 분석 기사는 최대 4개
        final_message.append("\n" + "="*20 + "\n")
        
    if normal_news:
        final_message.append("📰 [주요 업계 동향] 📰")
        final_message.extend(normal_news[:4]) # 일반 기사는 최대 4개
        
    return final_message

def send_telegram():
    token = str(os.environ.get('BOT_TOKEN')).strip()
    chat_id = str(os.environ.get('USER_ID')).strip()
    
    news_list = get_news()
    
    if not news_list:
        message = "오늘의 핵심 자동차 뉴스가 없습니다."
    else:
        message = "🚗 [자동차 산업 고퀄리티 요약] 🚗\n\n" + "\n\n".join(news_list)

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    # 미리보기 끄기(disable_web_page_preview)를 설정하여 메시지를 깔끔하게 만듭니다.
    response = requests.post(url, data={
        "chat_id": chat_id, 
        "text": message, 
        "disable_web_page_preview": True
    })
    
    print("-" * 30)
    print(f"텔레그램 응답: {response.text}")
    print("-" * 30)

if __name__ == "__main__":
    send_telegram()
