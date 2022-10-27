import MeCab
import re
import math
import mat_graf

negaposi = []  # ネガポジリスト
learn_data = [] # 教育データ
divide_line = 0 # 境界線
word_score_dict = {} # 単語とPN値の辞書
b = 0.2 #バイアス

# ひらがなの正規表現
re_hiragana = re.compile(r'[\u3041-\u3093]')

# シグモイド関数0~1の範囲で返す
def sigmoid(a):
    return 1 / (1 + math.exp(-a))

def learn():
    learn_word_file = open('learn_word.txt', 'r')
    for line in learn_word_file:
        line = line.rstrip()
        learn_data.append(line)

    learn_word_file.close()

    # 学習データを形態素解析させる
    for text in learn_data:
        m = MeCab.Tagger()
        s = m.parse(text)
        s = s.split('\n')

        sentences = []  # 形態素解析で得た単語のリスト
        for i in s[:-2]:
            i = re.split('[\t,]', i)
            sentences.append(i)

        # positive
        if sentences[1][0] == 'POSITIVE':

            for i in sentences:
                try:
                    if len(i[7]) != 1 and '副詞可能' not in i[3] and '人名' not in i and '固有名詞' not in i:

                        if ('特殊' not in i[5]) or ('一般' not in i[3]) or (len(i[0]) != 1):
                            if i[1] == '名詞' or i[1] == '副詞' or i[1] == '形容詞':
                                if i[7] not in word_score_dict:
                                    if i[7] != '*':
                                        word_score_dict.setdefault(i[7], 0.5)

                                else:
                                    word_score_dict[i[7]] += 0.2
                except:
                    pass

        # negative
        if sentences[1][0] == 'NEGATIVE':
            for i in sentences:
                try:
                    if len(i[7]) != 1 and '副詞可能' not in i[3] and '人名' not in i and '固有名詞' not in i:
                        if ('特殊' not in i[5]) or ('一般' not in i[3]) :
                            if i[1] == '名詞' or i[1] == '副詞' or i[1] == '形容詞':
                                if i[7] not in word_score_dict:
                                    if i[7] != '*':
                                        word_score_dict.setdefault(i[7], -0.4)
                                else:
                                    word_score_dict[i[7]] -= 0.2
                except:
                    pass

    for k, v in word_score_dict.items():
        word_score_dict[k] = sigmoid(v)

    # mat_graf.graf(word_score_dict)


def PN_judge(text):
    # 形態素解析を行う
    m = MeCab.Tagger()
    s = m.parse(text)
    s = s.split('\n')

    cnt = 0 # 出てきた単語の数
    total = 0 # 出てきた単語のPN値の総和
    classification = []  # 形態素解析のリスト
    for i in s:
        i = re.split('[\t,]', i)
        classification.append(i)

    for i in classification:
        try:
            total+= word_score_dict[i[7]]
            cnt += 1
        except:
            pass

    # PN_Tableに単語が含まれていなかった場合は0になる
    if total != 0:
        # PN値 = 出てきた単語のPN値の総和 ÷ 出てきた単語数
        pn_num = total / cnt
    else:
        pn_num = 0

    return pn_num
