import feedparser
import requests
import os
import urllib.parse

def get_news():
    # 1. 고퀄리티 기사 수집을 위한 '다중 경로' 쿼리
    queries = [
        # [그룹 A] 자동차 전문 매체 (오토헤럴드, 모터그래프, 오토데일리)
        '오토헤럴드 OR 모터그래프 OR 오토데일리 when:2d',
        
        # [그룹 B] 글로벌 5대 기업의 핵심 전략/개발 (한글+영어 혼용으로 수집 극대화)
        '(현대차 OR 기아 OR 도요타 OR TOYOTA OR 테슬라 OR TESLA OR BYD) ("투자" OR "SDV" OR "전략" OR "개발" OR "플랫폼") when:2d',
        
        # [그룹 C] 시장 분석 및 기술 동향
        '자동차 "자율주행" OR "전기차" OR "신기술" when:2d'
    ]
    
    all_entries = []
    for q in queries:
        encoded_query = urllib.parse.quote(q)
        rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=ko&gl=KR&ceid=KR:ko"
        feed = feedparser.parse(rss_url)
        all_entries.extend(feed.entries)

    if not all_entries:
        print("최근 48시간 내에 수집된 뉴스가 없습니다.")
        return []

    high_priority = [] # 전문지 및 글로벌 전략 뉴스
    general_news = []  # 기타 업계 동향
    seen_links = set()

    # 필터 및 분류 기준
    special_media = ['오토헤럴드', '모터그래프', '오토데일리']
    core_companies = ['현대차', '기아', '도요타', 'TOYOTA', '테슬라', 'TESLA', 'BYD']
    strategy_keys = ['투자', 'SDV', '전략', '개발', '분석', '플랫폼', '실적', '특징주']

    for entry in all_entries:
        if entry.link in seen_links: continue
        seen_links.add(entry.link)
            
        news_item = f"▶ {entry.title}\n🔗 {entry.link}"
        title_upper = entry.title.upper()
        
        # 전문지 기사이거나, 5대 기업 관련 전략 키워드가 포함된 경우 '고퀄리티'로 분류
        is_special_media = any(m in entry.title for m in special_media)
        is_core_strategy = any(c in title_upper for c in core_companies) and \
                           any(k in entry.title for k in strategy_keys)
        
        if is_special_media or is_core_strategy:
            high_priority.append(news_item)
        else:
            general_news.append(news_item)

    # 텔레그램 글자 수 제한(4,000자)을 피하기 위해 메시지 분할
    chunks = []
    
    if high_priority:
        # 고퀄리티 리포트는 충분히(최대 15개) 담습니다.
        chunks.append("🎯 [글로벌 전략 및 전문지 고퀄리티] 🎯\n\n" + "\n\n".join(high_priority[:15]))
        
    if general_news:
        # 일반 동향은 8개로 요약하여 전달합니다.
        chunks.append("📰 [주요 업계 및 기술 동향] 📰\n\n" + "\n\n".join(general_news[:8]))
        
    return chunks

def send_telegram():
    token = str(os.environ.get('BOT_TOKEN', '')).strip()
    chat_id = str(os.environ.get('USER_ID', '')).strip()
    
    chunks = get_news()
    
    if not chunks:
        return

    for message in chunks:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        # 최종 안전장치: 4,000자 초과 시 절단
        payload = {"chat_id": chat_id, "text": message[:4000], "disable_web_page_preview": True}
        response = requests.post(url, data=payload)
        print(f"전송 결과: {response.status_code}")

if __name__ == "__main__":
    send_telegram()
