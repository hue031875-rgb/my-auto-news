def get_news():
    # 쿼리를 아주 단순하게 나열합니다. 
    # 전문지 이름들을 앞쪽에 배치하고, 범위를 2d(48시간)로 유지합니다.
    query = '오토헤럴드 OR 모터그래프 OR 오토데일리 OR "현대차 투자" when:2d'
    
    encoded_query = urllib.parse.quote(query)
    rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=ko&gl=KR&ceid=KR:ko"
    
    feed = feedparser.parse(rss_url)
    
    # 만약 뉴스가 하나도 없다면, 검색 범위를 강제로 7일로 넓혀서 다시 검색합니다.
    if not feed.entries:
        print("48시간 내 뉴스가 없어 7일로 범위를 넓힙니다.")
        query = '오토헤럴드 OR 모터그래프 OR 오토데일리 OR "현대차 투자" when:7d'
        encoded_query = urllib.parse.quote(query)
        rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=ko&gl=KR&ceid=KR:ko"
        feed = feedparser.parse(rss_url)

    high_priority = []
    normal_news = []
    
    # ... (나머지 분류 로직은 동일)
