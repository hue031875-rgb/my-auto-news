import feedparser
import requests
import os
import urllib.parse

def get_news():
    # 전문 매체(오토헤럴드, 모터그래프)를 검색어 정면에 배치하여 수집 확률을 극대화합니다.
    # 'source:' 연산자를 써서 해당 매체의 기사를 직접 타겟팅합니다.
    target_media = "(source:오토헤럴드 OR source:모터그래프 OR source:오토데일리)"
    keywords = "(현대차 OR 테슬라 OR SDV OR 자율주행 OR 전기차)"
    analysis_keys = "(투자 OR 전략 OR 분석 OR 전망 OR 기획)"
    
    # 이 셋을 조합하여 가장 강력한 검색식을 만듭니다.
    query = f"{target_media} OR ({keywords} AND {analysis_keys})"
    
    encoded_query = urllib.parse.quote(query)
    rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=ko&gl=KR&ceid=KR:ko"
    
    feed = feedparser.parse(rss_url)
    
    high_priority = []
    normal_news = []
    
    priority_keywords = ['투자', '전략', '분석', '기획', '전망', '리포트', '특징주']
    filter_words = ['중고차', '렌트', '리스', '할부', '시승기', '판매합니다', '이벤트']

    # 수집 개수를 30개로 늘려 전문지 기사가 누락되지 않게 합니다.
    for entry in feed.entries[:30]:
        if any(word in entry.title for word in filter_words):
            continue
            
        news_item = f"▶ {entry.title}\n🔗 {entry.link}"
        
        # 제목에 '오토헤럴드'나 '모터그래프'가 포함되어 있거나 분석 키워드가 있으면 상단으로!
        if any(key in entry.title for key in priority_keywords) or \
           any(media in entry.title for media in ['오토헤럴드', '모터그래프']):
            high_priority.append(news_item)
        else:
            normal_news.append(news_item)

    final_message = []
    if high_priority:
        final_message.append("🎯 [핵심 분석 및 전문지 소식] 🎯")
        final_message.extend(high_priority[:6]) # 중요한 소식은 조금 더 많이 보여줍니다.
        final_message.append("\n" + "="*20 + "\n")
        
    if normal_news:
        final_message.append("📰 [주요 업계 동향] 📰")
        final_message.extend(normal_news[:4])
        
    return final_message

# (이하 send_telegram 함수는 이전과 동일합니다)
def send_telegram():
    token = str(os.environ.get('BOT_TOKEN')).strip()
    chat_id = str(os.environ.get('USER_ID')).strip()
    
    news_list = get_news()
    
    if not news_list:
        message = "오늘의 업데이트된 자동차 뉴스가 없습니다."
    else:
        message = "🚗 [자동차 산업 고퀄리티 요약] 🚗\n\n" + "\n\n".join(news_list)

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, data={"chat_id": chat_id, "text": message, "disable_web_page_preview": True})

if __name__ == "__main__":
    send_telegram()
