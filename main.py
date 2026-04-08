import feedparser
import requests
import os
import urllib.parse

def get_news():
    # 1. 48시간(2d)으로 범위를 넓혀서 정보를 풍성하게 가져옵니다.
    # 전문 매체 기사와 주요 키워드 기사를 동시에 훑습니다.
    query = '(오토헤럴드 OR 모터그래프 OR "현대차 투자" OR "SDV 전략" OR "자율주행 분석") when:2d'
    
    encoded_query = urllib.parse.quote(query)
    rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=ko&gl=KR&ceid=KR:ko"
    
    feed = feedparser.parse(rss_url)
    
    high_priority = []
    normal_news = []
    
    # 분석 키워드 및 전문 매체 리스트
    priority_keywords = ['투자', '전략', '분석', '기획', '전망', '리포트', '특징주', '공시']
    special_media = ['오토헤럴드', '모터그래프', '오토데일리', 'Auto Herald', 'Motor Graph']

    # 수집량을 50개로 늘려 48시간치 데이터를 충분히 확보합니다.
    for entry in feed.entries[:50]:
        # 제목에 매체 이름이 있는지 확인
        is_special = any(media in entry.title for media in special_media)
        # 제목에 분석 키워드가 있는지 확인
        is_priority = any(key in entry.title for key in priority_keywords)
        
        news_item = f"▶ {entry.title}\n🔗 {entry.link}"
        
        # 전문지 기사거나 고급 분석 기사라면 상단 배치!
        if is_special or is_priority:
            if news_item not in high_priority:
                high_priority.append(news_item)
        else:
            if news_item not in normal_news:
                normal_news.append(news_item)

    final_message = []
    if high_priority:
        final_message.append("🎯 [핵심 분석 및 전문지 소식 (48h)] 🎯")
        # 풍성해진 만큼 핵심 소식은 10개까지 보여줍니다.
        final_message.extend(high_priority[:10])
        final_message.append("\n" + "="*20 + "\n")
        
    if normal_news:
        final_message.append("📰 [주요 업계 동향] 📰")
        final_message.extend(normal_news[:5])
        
    return final_message

# (이하 send_telegram 함수는 동일)
