from PyQt5.QtWidgets import \
    QWidget, QApplication, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout, \
    QLabel,QTableWidget,QTableWidgetItem,QDialog, QHeaderView
from PyQt5.QtGui import *
import sys
import get_tweet # 検索したツイートをリストで返す
import Learn # ツイートのネガポジ度を判断
# import mat_graf # グラフ生成

text_and_score = {} # key:ツイート value: ネガポジ度
positive_tweet = []
negative_tweet = []
negapoji_list = []

class Window(QWidget):

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        key_serch = QPushButton('search')
        keyword = QLineEdit(self)

        positive_button = QPushButton('positive')
        positive_num = QLabel('')
        negative_button = QPushButton('negative')
        negative_num = QLabel('')

        '''
        横揃え表示
        キーワード入力 検索
        '''
        hbox = QHBoxLayout()
        hbox.addWidget(keyword)
        hbox.addWidget(key_serch)

        '''
        横揃え表示
        positive n%     negative n%
        '''
        hbox1 = QHBoxLayout()
        hbox1.addWidget(positive_button)
        hbox1.addWidget(positive_num)
        hbox1.addWidget(negative_button)
        hbox1.addWidget(negative_num)

        '''
        キーワード検索と
        positive,negativeを縦揃えにする
        '''
        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addLayout(hbox1)

        # ボタンイベント
        key_serch.clicked.connect(lambda: self.search_button_event(keyword, positive_num, negative_num))
        positive_button.clicked.connect(self.positive_button_event)
        negative_button.clicked.connect(self.negative_button_event)

        self.setLayout(vbox)
        self.setGeometry(500, 320, 350, 140)
        self.setWindowTitle('ツイート検索')


    # 検索ボタンイベント
    def search_button_event(self, s, ps, ns):

        print(s.text())

        # 検索で得たツイートをリストで取得
        tweet_list = get_tweet.search(s.text())
        s.clear()
        print(len(tweet_list))

        # 教育させる
        Learn.learn()


        # ここでJudgeを呼び出して分かち書きさせる
        for tweet in tweet_list:
            text_and_score.setdefault(tweet,Learn.PN_judge(tweet))

        # divide_line (分離する境界線)
        #for k,v in text_and_score.items():
        for k,v in sorted(text_and_score.items(), key=lambda x:x[1], reverse=True):
            if v >= 0.5:
                positive_tweet.append([k, v])

        for k, v in sorted(text_and_score.items(), key=lambda x: x[1]):
             if 0 < v and v < 0.5:
                negative_tweet.append([k, v])

        ps.setText(str(len(positive_tweet)))
        ns.setText(str(len(negative_tweet)))

    # ポジティブボタンイベント
    def positive_button_event(self):
        pos_win = Positeve_Window(self)
        pos_win.show()

    # ネガティブボタンイベント
    def negative_button_event(self):
        neg_win = Negative_Window(self)
        neg_win.show()


# ポジティブツイート
class Positeve_Window(QWidget):
    def __init__(self,parent=None):
        self.w = QDialog(parent)
        self.parent = parent

        data = positive_tweet

        super(Positeve_Window, self).__init__(parent)
        colcnt = len(data[0])
        rowcnt = len(data)
        self.tablewidget = QTableWidget(rowcnt, colcnt)

        #ヘッダー設定

        horHeaders = ['Tweet','PN値']
        self.tablewidget.setHorizontalHeaderLabels(horHeaders)
        self.tablewidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

        self.tablewidget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch, 0)

        #テーブルの中身作成
        for n in range(rowcnt):
            for m in range(colcnt):
                item = QTableWidgetItem(str(data[n][m]))
                self.tablewidget.setItem(n, m, item)

        #レイアウト
        layout = QHBoxLayout()
        layout.addWidget(self.tablewidget)
        self.w.setLayout(layout)

    def show(self):
        self.w.exec_()


# ネガティブツイート
class Negative_Window(QWidget):
    def __init__(self,parent=None):
        self.w = QDialog(parent)
        self.parent = parent

        data = negative_tweet

        super(Negative_Window, self).__init__(parent)
        colcnt = len(data[0])
        rowcnt = len(data)
        self.tablewidget = QTableWidget(rowcnt, colcnt)

        #ヘッダー設定

        horHeaders = ['Tweet', 'PN値']
        self.tablewidget.setHorizontalHeaderLabels(horHeaders)
        self.tablewidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

        self.tablewidget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch, 0)

        #テーブルの中身作成
        for n in range(rowcnt):
            for m in range(colcnt):
                item = QTableWidgetItem(str(data[n][m]))
                self.tablewidget.setItem(n, m, item)

        #レイアウト
        layout = QHBoxLayout()
        layout.addWidget(self.tablewidget)
        self.w.setLayout(layout)


    def show(self):
        self.w.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()


    win.show()
    sys.exit(app.exec_())