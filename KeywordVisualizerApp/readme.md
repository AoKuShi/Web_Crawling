<개요>
 사용자가 입력한 검색어를 기반으로 네이버 뉴스 기사를 수집, 분석하여 핵심 키워드를 '막대 그레프'와 '데이터 클라우드'로 시각화하는 웹페이지

<기술>
  -프론트엔드: Streamlit (UI 구성 및 시각화)
  -백엔드 및 텍스트 처리(
    -konlpy.Okt (한국어 형태소 분석)
    -collections.Counter (빈도 분석)
    -matplotlib, seaborn (그래프 시각화)
    -wordcloud (워드클라우드 생성)
    )
  -데이터 수집: Naver OpenAPI (네이버 뉴스 검색)
  -파일 처리: CSV 업로드 및 저장
