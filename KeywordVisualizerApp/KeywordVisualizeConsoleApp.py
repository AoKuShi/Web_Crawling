import lib.myTextMining as tm
import lib.NaverNewsCrawler as NNC
from konlpy.tag import Okt

while True:
  keyword = input("\n검색어 입력(종료하려면 '!'를 입력하세요) : ").strip()

  if keyword == "!":
    break

  resultAll = []
  
  start = 1
  display = 10
  resultJSON = NNC.searchNaverNews(keyword, start, display)

  while (resultJSON != None) and (resultJSON['display'] > 0):
      NNC.setNewsSearchResult(resultAll, resultJSON)
      start += resultJSON['display']
      resultJSON = NNC.searchNaverNews(keyword, start, display)
      if resultJSON != None:
          print(f"{keyword} [{start}] : Search Request Success")
      else:
          print(f"{keyword} [{start}] : Error ~~~~")

  filename = f"./data/{keyword}_naver_news.csv"
  NNC.saveSearchResult_CSV(resultAll, filename)

  input_filename = keyword + "_naver_news.csv"
  corpus_list = tm.load_corpus_from_csv("./data/" + input_filename, "description")
  print(corpus_list[:10])

  my_tokenizer = Okt().pos
  my_tags = ['Noun', 'Adjective', 'Verb'
  ]
  my_stopwords = my_stopwords = [
    '하며', '입', '하고', '로써', '하여', '애', '제', '한다', '그', '이', '할', '정', '수',
    '등', '를', '을', '에', '의', '가', '이', '은', '는', '와', '과', '에서', '에게',
    '한', '되', '한다', '하는', '됐다', '됐다', '중', '대한', '위한', '이런', '저런',
    '했다', '했다', '됐다', '된다', '하는', '것', '수', '있다', '없다', '됐다', '라고'
    ]

  counter = tm.analyze_word_freq(corpus_list, my_tokenizer, my_tags, my_stopwords)
  print(list(counter.items())[:20])
  tm.visualize_barchart(counter, "다음 영화 리뷰 키보드 분석", "빈도수수", "키워드")
  tm.visualize_wordcloud(counter)