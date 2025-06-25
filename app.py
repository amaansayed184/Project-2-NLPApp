from http.client import responses
from tkinter import *
from tkinter import messagebox
from mydb import Database
from api_handling import API

class NLPApp:
    def __init__(self):
        self.db=Database()
        self.api=API()
        self.root=Tk()
        self.root.title("NLPApp ")
        self.root.iconbitmap('resources/favicon.ico')
        self.root.geometry('500x500')

        # Style configuration
        self.style_config = {
            "bg_color": "#ADD8E6",
            "fg_color": "white",
            "btn_bg_color": "#007BFF",
            "btn_fg_color": "white",
            "font_heading": ('Helvetica', 24, 'bold'),
            "font_subheading": ('Helvetica', 20),
            "font_regular": ('Helvetica', 12),
            "btn_pady": 5
        }

        self.root.configure(bg=self.style_config["bg_color"])

        self.login_gui()


        self.root.mainloop()

    def login_gui(self):
        self.clear()
        head=Label(self.root,text='NLPApp',bg=self.style_config["bg_color"],fg=self.style_config["fg_color"])
        head.configure(font=self.style_config["font_heading"])
        head.pack(pady=(30,30))

        head2 = Label(self.root, text='Login Page', bg=self.style_config["bg_color"], fg=self.style_config["fg_color"])
        head2.configure(font=self.style_config["font_subheading"])
        head2.pack(pady=(10, 20))

        label1=Label(self.root,text='enter email',bg=self.style_config["bg_color"],fg=self.style_config["fg_color"])
        label1.configure(font=self.style_config["font_regular"])
        label1.pack(pady=(10,10))

        self.email_input= Entry(self.root,width=50)
        self.email_input.pack(pady=(5,10),ipady=4)

        label2 = Label(self.root, text='enter password',bg=self.style_config["bg_color"],fg=self.style_config["fg_color"])
        label2.configure(font=self.style_config["font_regular"])
        label2.pack(pady=(10, 10))

        self.password_input = Entry(self.root, width=50,show='*')
        self.password_input.pack(pady=(5, 10), ipady=4)

        login_btn=Button(self.root,text='Login',width=10,height=2,command=self.login_perform, bg=self.style_config["btn_bg_color"], fg=self.style_config["btn_fg_color"], pady=self.style_config["btn_pady"])
        login_btn.configure(font=self.style_config["font_regular"])
        login_btn.pack(pady=(10,10))

        label3 = Label(self.root, text='not a member?',bg=self.style_config["bg_color"],fg=self.style_config["fg_color"])
        label3.configure(font=self.style_config["font_regular"])
        label3.pack(pady=(20, 10))

        redirect_btn = Button(self.root, text='register now', width=10, height=2,command=self.register_gui, bg=self.style_config["btn_bg_color"], fg=self.style_config["btn_fg_color"], pady=self.style_config["btn_pady"])
        redirect_btn.configure(font=self.style_config["font_regular"])
        redirect_btn.pack(pady=(10, 10))

    def register_gui(self):
        self.clear()

        head = Label(self.root, text='NLPApp', bg=self.style_config["bg_color"], fg=self.style_config["fg_color"])
        head.configure(font=self.style_config["font_heading"])
        head.pack(pady=(30, 30))

        head2 = Label(self.root, text='Registration Page', bg=self.style_config["bg_color"], fg=self.style_config["fg_color"])
        head2.configure(font=self.style_config["font_subheading"])
        head2.pack(pady=(10, 20))

        label0 = Label(self.root, text='enter name', bg=self.style_config["bg_color"],fg=self.style_config["fg_color"])
        label0.configure(font=self.style_config["font_regular"])
        label0.pack(pady=(10, 10))

        self.name_input = Entry(self.root, width=50)
        self.name_input.pack(pady=(5, 10), ipady=4)


        label1 = Label(self.root, text='enter email', bg=self.style_config["bg_color"],fg=self.style_config["fg_color"])
        label1.configure(font=self.style_config["font_regular"])
        label1.pack(pady=(10, 10))

        self.email_input = Entry(self.root, width=50)
        self.email_input.pack(pady=(5, 10), ipady=4)

        label2 = Label(self.root, text='enter password', bg=self.style_config["bg_color"],fg=self.style_config["fg_color"])
        label2.configure(font=self.style_config["font_regular"])
        label2.pack(pady=(10, 10))

        self.password_input = Entry(self.root, width=50, show='*')
        self.password_input.pack(pady=(5, 10), ipady=4)

        register_btn = Button(self.root, text='register', width=10, height=2,command=self.register_perform, bg=self.style_config["btn_bg_color"], fg=self.style_config["btn_fg_color"], pady=self.style_config["btn_pady"])
        register_btn.configure(font=self.style_config["font_regular"])
        register_btn.pack(pady=(10, 10))

        label3 = Label(self.root, text='already register?', bg=self.style_config["bg_color"],fg=self.style_config["fg_color"])
        label3.configure(font=self.style_config["font_regular"])
        label3.pack(pady=(20, 10))

        redirect_btn = Button(self.root, text='login', width=10, height=2, command=self.login_gui, bg=self.style_config["btn_bg_color"], fg=self.style_config["btn_fg_color"], pady=self.style_config["btn_pady"])
        redirect_btn.configure(font=self.style_config["font_regular"])
        redirect_btn.pack(pady=(10, 10))


    def clear(self):
        # clearing existing gui
        for i in self.root.pack_slaves():
            i.destroy()

    def register_perform(self):
        name=self.name_input.get()
        email = self.email_input.get()
        password = self.password_input.get()

        response=self.db.add_data(name, email, password)

        if response:
            messagebox.showinfo('Success','Registration successful..You may Login now')
        else:
            messagebox.showerror('Error','Email Already exist')


    def login_perform(self):
        email = self.email_input.get()
        password = self.password_input.get()

        response=self.db.search(email, password)
        if response:
            messagebox.showinfo('success','login successfully')
            self.home_gui()

        else:
            messagebox.showerror('Error','Incorrect email/password')

    def home_gui(self):
        self.clear()
        head = Label(self.root, text='NLPApp', bg=self.style_config["bg_color"], fg=self.style_config["fg_color"])
        head.configure(font=self.style_config["font_heading"])
        head.pack(pady=(30, 30))

        sentiment_analysis_btn = Button(self.root, text='Sentiment Analysis', width=30, height=2, command=self.sentiment_gui, bg=self.style_config["btn_bg_color"], fg=self.style_config["btn_fg_color"], pady=self.style_config["btn_pady"])
        sentiment_analysis_btn.configure(font=self.style_config["font_regular"])
        sentiment_analysis_btn.pack(pady=(10, 10))

        NER_analysis_btn = Button(self.root, text='Name Entity Recognition', width=30, height=2, command=self.ner_gui, bg=self.style_config["btn_bg_color"], fg=self.style_config["btn_fg_color"], pady=self.style_config["btn_pady"])
        NER_analysis_btn.configure(font=self.style_config["font_regular"])
        NER_analysis_btn.pack(pady=(10, 10))

        summerization_btn = Button(self.root, text='Summarization', width=30, height=2, command=self.summarization_gui, bg=self.style_config["btn_bg_color"], fg=self.style_config["btn_fg_color"], pady=self.style_config["btn_pady"])
        summerization_btn.configure(font=self.style_config["font_regular"])
        summerization_btn.pack(pady=(10, 10))

        grammer_spelling_btn = Button(self.root, text='Grammer Spelling Correction', width=30, height=2, command=self.grammer_spelling_gui, bg=self.style_config["btn_bg_color"], fg=self.style_config["btn_fg_color"], pady=self.style_config["btn_pady"])
        grammer_spelling_btn.configure(font=self.style_config["font_regular"])
        grammer_spelling_btn.pack(pady=(10, 10))

        language_detection_btn = Button(self.root, text='Language Detection', width=30, height=2, command=self.lang_detect_gui, bg=self.style_config["btn_bg_color"], fg=self.style_config["btn_fg_color"], pady=self.style_config["btn_pady"])
        language_detection_btn.configure(font=self.style_config["font_regular"])
        language_detection_btn.pack(pady=(10, 10))

        headline_generation_btn = Button(self.root, text='Headline Generation', width=30, height=2, command=self.headline_generation_gui, bg=self.style_config["btn_bg_color"], fg=self.style_config["btn_fg_color"], pady=self.style_config["btn_pady"])
        headline_generation_btn.configure(font=self.style_config["font_regular"])
        headline_generation_btn.pack(pady=(10, 10))

        logout_btn = Button(self.root, text='logout', width=10, height=2, command=self.login_gui, bg=self.style_config["btn_bg_color"], fg=self.style_config["btn_fg_color"], pady=self.style_config["btn_pady"])
        logout_btn.configure(font=self.style_config["font_regular"])
        logout_btn.pack(pady=(10, 10))

    def sentiment_gui(self):
        self.clear()
        head = Label(self.root, text='NLPApp', bg=self.style_config["bg_color"], fg=self.style_config["fg_color"])
        head.configure(font=self.style_config["font_heading"])
        head.pack(pady=(30, 30))

        head2 = Label(self.root, text='Sentiment Analysis', bg=self.style_config["bg_color"], fg=self.style_config["fg_color"])
        head2.configure(font=self.style_config["font_subheading"])
        head2.pack(pady=(10, 20))

        self.para = Label(self.root, text='enter paragraph', bg=self.style_config["bg_color"],fg=self.style_config["fg_color"])
        self.para.configure(font=self.style_config["font_regular"])
        self.para.pack(pady=(10, 10))

        self.para_input = Entry(self.root, width=70)
        self.para_input.pack(pady=(5, 10), ipady=4)

        analysis_btn = Button(self.root, text='Analyze Sentiment', width=30, height=2,command=self.do_sentiment_analysis, bg=self.style_config["btn_bg_color"], fg=self.style_config["btn_fg_color"], pady=self.style_config["btn_pady"])
        analysis_btn.configure(font=self.style_config["font_regular"])
        analysis_btn.pack(pady=(10, 10))

        self.sentiment_result = Label(self.root, text='', bg=self.style_config["bg_color"],fg=self.style_config["fg_color"])
        self.sentiment_result.pack(pady=(10, 10))
        self.sentiment_result.configure(font=self.style_config["font_regular"])

        back_btn = Button(self.root, text='GO BACK', width=10, height=2, command=self.home_gui, bg=self.style_config["btn_bg_color"], fg=self.style_config["btn_fg_color"], pady=self.style_config["btn_pady"])
        back_btn.configure(font=self.style_config["font_regular"])
        back_btn.pack(pady=(10, 10))


    def summarization_gui(self):
        self.clear()
        head = Label(self.root, text='NLPApp', bg=self.style_config["bg_color"], fg=self.style_config["fg_color"])
        head.configure(font=self.style_config["font_heading"])
        head.pack(pady=(30, 30))

        head2 = Label(self.root, text='Summarization', bg=self.style_config["bg_color"], fg=self.style_config["fg_color"])
        head2.configure(font=self.style_config["font_subheading"])
        head2.pack(pady=(10, 20))

        self.para2 = Label(self.root, text='enter paragraph', bg=self.style_config["bg_color"],fg=self.style_config["fg_color"])
        self.para2.configure(font=self.style_config["font_regular"])
        self.para2.pack(pady=(10, 10))

        self.para2_input = Entry(self.root, width=70)
        self.para2_input.pack(pady=(5, 10), ipady=4)

        summarize_btn = Button(self.root, text='Summarize It', width=30, height=2,command=self.do_summarize, bg=self.style_config["btn_bg_color"], fg=self.style_config["btn_fg_color"], pady=self.style_config["btn_pady"])
        summarize_btn.configure(font=self.style_config["font_regular"])
        summarize_btn.pack(pady=(10, 10))

        self.summarize_result = Label(self.root, text='', bg=self.style_config["bg_color"],fg=self.style_config["fg_color"])
        self.summarize_result.pack(pady=(10, 10))
        self.summarize_result.configure(font=self.style_config["font_regular"])

        back_btn = Button(self.root, text='GO BACK', width=10, height=2, command=self.home_gui, bg=self.style_config["btn_bg_color"], fg=self.style_config["btn_fg_color"], pady=self.style_config["btn_pady"])
        back_btn.configure(font=self.style_config["font_regular"])
        back_btn.pack(pady=(10, 10))

    def ner_gui(self):
        self.clear()
        head = Label(self.root, text='NLPApp', bg=self.style_config["bg_color"], fg=self.style_config["fg_color"])
        head.configure(font=self.style_config["font_heading"])
        head.pack(pady=(30, 30))

        head2 = Label(self.root, text='Name Entity Recognition', bg=self.style_config["bg_color"], fg=self.style_config["fg_color"])
        head2.configure(font=self.style_config["font_subheading"])
        head2.pack(pady=(10, 20))

        self.para3 = Label(self.root, text='enter paragraph', bg=self.style_config["bg_color"],fg=self.style_config["fg_color"])
        self.para3.configure(font=self.style_config["font_regular"])
        self.para3.pack(pady=(10, 10))


        self.para3_input = Entry(self.root, width=70)
        self.para3_input.pack(pady=(5, 10), ipady=4)

        self.word = Label(self.root, text='enter word', bg=self.style_config["bg_color"],fg=self.style_config["fg_color"])
        self.word.configure(font=self.style_config["font_regular"])
        self.word.pack(pady=(10, 10))

        self.word_input = Entry(self.root, width=70)
        self.word_input.pack(pady=(5, 10), ipady=4)

        ner_btn = Button(self.root, text='Search', width=30, height=2,command=self.do_ner, bg=self.style_config["btn_bg_color"], fg=self.style_config["btn_fg_color"], pady=self.style_config["btn_pady"])
        ner_btn.configure(font=self.style_config["font_regular"])
        ner_btn.pack(pady=(10, 10))

        self.ner_result = Label(self.root, text='', bg=self.style_config["bg_color"],fg=self.style_config["fg_color"])
        self.ner_result.pack(pady=(10, 10))
        self.ner_result.configure(font=self.style_config["font_regular"])

        back_btn = Button(self.root, text='GO BACK', width=10, height=2, command=self.home_gui, bg=self.style_config["btn_bg_color"], fg=self.style_config["btn_fg_color"], pady=self.style_config["btn_pady"])
        back_btn.configure(font=self.style_config["font_regular"])
        back_btn.pack(pady=(10, 10))

    def lang_detect_gui(self):
        self.clear()
        head = Label(self.root, text='NLPApp', bg=self.style_config["bg_color"], fg=self.style_config["fg_color"])
        head.configure(font=self.style_config["font_heading"])
        head.pack(pady=(30, 30))

        head3 = Label(self.root, text='Language Detection', bg=self.style_config["bg_color"], fg=self.style_config["fg_color"])
        head3.configure(font=self.style_config["font_subheading"])
        head3.pack(pady=(10, 20))

        self.para4 = Label(self.root, text='enter paragraph', bg=self.style_config["bg_color"],fg=self.style_config["fg_color"])
        self.para4.configure(font=self.style_config["font_regular"])
        self.para4.pack(pady=(10, 10))

        self.para4_input = Entry(self.root, width=70)
        self.para4_input.pack(pady=(5, 10), ipady=4)

        lang_detect_btn = Button(self.root, text='Detect Language', width=30, height=2,command=self.do_lang_detect, bg=self.style_config["btn_bg_color"], fg=self.style_config["btn_fg_color"], pady=self.style_config["btn_pady"])
        lang_detect_btn.configure(font=self.style_config["font_regular"])
        lang_detect_btn.pack(pady=(10, 10))

        self.lang_detect_result = Label(self.root, text='', bg=self.style_config["bg_color"],fg=self.style_config["fg_color"])
        self.lang_detect_result.pack(pady=(10, 10))
        self.lang_detect_result.configure(font=self.style_config["font_regular"])

        back_btn = Button(self.root, text='GO BACK', width=10, height=2, command=self.home_gui, bg=self.style_config["btn_bg_color"], fg=self.style_config["btn_fg_color"], pady=self.style_config["btn_pady"])
        back_btn.configure(font=self.style_config["font_regular"])
        back_btn.pack(pady=(10, 10))

    def grammer_spelling_gui(self):
        self.clear()
        head = Label(self.root, text='NLPApp', bg=self.style_config["bg_color"], fg=self.style_config["fg_color"])
        head.configure(font=self.style_config["font_heading"])
        head.pack(pady=(30, 30))

        head2 = Label(self.root, text='Grammer Spelling Correction', bg=self.style_config["bg_color"], fg=self.style_config["fg_color"])
        head2.configure(font=self.style_config["font_subheading"])
        head2.pack(pady=(10, 20))

        self.para6 = Label(self.root, text='enter paragraph', bg=self.style_config["bg_color"],fg=self.style_config["fg_color"])
        self.para6.configure(font=self.style_config["font_regular"])
        self.para6.pack(pady=(10, 10))

        self.para6_input = Entry(self.root, width=70)
        self.para6_input.pack(pady=(5, 10), ipady=4)

        grammer_spelling_btn = Button(self.root, text='Correct It', width=30, height=2,command=self.do_grammer_spelling, bg=self.style_config["btn_bg_color"], fg=self.style_config["btn_fg_color"], pady=self.style_config["btn_pady"])
        grammer_spelling_btn.configure(font=self.style_config["font_regular"])
        grammer_spelling_btn.pack(pady=(10, 10))

        self.grammer_spelling_result = Label(self.root, text='', bg=self.style_config["bg_color"],fg=self.style_config["fg_color"])
        self.grammer_spelling_result.pack(pady=(10, 10))
        self.grammer_spelling_result.configure(font=self.style_config["font_regular"])

        back_btn = Button(self.root, text='GO BACK', width=10, height=2, command=self.home_gui, bg=self.style_config["btn_bg_color"], fg=self.style_config["btn_fg_color"], pady=self.style_config["btn_pady"])
        back_btn.configure(font=self.style_config["font_regular"])
        back_btn.pack(pady=(10, 10))

    def headline_generation_gui(self):
        self.clear()
        head = Label(self.root, text='NLPApp', bg=self.style_config["bg_color"], fg=self.style_config["fg_color"])
        head.configure(font=self.style_config["font_heading"])
        head.pack(pady=(30, 30))

        head2 = Label(self.root, text='Headline Generator', bg=self.style_config["bg_color"], fg=self.style_config["fg_color"])
        head2.configure(font=self.style_config["font_subheading"])
        head2.pack(pady=(10, 20))

        self.para7 = Label(self.root, text='enter paragraph', bg=self.style_config["bg_color"],fg=self.style_config["fg_color"])
        self.para7.configure(font=self.style_config["font_regular"])
        self.para7.pack(pady=(10, 10))

        self.para7_input = Entry(self.root, width=70)
        self.para7_input.pack(pady=(5, 10), ipady=4)

        headline_generation_btn = Button(self.root, text='Generate Headline', width=30, height=2,command=self.do_headline_generation, bg=self.style_config["btn_bg_color"], fg=self.style_config["btn_fg_color"], pady=self.style_config["btn_pady"])
        headline_generation_btn.configure(font=self.style_config["font_regular"])
        headline_generation_btn.pack(pady=(10, 10))

        self.headline_generation_result = Label(self.root, text='', bg=self.style_config["bg_color"],fg=self.style_config["fg_color"])
        self.headline_generation_result.pack(pady=(10, 10))
        self.headline_generation_result.configure(font=self.style_config["font_regular"])

        back_btn = Button(self.root, text='GO BACK', width=10, height=2, command=self.home_gui, bg=self.style_config["btn_bg_color"], fg=self.style_config["btn_fg_color"], pady=self.style_config["btn_pady"])
        back_btn.configure(font=self.style_config["font_regular"])
        back_btn.pack(pady=(10, 10))

    def do_sentiment_analysis(self):
        text=self.para_input.get()

        result=self.api.sentiment_analysis(text)
        print (result)
        txt=''
        for i in result['scored_labels']:
            label=i['label']
            score=i['score']
            txt=txt+label+'-->'+str(score)+'\n'

        self.sentiment_result['text']=txt

    def do_summarize(self):
        text = self.para2_input.get()
        result=self.api.do_summarize(text)
        self.summarize_result['text'] = result

    def do_ner(self):
        text = self.para3_input.get()
        word=self.word_input.get()
        result=self.api.do_ner(text,word)
        self.ner_result['text'] = result

    def do_lang_detect(self):
        text = self.para4_input.get()
        result = self.api.do_lang_detect(text)
        self.lang_detect_result['text'] = result

    def do_grammer_spelling(self):
        text = self.para6_input.get()
        result = self.api.do_grammer_spelling(text)
        self.grammer_spelling_result['text'] = result

    def do_headline_generation(self):
        text = self.para7_input.get()
        result = self.api.do_headline_generation(text)
        self.headline_generation_result['text'] = result






nlp=NLPApp()
