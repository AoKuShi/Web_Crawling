import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import lib.myTextMining as tm
import lib.NaverNewsCrawler as nc
from collections import Counter
from matplotlib import rc, font_manager

# 한글 폰트 설정
font_path = "c:/Windows/Fonts/malgun.ttf"  # 맑은 고딕 경로
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)

# Streamlit 설정
st.set_page_config(layout="wide", page_title="Keyword Visualizer")

# 네비게이션 바 (좌측)
st.sidebar.title("🔍 뉴스 키워드 분석")
search_query = st.sidebar.text_input("검색어 입력", "")
save_csv = st.sidebar.checkbox("CSV 저장 여부")
uploaded_file = st.sidebar.file_uploader("CSV 파일 업로드", type=["csv"])

# 슬라이드 바: 단어 수 조절
num_words_freq = st.sidebar.slider("빈도수 그래프 단어 수", 5, 50, 20)
num_words_wc = st.sidebar.slider("워드클라우드 단어 수", 10, 100, 50)

# 데이터 로딩
df = None
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success("CSV 파일 업로드 완료")

elif st.sidebar.button("검색 실행") and search_query:
    result_all = []
    for start in range(1, 100, 100):  # 뉴스 100개 가져오기 (display=100)
        result_json = nc.searchNaverNews(search_query, start=start, display=100)
        if result_json is not None:
            nc.setNewsSearchResult(result_all, result_json)
    df = pd.DataFrame(result_all)
    
    if save_csv:
        filename = f"./data/{search_query}_naver_news.csv"
        nc.saveSearchResult_CSV(result_all, filename)
        st.sidebar.success("CSV 저장 완료")

# 키워드 분석 및 시각화
if df is not None and "title" in df.columns:
    st.subheader("키워드 시각화 결과")
    
    # 뉴스 제목 합치기
    corpus_list = df["title"].dropna().tolist()
    
    # 형태소 분석 및 단어 추출
    from konlpy.tag import Okt
    okt = Okt()
    stopwords = ["기자", "뉴스", "이", "그", "저", "것", "등", "더", "할", "수", "되", "의", "은", "는", "에", "을", "를", "로", "과", "와"]
    tags = ['Noun']  # 명사만

    token_list = tm.tokenize_korean_corpus(corpus_list, okt.pos, tags, stopwords)
    counter = Counter(token_list)

    # 빈도수 그래프
    top_words_freq = counter.most_common(num_words_freq)
    words_freq, counts_freq = zip(*top_words_freq)

    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(x=list(counts_freq), y=list(words_freq), ax=ax, palette="viridis")
    ax.set_title("키워드 빈도수")
    ax.set_xlabel("빈도수")
    ax.set_ylabel("단어")
    st.pyplot(fig)

    # 워드클라우드
    top_words_wc = dict(counter.most_common(num_words_wc))
    wordcloud = WordCloud(
        font_path="c:/Windows/fonts/malgun.ttf",
        width=800,
        height=400,
        background_color="white"
    ).generate_from_frequencies(top_words_wc)

    fig_wc, ax_wc = plt.subplots(figsize=(8, 4))
    ax_wc.imshow(wordcloud, interpolation="bilinear")
    ax_wc.axis("off")
    st.pyplot(fig_wc)

else:
    st.warning("검색어 입력 후 검색 실행 또는 CSV 파일을 업로드하세요.")
