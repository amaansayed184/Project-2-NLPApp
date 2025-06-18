import nlpcloud
class API:
    def sentiment_analysis(self,text):
        client = nlpcloud.Client("finetuned-llama-3-70b", "85809261613422ef532cf0eb34f371132b97ea57", gpu=True)
        response = client.sentiment(text, target="NLP Cloud")

        return response

    def do_summarize(self,text):
        client = nlpcloud.Client("finetuned-llama-3-70b", "8fe1f51cef36cc699628de36581a15bdaceac742", gpu=True)

        response=client.summarization(text, size="small")
        return response

    def do_ner(self,text,word):
        client = nlpcloud.Client("finetuned-llama-3-70b", "e77aacb58d577d590fb2fabf00186ce892b496a8", gpu=True)
        response = client.entities(text, searched_entity=word)

        return response

    def do_lang_detect(self,text):
        client = nlpcloud.Client("python-langdetect", "4e604f493b0fc3eaaae0e27983bceb507303ee98", gpu=False)
        response=client.langdetection(text)
        return response

    def do_grammer_spelling(self,text):
        client = nlpcloud.Client("finetuned-llama-3-70b", "36f1ad86326b647c72eb589a2cf8d8e50497bcb1", gpu=True)
        return client.gs_correction(text)

    def do_headline_generation(self,text):
        client = nlpcloud.Client("t5-base-en-generate-headline", "8fe1f51cef36cc699628de36581a15bdaceac742", gpu=False)
        return client.summarization(text)