import feedparser
import requests
import os
import urllib.parse

def get_news():
    # 1. 쿼리 그룹을 세분화하여 글로벌 기업 소식을 꼼꼼히 수집합니다.
    queries = [
        # 전문지 그룹
        '오토헤럴드 OR 모터그래프 OR 오토데일리 when:2d',
        
        # 일반 신차 및 업계 동향
        '자동차 "신차" OR "출시" OR "전기차" when:2d',
        
        # 핵심 관심사 (현대차, 기아, 도요타, 테슬라, BYD) + 전략 키워드
        '(현대차 OR 기아 OR 도요타 OR TOYOTA OR 테슬라 OR TESLA OR BYD) ("투자" OR "SDV" OR "전략" OR "개발") when:2d'
    ]
    
    all_entries = []
    for q in queries:
        encoded_query = urllib.parse.quote(q)
        rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=ko&gl=KR&ceid=KR:ko"
        feed = feedparser.parse(rss_url)
        all_entries.extend(feed.entries)

    if not all_entries: return []

    high_priority = [] # 전문지 및 글로벌 기업 전략 뉴스
    general_news = []  # 일반 자동차 뉴스
    seen_links = set()

    # 필터링 및 분류 키워드
    special_media = ['오토헤럴드', '모터그래프', '오토데일리']
    core_companies = ['현대차', '기아', '도요타', 'TOYOTA', '테슬라', 'TESLA', 'BYD']
    strategy_keys = ['투자', 'SDV', '전략', '개발', '공시', '실적', '분석']

    for entry in all_entries:
        if entry.link in seen_links: continue
        seen_links.add(entry.link)
            
        news_item = f"▶ {entry.title}\n🔗 {entry.link}"
        
        # 제목에 전문지 매체명이 있거나, 주요 기업 + 전략 키워드가 포함된 경우 상단 배치
        title_upper = entry.title.upper()
        is_special_media = any(m in entry.title for m in special_media)
        is_core_content = any(c in title_upper for c in core_companies) and \
                          any(k in entry.title for k in strategy_keys)
        
        if is_special_media or is_core_content:
            high_priority.append(news_item)
        else:
            general_news.append(news_item)

    # 메시지 구성 (글자 수 제한을 고려해 분할 전송)
    chunks = []
    
    if high_priority:
        # 글로벌 전략 뉴스는 중요하므로 최대 15개까지 확보
        chunks.append("🎯 [글로벌 전략 및 전문지 리포트] 🎯\n\n" + "\n\n".join(high_priority[:15]))
        
    if general_news:
        # 일반 동향은 8개로 균형 유지
        chunks.append("📰 [주요 업계 및 신차 동향] 📰\n\n" + "\n\n".join(general_news[:8]))
        
    return chunks

# send_telegram 함수는 이전과 동일하게 유지됩니다.
