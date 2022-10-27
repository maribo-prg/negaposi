# ネガポジ度を返す
import MeCab
import re


negaposi = []  # ネガポジリスト
learn_data = [] # 教育データ
divide_line = 0 # 境界線
word_score_dict = {} # 単語とPN値の辞書
b = 0.2 #バイアス


# 極性単語辞書の読み込み
get_word_score = open('word_score.txt', 'r')
for line in get_word_score:
    line = line.rstrip()
    tmp = line.split(':')
    tmp[3] = float(tmp[3])
    word_score_dict.setdefault(tmp[0], tmp[3])

get_word_score.close()


def Judge(texts):
    nega_cnt = 0
    pos_cnt = 0

    for text in texts:
        score = 0 # ポジねが度

        # 形態素解析を行う
        m = MeCab.Tagger()
        s = m.parse(text)
        s = s.split('\n')

        sentences = [] # 形態素解析で得た単語のリスト
        for i in s:
            i = re.split('[\t,]', i)
            sentences.append(i)

        cnt = 0
        for i in sentences:
            try:
                score += word_score_dict[i[7]]
                cnt += 1

            except:
                pass

        if score != 0:
            pn_num = score / cnt
        else:
            pn_num = 0
        if pn_num > divide_line :
            pos_cnt += 1
        elif pn_num < divide_line:
            nega_cnt += 1

        negaposi.append(pn_num)

    return negaposi
