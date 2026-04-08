import feedparser
import requests
import os
import urllib.parse

def get_news():
    # 1. 쿼리 최적화: 중고차(-중고차)와 단순 시승기(-시승기)를 검색 단계에서 배제합니다.
    queries = [
        # 전문지 그룹
        '오토헤럴드 OR 모터그래프 OR 오토데일리 -중고차 -시승기 when:2d',
        
        # 글로벌 5대장 핵심 전략 (국내외 주요 뉴스)
        '(현대차 OR 기아 OR 도요타 OR 테슬라 OR BYD) ("투자" OR "SDV" OR "전략" OR "개발" OR "플랫폼") -중고차 -렌트 when:2d',
        
        # [해외 소스 추가] 로이터, 블룸버그 등 외신 인용 기사 타겟팅
        '자동차 "로이터" OR "블룸버그" OR "외신" ("전략" OR "시장") when:2d'
    ]
    
    all_entries = []
    for q in queries:
        encoded_query = urllib.parse.quote(q)
        rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=ko&gl=KR&ceid=KR:ko"
        feed = feedparser.parse(rss_url)
        all_entries.extend(feed.entries)

    if not all_entries: return []

    high_priority = [] 
    general_news = []  
    seen_links = set()

    # 2. 강력한 제외 키워드 (노이즈 제거)
    filter_words = ['중고차', '렌트', '리스', '할부', '시승기', '이벤트', '판매합니다', '경매', '블랙박스']
    
    # 3. 우선순위 키워드
    strategy_keys = ['투자', 'SDV', '전략', '개발', '공시', '실적', '협력', 'M&A']

    for entry in all_entries:
        if entry.link in seen_links: continue
        
        # 제목에 제외 키워드가 하나라도 있으면 아예 무시합니다.
        if any(word in entry.title for word in filter_words):
            continue
            
        seen_links.add(entry.link)
        news_item = f"▶ {entry.title}\n🔗 {entry.link}"
        
        # 전문지 기사거나 핵심 전략 키워드가 포함된 경우만 '상단' 배치
        is_special = any(m in entry.title for m in ['오토헤럴드', '모터그래프', '오토데일리'])
        is_strategy = any(k in entry.title for k in strategy_keys)
        
        if is_special or is_strategy:
            high_priority.append(news_item)
        else:
            general_news.append(news_item)

    # 메시지 분할 전송
    chunks = []
    if high_priority:
        # 양보다 질! 핵심 뉴스는 상위 10개로 압축합니다.
        chunks.append("🔥 [글로벌 전략 & 고퀄리티 리포트] 🔥\n\n" + "\n\n".join(high_priority[:10]))
        
    if general_news:
        # 일반 뉴스는 참고용으로 5개만 섞습니다.
        chunks.append("📰 [업계 주요 동향] 📰\n\n" + "\n\n".join(general_news[:5]))
        
    return chunks

def send_telegram():
    token = str(os.environ.get('BOT_TOKEN', '')).strip()
    chat_id = str(os.environ.get('USER_ID', '')).strip()
    chunks = get_news()
    if not chunks: return

    for message in chunks:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {"chat_id": chat_id, "text": message[:4000], "disable_web_page_preview": True}
        requests.post(url, data=payload)

if __name__ == "__main__":
    send_telegram()
