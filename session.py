import line
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
import scipy as sp
import Global_Variables
import jieba
clf=joblib.load('emotion_model.model')
count_vec = TfidfVectorizer(binary=False, decode_error='ignore')
x_train = sp.load('train_data.npy')

class Charactor():
    def __init__(self,name=""):
        self.name=name
        self.charactor_worlds=[]
        self.charactor_world_amount=0
        self.charactor_positive_emotion=[]
        self.charactor_nagetive_emotion=[]
        self.charactor_emotion=[]
        self.appearance=False
class Session():
    def __init__(self,session_content,mode=0):
        self.mode=mode
        self.session_number = 0
        self.session_time = ''
        self.session_place = ''
        self.session_location = ''
        self. line_list = []
        self.session_content = ''
        self.session_positive_words = []
        self.session_negative_words = []
        self.session_emotion_words = []
        self.session_positive_words_set = []
        self.session_negative_words_set = []
        self. session_emotion_words_set = []
        self.session_emotion_value = ''
        self.session_content=session_content
        self.session_words_amount=0
        self.session_charactor_dic={}
        for i in Global_Variables.name_list:
            self.session_charactor_dic[i]=Charactor(i)
        self.read_session_lines()

    def read_session_lines(self):
        count = 0
        for i in self.session_content.split('\n'):
            if len(str(i).strip('\n').strip(' '))==0:
                continue
            if count!=0:
                session_line=line.Line(i,self.mode)
                self.line_list.append(session_line)
                self.session_positive_words.extend(session_line.positive)
                self.session_negative_words.extend(session_line.nagetive)
                self.session_emotion_words.extend(session_line.positive)
                self.session_emotion_words.extend(session_line.nagetive)
            else:
                session_info=i.split(' ')
                if self.mode==0:
                    self.session_number=int(session_info[0].strip('.').strip(' ').strip('\ufeff'))
                    self.session_time=session_info[1].strip(' ')
                    self.session_place=session_info[2].strip(' ')
                    self.session_location=session_info[3].strip(' ').strip('\n')
                else:
                    self.session_number=int(session_info[0].strip('.').strip(' ').strip('\ufeff'))
                    self.session_location=session_info[1].strip(' ')
                    self.session_time=session_info[2].strip(' ')
                    self.session_place=session_info[3].strip(' ').strip('\n')
                count+=1
        self.session_positive_words_set=set(self.session_positive_words)
        self.session_negative_words_set=set(self.session_negative_words)
        self.session_emotion_words_set=set(self.session_emotion_words)
        self.cal_words_amount()

    def cal_words_amount(self,charactor=''):
        if len(charactor)==0:
            for line in self.line_list:
                if line.type=='talk':
                    if line.who_said in Global_Variables.name_list:
                        said_word=line.content
                        self.session_charactor_dic[line.who_said].appearance=True
                        self.session_charactor_dic[line.who_said].charactor_worlds.append(said_word)
                        cut_said_word=jieba.cut(said_word)
                        for word in cut_said_word:
                            if word in Global_Variables.positive_words:
                                self.session_charactor_dic[line.who_said].charactor_positive_emotion.append(word)
                                self.session_charactor_dic[line.who_said].charactor_emotion.append(word)
                            if word in Global_Variables.negative_words:
                                self.session_charactor_dic[line.who_said].charactor_nagetive_emotion.append(word)
                                self.session_charactor_dic[line.who_said].charactor_emotion.append(word)
                        for i in Global_Variables.punctuation_mark:
                            said_word=said_word.replace(i,'')
                        self.session_charactor_dic[line.who_said].charactor_world_amount+=len(said_word)
            for v in self.session_charactor_dic.values():
                self.session_words_amount+=v.charactor_world_amount


    def show_info(self,show_line_detail=0):
        print('场次编号:'+str(self.session_number))
        print('场次时间:'+str(self.session_time))
        print('室内室外:'+str(self.session_place))
        print('场景地点:'+str(self.session_location))
        print('场景积极词:'+str(self.session_positive_words_set))
        print('场景消极词:'+str(self.session_negative_words_set))
        print('场景全部情感词:'+str(self.session_emotion_words_set))
        print('场景台词数:'+str(self.session_words_amount))
        # print('场景情感值:'+str(self.session_emotion_value))
        if show_line_detail==1:
            for line in self.line_list:
                line.showInfo()

    def compare_emotion(self,x_test):
        count_vec.fit_transform(x_train)
        x_test = count_vec.transform(x_test)
        # print(doc_class_predicted)
        self.session_emotion_value=clf.predict_proba(x_test)[0]


if __name__=="__main__":
    a=open('test.txt',encoding='utf-8').read()
    a=Session(a)
    a.show_info()