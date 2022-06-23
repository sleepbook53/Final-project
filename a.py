from youtube_transcript_api import YouTubeTranscriptApi
from konlpy.tag import Kkma
from pykospacing import Spacing

def ytb_subtitle(results2):
    for i in results2 :
      link = i['link']
      
      try:
          code = link.split('=')[1]
          srt = YouTubeTranscriptApi.get_transcript(f"{code}", languages=['ko']) #한글로, 딕셔너리 구조

          text = ''

          for i in range(len(srt)):
              text += srt[i]['text'] + ''

          text_ = text.replace(' ','')

          #문장 분리 / kss 사용해도 무방
          kkma = Kkma()

          text_sentences = kkma.sentences(text_)

          #종결 단어
          lst = ['죠','다','요','시오', '습니까','십니까','됩니까','옵니까','뭡니까',]

          # df = pd.read_csv('not_verb.csv',encoding='utf-8')
          # not_verb = df.stop.to_list()

          #단어 단위로 끊기
          text_all = ' '.join(text_sentences).split(' ')

          for n in range(len(text_all)) :
              i = text_all[n]
              if len(i) == 1 : #한글자일 경우 추가로 작업x
                  continue

              else :
                  for j in lst : #종결 단어
                      #질문형
                      if j in lst[4:]:
                          i += '?'

                      #명령형                
                      elif j == '시오':
                          i += '!'

                      #마침표    
                      else :
                          # if i in not_verb : #특정 단어 제외
                          #     continue
                          # else :
                        if j == i[len(i)-1] : #종결
                            text_all[n] += '.'


          spacing = Spacing()
          text_all_in_one = ' '.join(text_all)

          text_split = spacing(text_all_in_one.replace(' ','')).split('.')
          text2one= []
          for t in text_split:
              text2one.append(t.lstrip())
          global w
          w = ['. '.join(text2one)]
         # print('O')
        
      except:
          print('X')

      for j in results2 :
        j['subtitle'] = w  
      global count
      count -= 1  
      print('남은 수 : ', count)
      print(j['subtitle'])

