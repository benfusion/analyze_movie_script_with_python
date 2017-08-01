#coding=utf-8
import session
import os
from imp import reload
import Global_Variables
from docx import Document

"""
----------handle_scipt.py-------------
             记录整个剧本信息
"""
if not os.path.exists('out'):
    os.mkdir('out')

class Script:
    '''
    记录整个剧本的信息，包含多个场景的类的实例
    '''
    def __init__(self,filename,mode=1):
        self.mode=mode
        self.script_name=''
        self.session_list=[]
        self.charactor_overrall_word_count_dic={}
        self.charactor_overral_apear_in_session={}
        for i in Global_Variables.name_list:
            self.charactor_overrall_word_count_dic[i]=0
        self.all_charactor_count={}
        self.read_script_file(filename)
        self.cal_overrall_count()
        self.cal_all_character()
        self.cal_character_apear_count()

    def read_script_file(self,filename):
        name=os.path.splitext(filename)[0]
        self.script_name=name.split('\\')[len(name.split('\\'))-1]
        script=""
        # script=open(filename,encoding='utf-8').read()
        document = Document(filename)
        for para in document.paragraphs:
            script+=para.text+'\n'
        # print(script)
        split_script=script.split('\n\n') #以双回车判断是否为一个场
        for s in split_script:
            ss=session.Session(s,self.mode)
            self.session_list.append(ss)

    def cal_overrall_count(self):
        """
        统计每个角色的台词数
        """
        for session in self.session_list:
            for keys,session_charactor_info in session.session_charactor_dic.items():
                self.charactor_overrall_word_count_dic[keys]+=session_charactor_info.charactor_world_amount

    def cal_all_character(self):
        """
        计算角色（包含非主要角色）出场次数
        """
        for session in self.session_list:
            for name in session.session_all_charactor_set:
                self.all_charactor_count.setdefault(name,0)
                self.all_charactor_count[name]+=1

        '''输出所有角色出现次数的排序（未分词）到屏幕，可以发现主要人物'''
        # print(sorted(self.all_charactor_count.items(),key=lambda x:x[1],reverse=True))
    def cal_character_apear_count(self):
        """
        计算主要角色的出场次数
        """
        for session in self.session_list:
            for name,apear in session.session_charactor_dic.items():
                self.charactor_overral_apear_in_session.setdefault(name,0)
                if apear.appearance:
                    self.charactor_overral_apear_in_session[name]+=1
        # print(self.charactor_overral_apear_in_session)

    def write_character_total_words(self):
        f=open('out\\'+self.script_name+'_total_words.txt','w')
        for k,v in self.charactor_overrall_word_count_dic.items():
            str2=k+' '+str(v)+'\n'
            f.write(str2)
        f.close()

    def write_charactor_overral_apear(self):
        f=open('out\\'+self.script_name+'_total_apear.txt','w')
        for k,v in self.charactor_overral_apear_in_session.items():
            str2=k+' '+str(v)+'\n'
            f.write(str2)
        f.close()
    def write_session_emotion(self):
        f=open('out\\'+self.script_name+'_session_emotion.txt','w')
        for session in self.session_list:
            str2=str(session.session_number)+' '+str(session.session_positive_value)+' '+str(session.session_negative_value)+' '+str(session.session_emotion_value)+'\n'
            f.write(str2)
        f.close()
        for name in Global_Variables.name_list:
            f=open('out\\'+self.script_name+'_'+name+'_in_session_emotion.txt','w')
            for session in self.session_list:
                str2=str(session.session_number)+' '+str(session.session_charactor_dic[name].charactor_value)+'\n'
                f.write(str2)
            f.close()

    def write_session_words(self):
        f=open('out\\'+self.script_name+'_session_wrods.txt','w')
        for session in self.session_list:
            str2=str(session.session_number)+' '+str(session.session_words_amount)+'\n'
            f.write(str2)
        f.close()

    def showinfo(self,show_session_detail=0,show_line_detail=0):
        for k,v in self.charactor_overrall_word_count_dic.items():
            print(k+str(v))
        if show_session_detail==1:
            for i in self.session_list:
                i.show_info(show_line_detail=show_line_detail)
if __name__=="__main__":
    script=Script('白鹿原_改.docx',mode=1)
    # print(script.script_name)
    script.showinfo(show_session_detail=1)
    script.write_character_total_words()
    script.write_charactor_overral_apear()
    script.write_session_emotion()
    script.write_session_words()