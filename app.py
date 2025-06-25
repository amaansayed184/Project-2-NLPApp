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
            "bg_color": "#0A192F",  # Deep space blue
            "fg_color": "#CCD6F6",  # Light silver for general text
            "accent_color": "#64FFDA",  # Neon cyan for primary accents
            "btn_bg_color": "#112240",  # Slightly lighter blue-grey
            "btn_fg_color": "#64FFDA",  # Neon cyan for button text
            "btn_hover_bg_color": "#1F3A5F", # A slightly brighter blue for hover
            "input_bg_color": "#0A192F", # Matching main background
            "input_fg_color": "#64FFDA", # Neon cyan for input text
            "input_border_color": "#64FFDA", # Neon cyan for input field border
            "font_heading": ('Helvetica Neue', 26, 'bold'),
            "font_subheading": ('Helvetica Neue', 20),
            "font_regular": ('Helvetica Neue', 12),
            "font_button": ('Helvetica Neue', 12, 'bold'),
            "btn_pady": 7,
            "label_pady_general": (10,5), # General padding for standard labels
            "label_pady_header": (30,15), # Padding for main headers like "NLPApp"
            "label_pady_subheader": (15,10), # Padding for subheaders like "Login Page"
            "entry_ipady": 5, # internal padding for entry fields
            "entry_borderwidth": 1 # borderwidth for the frame around entry
        }

        self.root.configure(bg=self.style_config["bg_color"])

        self.login_gui()


        self.root.mainloop()

    def login_gui(self):
        self.clear()
        head=Label(self.root,text='NLPApp',bg=self.style_config["bg_color"],fg=self.style_config["accent_color"])
        head.configure(font=self.style_config["font_heading"])
        head.pack(pady=self.style_config["label_pady_header"])

        head2 = Label(self.root, text='Login Page', bg=self.style_config["bg_color"], fg=self.style_config["fg_color"])
        head2.configure(font=self.style_config["font_subheading"])
        head2.pack(pady=self.style_config["label_pady_subheader"])

        label1=Label(self.root,text='Enter Email',bg=self.style_config["bg_color"],fg=self.style_config["fg_color"])
        label1.configure(font=self.style_config["font_regular"])
        label1.pack(pady=self.style_config["label_pady_general"])

        email_frame = Frame(self.root, background=self.style_config["input_border_color"], borderwidth=self.style_config["entry_borderwidth"], relief="flat")
        self.email_input= Entry(email_frame,width=50, bg=self.style_config["input_bg_color"], fg=self.style_config["input_fg_color"], insertbackground=self.style_config["accent_color"], relief="flat", borderwidth=0)
        self.email_input.pack(pady=(0,0),ipady=self.style_config["entry_ipady"], padx=1, pady=1) # padx/pady for inner frame border
        email_frame.pack(pady=(5,10))


        label2 = Label(self.root, text='Enter Password',bg=self.style_config["bg_color"],fg=self.style_config["fg_color"])
        label2.configure(font=self.style_config["font_regular"])
        label2.pack(pady=self.style_config["label_pady_general"])

        password_frame = Frame(self.root, background=self.style_config["input_border_color"], borderwidth=self.style_config["entry_borderwidth"], relief="flat")
        self.password_input = Entry(password_frame, width=50,show='*', bg=self.style_config["input_bg_color"], fg=self.style_config["input_fg_color"], insertbackground=self.style_config["accent_color"], relief="flat", borderwidth=0)
        self.password_input.pack(pady=(0,0),ipady=self.style_config["entry_ipady"], padx=1, pady=1)
        password_frame.pack(pady=(5,10))

        login_btn=Button(self.root,text='Login',width=12,command=self.login_perform,
                         bg=self.style_config["btn_bg_color"], fg=self.style_config["btn_fg_color"],
                         font=self.style_config["font_button"], pady=self.style_config["btn_pady"],
                         relief="flat", activebackground=self.style_config["btn_hover_bg_color"], activeforeground=self.style_config["accent_color"])
        login_btn.pack(pady=(20,10))

        label3 = Label(self.root, text='Not a member?',bg=self.style_config["bg_color"],fg=self.style_config["fg_color"])
        label3.configure(font=self.style_config["font_regular"])
        label3.pack(pady=(20,self.style_config["label_pady_general"][1]))

        redirect_btn = Button(self.root, text='Register Now', width=12,command=self.register_gui,
                              bg=self.style_config["btn_bg_color"], fg=self.style_config["btn_fg_color"],
                              font=self.style_config["font_button"], pady=self.style_config["btn_pady"],
                              relief="flat", activebackground=self.style_config["btn_hover_bg_color"], activeforeground=self.style_config["accent_color"])
        redirect_btn.pack(pady=(10, 10))

    def register_gui(self):
        self.clear()

        head = Label(self.root, text='NLPApp', bg=self.style_config["bg_color"], fg=self.style_config["accent_color"])
        head.configure(font=self.style_config["font_heading"])
        head.pack(pady=self.style_config["label_pady_header"])

        head2 = Label(self.root, text='Registration Page', bg=self.style_config["bg_color"], fg=self.style_config["fg_color"])
        head2.configure(font=self.style_config["font_subheading"])
        head2.pack(pady=self.style_config["label_pady_subheader"])

        label0 = Label(self.root, text='Enter Name', bg=self.style_config["bg_color"],fg=self.style_config["fg_color"])
        label0.configure(font=self.style_config["font_regular"])
        label0.pack(pady=self.style_config["label_pady_general"])

        name_frame = Frame(self.root, background=self.style_config["input_border_color"], borderwidth=self.style_config["entry_borderwidth"], relief="flat")
        self.name_input = Entry(name_frame, width=50, bg=self.style_config["input_bg_color"], fg=self.style_config["input_fg_color"], insertbackground=self.style_config["accent_color"], relief="flat", borderwidth=0)
        self.name_input.pack(pady=(0,0),ipady=self.style_config["entry_ipady"], padx=1, pady=1)
        name_frame.pack(pady=(5,10))


        label1 = Label(self.root, text='Enter Email', bg=self.style_config["bg_color"],fg=self.style_config["fg_color"])
        label1.configure(font=self.style_config["font_regular"])
        label1.pack(pady=self.style_config["label_pady_general"])

        email_frame = Frame(self.root, background=self.style_config["input_border_color"], borderwidth=self.style_config["entry_borderwidth"], relief="flat")
        self.email_input = Entry(email_frame, width=50, bg=self.style_config["input_bg_color"], fg=self.style_config["input_fg_color"], insertbackground=self.style_config["accent_color"], relief="flat", borderwidth=0)
        self.email_input.pack(pady=(0,0),ipady=self.style_config["entry_ipady"], padx=1, pady=1)
        email_frame.pack(pady=(5,10))

        label2 = Label(self.root, text='Enter Password', bg=self.style_config["bg_color"],fg=self.style_config["fg_color"])
        label2.configure(font=self.style_config["font_regular"])
        label2.pack(pady=self.style_config["label_pady_general"])

        password_frame = Frame(self.root, background=self.style_config["input_border_color"], borderwidth=self.style_config["entry_borderwidth"], relief="flat")
        self.password_input = Entry(password_frame, width=50, show='*', bg=self.style_config["input_bg_color"], fg=self.style_config["input_fg_color"], insertbackground=self.style_config["accent_color"], relief="flat", borderwidth=0)
        self.password_input.pack(pady=(0,0),ipady=self.style_config["entry_ipady"], padx=1, pady=1)
        password_frame.pack(pady=(5,10))

        register_btn = Button(self.root, text='Register', width=12,command=self.register_perform,
                              bg=self.style_config["btn_bg_color"], fg=self.style_config["btn_fg_color"],
                              font=self.style_config["font_button"], pady=self.style_config["btn_pady"],
                              relief="flat", activebackground=self.style_config["btn_hover_bg_color"], activeforeground=self.style_config["accent_color"])
        register_btn.pack(pady=(20, 10))

        label3 = Label(self.root, text='Already Registered?', bg=self.style_config["bg_color"],fg=self.style_config["fg_color"])
        label3.configure(font=self.style_config["font_regular"])
        label3.pack(pady=(20,self.style_config["label_pady_general"][1]))

        redirect_btn = Button(self.root, text='Login Now', width=12, command=self.login_gui,
                              bg=self.style_config["btn_bg_color"], fg=self.style_config["btn_fg_color"],
                              font=self.style_config["font_button"], pady=self.style_config["btn_pady"],
                              relief="flat", activebackground=self.style_config["btn_hover_bg_color"], activeforeground=self.style_config["accent_color"])
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
        head = Label(self.root, text='NLPApp', bg=self.style_config["bg_color"], fg=self.style_config["accent_color"])
        head.configure(font=self.style_config["font_heading"])
        head.pack(pady=self.style_config["label_pady_header"])

        button_width = 35 # Increased width for better aesthetics
        button_pady = (10,5) # Standard pady for home screen buttons

        sentiment_analysis_btn = Button(self.root, text='Sentiment Analysis', width=button_width, command=self.sentiment_gui,
                                        bg=self.style_config["btn_bg_color"], fg=self.style_config["btn_fg_color"],
                                        font=self.style_config["font_button"], pady=self.style_config["btn_pady"],
                                        relief="flat", activebackground=self.style_config["btn_hover_bg_color"], activeforeground=self.style_config["accent_color"])
        sentiment_analysis_btn.pack(pady=button_pady)

        NER_analysis_btn = Button(self.root, text='Named Entity Recognition', width=button_width, command=self.ner_gui,
                                  bg=self.style_config["btn_bg_color"], fg=self.style_config["btn_fg_color"],
                                  font=self.style_config["font_button"], pady=self.style_config["btn_pady"],
                                  relief="flat", activebackground=self.style_config["btn_hover_bg_color"], activeforeground=self.style_config["accent_color"])
        NER_analysis_btn.pack(pady=button_pady)

        summerization_btn = Button(self.root, text='Summarization', width=button_width, command=self.summarization_gui,
                                   bg=self.style_config["btn_bg_color"], fg=self.style_config["btn_fg_color"],
                                   font=self.style_config["font_button"], pady=self.style_config["btn_pady"],
                                   relief="flat", activebackground=self.style_config["btn_hover_bg_color"], activeforeground=self.style_config["accent_color"])
        summerization_btn.pack(pady=button_pady)

        grammer_spelling_btn = Button(self.root, text='Grammar & Spelling Correction', width=button_width, command=self.grammer_spelling_gui,
                                      bg=self.style_config["btn_bg_color"], fg=self.style_config["btn_fg_color"],
                                      font=self.style_config["font_button"], pady=self.style_config["btn_pady"],
                                      relief="flat", activebackground=self.style_config["btn_hover_bg_color"], activeforeground=self.style_config["accent_color"])
        grammer_spelling_btn.pack(pady=button_pady)

        language_detection_btn = Button(self.root, text='Language Detection', width=button_width, command=self.lang_detect_gui,
                                        bg=self.style_config["btn_bg_color"], fg=self.style_config["btn_fg_color"],
                                        font=self.style_config["font_button"], pady=self.style_config["btn_pady"],
                                        relief="flat", activebackground=self.style_config["btn_hover_bg_color"], activeforeground=self.style_config["accent_color"])
        language_detection_btn.pack(pady=button_pady)

        headline_generation_btn = Button(self.root, text='Headline Generation', width=button_width, command=self.headline_generation_gui,
                                         bg=self.style_config["btn_bg_color"], fg=self.style_config["btn_fg_color"],
                                         font=self.style_config["font_button"], pady=self.style_config["btn_pady"],
                                         relief="flat", activebackground=self.style_config["btn_hover_bg_color"], activeforeground=self.style_config["accent_color"])
        headline_generation_btn.pack(pady=button_pady)

        logout_btn = Button(self.root, text='Logout', width=12, command=self.login_gui,
                            bg=self.style_config["btn_bg_color"], fg=self.style_config["btn_fg_color"],
                            font=self.style_config["font_button"], pady=self.style_config["btn_pady"],
                            relief="flat", activebackground=self.style_config["btn_hover_bg_color"], activeforeground=self.style_config["accent_color"])
        logout_btn.pack(pady=(20, 10))

    def sentiment_gui(self):
        self.clear()
        head = Label(self.root, text='NLPApp', bg=self.style_config["bg_color"], fg=self.style_config["accent_color"])
        head.configure(font=self.style_config["font_heading"])
        head.pack(pady=self.style_config["label_pady_header"])

        head2 = Label(self.root, text='Sentiment Analysis', bg=self.style_config["bg_color"], fg=self.style_config["fg_color"])
        head2.configure(font=self.style_config["font_subheading"])
        head2.pack(pady=self.style_config["label_pady_subheader"])

        self.para = Label(self.root, text='Enter Paragraph', bg=self.style_config["bg_color"],fg=self.style_config["fg_color"])
        self.para.configure(font=self.style_config["font_regular"])
        self.para.pack(pady=self.style_config["label_pady_general"])

        para_frame = Frame(self.root, background=self.style_config["input_border_color"], borderwidth=self.style_config["entry_borderwidth"], relief="flat")
        self.para_input = Entry(para_frame, width=70, bg=self.style_config["input_bg_color"], fg=self.style_config["input_fg_color"], insertbackground=self.style_config["accent_color"], relief="flat", borderwidth=0)
        self.para_input.pack(ipady=self.style_config["entry_ipady"], padx=1, pady=1)
        para_frame.pack(pady=(5,10))


        analysis_btn = Button(self.root, text='Analyze Sentiment', width=25,command=self.do_sentiment_analysis,
                              bg=self.style_config["btn_bg_color"], fg=self.style_config["btn_fg_color"],
                              font=self.style_config["font_button"], pady=self.style_config["btn_pady"],
                              relief="flat", activebackground=self.style_config["btn_hover_bg_color"], activeforeground=self.style_config["accent_color"])
        analysis_btn.pack(pady=(20, 10))

        self.sentiment_result = Label(self.root, text='', bg=self.style_config["bg_color"],fg=self.style_config["accent_color"], justify=LEFT)
        self.sentiment_result.pack(pady=self.style_config["label_pady_general"])
        self.sentiment_result.configure(font=self.style_config["font_regular"])

        back_btn = Button(self.root, text='Go Back', width=12, command=self.home_gui,
                          bg=self.style_config["btn_bg_color"], fg=self.style_config["btn_fg_color"],
                          font=self.style_config["font_button"], pady=self.style_config["btn_pady"],
                          relief="flat", activebackground=self.style_config["btn_hover_bg_color"], activeforeground=self.style_config["accent_color"])
        back_btn.pack(pady=(20, 10))


    def summarization_gui(self):
        self.clear()
        head = Label(self.root, text='NLPApp', bg=self.style_config["bg_color"], fg=self.style_config["accent_color"])
        head.configure(font=self.style_config["font_heading"])
        head.pack(pady=self.style_config["label_pady_header"])

        head2 = Label(self.root, text='Summarization', bg=self.style_config["bg_color"], fg=self.style_config["fg_color"])
        head2.configure(font=self.style_config["font_subheading"])
        head2.pack(pady=self.style_config["label_pady_subheader"])

        self.para2 = Label(self.root, text='Enter Paragraph', bg=self.style_config["bg_color"],fg=self.style_config["fg_color"])
        self.para2.configure(font=self.style_config["font_regular"])
        self.para2.pack(pady=self.style_config["label_pady_general"])

        para2_frame = Frame(self.root, background=self.style_config["input_border_color"], borderwidth=self.style_config["entry_borderwidth"], relief="flat")
        self.para2_input = Entry(para2_frame, width=70, bg=self.style_config["input_bg_color"], fg=self.style_config["input_fg_color"], insertbackground=self.style_config["accent_color"], relief="flat", borderwidth=0)
        self.para2_input.pack(ipady=self.style_config["entry_ipady"], padx=1, pady=1)
        para2_frame.pack(pady=(5,10))

        summarize_btn = Button(self.root, text='Summarize It', width=25,command=self.do_summarize,
                               bg=self.style_config["btn_bg_color"], fg=self.style_config["btn_fg_color"],
                               font=self.style_config["font_button"], pady=self.style_config["btn_pady"],
                               relief="flat", activebackground=self.style_config["btn_hover_bg_color"], activeforeground=self.style_config["accent_color"])
        summarize_btn.pack(pady=(20, 10))

        self.summarize_result = Label(self.root, text='', bg=self.style_config["bg_color"],fg=self.style_config["accent_color"], justify=LEFT, wraplength=450)
        self.summarize_result.pack(pady=self.style_config["label_pady_general"])
        self.summarize_result.configure(font=self.style_config["font_regular"])

        back_btn = Button(self.root, text='Go Back', width=12, command=self.home_gui,
                          bg=self.style_config["btn_bg_color"], fg=self.style_config["btn_fg_color"],
                          font=self.style_config["font_button"], pady=self.style_config["btn_pady"],
                          relief="flat", activebackground=self.style_config["btn_hover_bg_color"], activeforeground=self.style_config["accent_color"])
        back_btn.pack(pady=(20, 10))

    def ner_gui(self):
        self.clear()
        head = Label(self.root, text='NLPApp', bg=self.style_config["bg_color"], fg=self.style_config["accent_color"])
        head.configure(font=self.style_config["font_heading"])
        head.pack(pady=self.style_config["label_pady_header"])

        head2 = Label(self.root, text='Named Entity Recognition', bg=self.style_config["bg_color"], fg=self.style_config["fg_color"])
        head2.configure(font=self.style_config["font_subheading"])
        head2.pack(pady=self.style_config["label_pady_subheader"])

        self.para3 = Label(self.root, text='Enter Paragraph', bg=self.style_config["bg_color"],fg=self.style_config["fg_color"])
        self.para3.configure(font=self.style_config["font_regular"])
        self.para3.pack(pady=self.style_config["label_pady_general"])

        para3_frame = Frame(self.root, background=self.style_config["input_border_color"], borderwidth=self.style_config["entry_borderwidth"], relief="flat")
        self.para3_input = Entry(para3_frame, width=70, bg=self.style_config["input_bg_color"], fg=self.style_config["input_fg_color"], insertbackground=self.style_config["accent_color"], relief="flat", borderwidth=0)
        self.para3_input.pack(ipady=self.style_config["entry_ipady"], padx=1, pady=1)
        para3_frame.pack(pady=(5,10))

        self.word = Label(self.root, text='Enter Word to Search', bg=self.style_config["bg_color"],fg=self.style_config["fg_color"])
        self.word.configure(font=self.style_config["font_regular"])
        self.word.pack(pady=self.style_config["label_pady_general"])

        word_frame = Frame(self.root, background=self.style_config["input_border_color"], borderwidth=self.style_config["entry_borderwidth"], relief="flat")
        self.word_input = Entry(word_frame, width=70, bg=self.style_config["input_bg_color"], fg=self.style_config["input_fg_color"], insertbackground=self.style_config["accent_color"], relief="flat", borderwidth=0)
        self.word_input.pack(ipady=self.style_config["entry_ipady"], padx=1, pady=1)
        word_frame.pack(pady=(5,10))

        ner_btn = Button(self.root, text='Search Entity', width=25,command=self.do_ner,
                         bg=self.style_config["btn_bg_color"], fg=self.style_config["btn_fg_color"],
                         font=self.style_config["font_button"], pady=self.style_config["btn_pady"],
                         relief="flat", activebackground=self.style_config["btn_hover_bg_color"], activeforeground=self.style_config["accent_color"])
        ner_btn.pack(pady=(20, 10))

        self.ner_result = Label(self.root, text='', bg=self.style_config["bg_color"],fg=self.style_config["accent_color"], justify=LEFT, wraplength=450)
        self.ner_result.pack(pady=self.style_config["label_pady_general"])
        self.ner_result.configure(font=self.style_config["font_regular"])

        back_btn = Button(self.root, text='Go Back', width=12, command=self.home_gui,
                          bg=self.style_config["btn_bg_color"], fg=self.style_config["btn_fg_color"],
                          font=self.style_config["font_button"], pady=self.style_config["btn_pady"],
                          relief="flat", activebackground=self.style_config["btn_hover_bg_color"], activeforeground=self.style_config["accent_color"])
        back_btn.pack(pady=(20, 10))

    def lang_detect_gui(self):
        self.clear()
        head = Label(self.root, text='NLPApp', bg=self.style_config["bg_color"], fg=self.style_config["accent_color"])
        head.configure(font=self.style_config["font_heading"])
        head.pack(pady=self.style_config["label_pady_header"])

        head3 = Label(self.root, text='Language Detection', bg=self.style_config["bg_color"], fg=self.style_config["fg_color"])
        head3.configure(font=self.style_config["font_subheading"])
        head3.pack(pady=self.style_config["label_pady_subheader"])

        self.para4 = Label(self.root, text='Enter Paragraph', bg=self.style_config["bg_color"],fg=self.style_config["fg_color"])
        self.para4.configure(font=self.style_config["font_regular"])
        self.para4.pack(pady=self.style_config["label_pady_general"])

        para4_frame = Frame(self.root, background=self.style_config["input_border_color"], borderwidth=self.style_config["entry_borderwidth"], relief="flat")
        self.para4_input = Entry(para4_frame, width=70, bg=self.style_config["input_bg_color"], fg=self.style_config["input_fg_color"], insertbackground=self.style_config["accent_color"], relief="flat", borderwidth=0)
        self.para4_input.pack(ipady=self.style_config["entry_ipady"], padx=1, pady=1)
        para4_frame.pack(pady=(5,10))

        lang_detect_btn = Button(self.root, text='Detect Language', width=25,command=self.do_lang_detect,
                                 bg=self.style_config["btn_bg_color"], fg=self.style_config["btn_fg_color"],
                                 font=self.style_config["font_button"], pady=self.style_config["btn_pady"],
                                 relief="flat", activebackground=self.style_config["btn_hover_bg_color"], activeforeground=self.style_config["accent_color"])
        lang_detect_btn.pack(pady=(20, 10))

        self.lang_detect_result = Label(self.root, text='', bg=self.style_config["bg_color"],fg=self.style_config["accent_color"], justify=LEFT)
        self.lang_detect_result.pack(pady=self.style_config["label_pady_general"])
        self.lang_detect_result.configure(font=self.style_config["font_regular"])

        back_btn = Button(self.root, text='Go Back', width=12, command=self.home_gui,
                          bg=self.style_config["btn_bg_color"], fg=self.style_config["btn_fg_color"],
                          font=self.style_config["font_button"], pady=self.style_config["btn_pady"],
                          relief="flat", activebackground=self.style_config["btn_hover_bg_color"], activeforeground=self.style_config["accent_color"])
        back_btn.pack(pady=(20, 10))

    def grammer_spelling_gui(self):
        self.clear()
        head = Label(self.root, text='NLPApp', bg=self.style_config["bg_color"], fg=self.style_config["accent_color"])
        head.configure(font=self.style_config["font_heading"])
        head.pack(pady=self.style_config["label_pady_header"])

        head2 = Label(self.root, text='Grammar & Spelling Correction', bg=self.style_config["bg_color"], fg=self.style_config["fg_color"])
        head2.configure(font=self.style_config["font_subheading"])
        head2.pack(pady=self.style_config["label_pady_subheader"])

        self.para6 = Label(self.root, text='Enter Paragraph', bg=self.style_config["bg_color"],fg=self.style_config["fg_color"])
        self.para6.configure(font=self.style_config["font_regular"])
        self.para6.pack(pady=self.style_config["label_pady_general"])

        para6_frame = Frame(self.root, background=self.style_config["input_border_color"], borderwidth=self.style_config["entry_borderwidth"], relief="flat")
        self.para6_input = Entry(para6_frame, width=70, bg=self.style_config["input_bg_color"], fg=self.style_config["input_fg_color"], insertbackground=self.style_config["accent_color"], relief="flat", borderwidth=0)
        self.para6_input.pack(ipady=self.style_config["entry_ipady"], padx=1, pady=1)
        para6_frame.pack(pady=(5,10))

        grammer_spelling_btn = Button(self.root, text='Correct It', width=25,command=self.do_grammer_spelling,
                                      bg=self.style_config["btn_bg_color"], fg=self.style_config["btn_fg_color"],
                                      font=self.style_config["font_button"], pady=self.style_config["btn_pady"],
                                      relief="flat", activebackground=self.style_config["btn_hover_bg_color"], activeforeground=self.style_config["accent_color"])
        grammer_spelling_btn.pack(pady=(20, 10))

        self.grammer_spelling_result = Label(self.root, text='', bg=self.style_config["bg_color"],fg=self.style_config["accent_color"], justify=LEFT, wraplength=450)
        self.grammer_spelling_result.pack(pady=self.style_config["label_pady_general"])
        self.grammer_spelling_result.configure(font=self.style_config["font_regular"])

        back_btn = Button(self.root, text='Go Back', width=12, command=self.home_gui,
                          bg=self.style_config["btn_bg_color"], fg=self.style_config["btn_fg_color"],
                          font=self.style_config["font_button"], pady=self.style_config["btn_pady"],
                          relief="flat", activebackground=self.style_config["btn_hover_bg_color"], activeforeground=self.style_config["accent_color"])
        back_btn.pack(pady=(20, 10))

    def headline_generation_gui(self):
        self.clear()
        head = Label(self.root, text='NLPApp', bg=self.style_config["bg_color"], fg=self.style_config["accent_color"])
        head.configure(font=self.style_config["font_heading"])
        head.pack(pady=self.style_config["label_pady_header"])

        head2 = Label(self.root, text='Headline Generator', bg=self.style_config["bg_color"], fg=self.style_config["fg_color"])
        head2.configure(font=self.style_config["font_subheading"])
        head2.pack(pady=self.style_config["label_pady_subheader"])

        self.para7 = Label(self.root, text='Enter Paragraph', bg=self.style_config["bg_color"],fg=self.style_config["fg_color"])
        self.para7.configure(font=self.style_config["font_regular"])
        self.para7.pack(pady=self.style_config["label_pady_general"])

        para7_frame = Frame(self.root, background=self.style_config["input_border_color"], borderwidth=self.style_config["entry_borderwidth"], relief="flat")
        self.para7_input = Entry(para7_frame, width=70, bg=self.style_config["input_bg_color"], fg=self.style_config["input_fg_color"], insertbackground=self.style_config["accent_color"], relief="flat", borderwidth=0)
        self.para7_input.pack(ipady=self.style_config["entry_ipady"], padx=1, pady=1)
        para7_frame.pack(pady=(5,10))

        headline_generation_btn = Button(self.root, text='Generate Headline', width=25,command=self.do_headline_generation,
                                         bg=self.style_config["btn_bg_color"], fg=self.style_config["btn_fg_color"],
                                         font=self.style_config["font_button"], pady=self.style_config["btn_pady"],
                                         relief="flat", activebackground=self.style_config["btn_hover_bg_color"], activeforeground=self.style_config["accent_color"])
        headline_generation_btn.pack(pady=(20, 10))

        self.headline_generation_result = Label(self.root, text='', bg=self.style_config["bg_color"],fg=self.style_config["accent_color"], justify=LEFT, wraplength=450)
        self.headline_generation_result.pack(pady=self.style_config["label_pady_general"])
        self.headline_generation_result.configure(font=self.style_config["font_regular"])

        back_btn = Button(self.root, text='Go Back', width=12, command=self.home_gui,
                          bg=self.style_config["btn_bg_color"], fg=self.style_config["btn_fg_color"],
                          font=self.style_config["font_button"], pady=self.style_config["btn_pady"],
                          relief="flat", activebackground=self.style_config["btn_hover_bg_color"], activeforeground=self.style_config["accent_color"])
        back_btn.pack(pady=(20, 10))

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
