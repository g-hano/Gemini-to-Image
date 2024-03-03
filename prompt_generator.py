import langchain_google_genai as genai
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os
load_dotenv()
api_key=os.environ.get("GOOGLE_API_KEY")

class PromptGenerator:
    def __init__(self, verbose: bool=True, temp: float=0.8):
        self.llm = genai.GoogleGenerativeAI(model="gemini-pro",
                                            verbose=verbose,
                                            temperature=temp,
                                            top_k=1,
                                            top_p=1,
                                            max_output_tokens=2048,
                                            google_api_key=api_key)
        
        self.template = """Do not wrap your answer in quotes. Always answer only with your response.
        Let's say you are a professional prompt engineer and you are invited to an university
        to talk about prompt engineering. One of the students asked you to create a better prompt 
        for an text to image model given this sentence:

        Sentence: {input}

        Answer: """
        
        self.prompt_template = PromptTemplate(input_variables=["input"], template=self.template)
        
    def get_response(self, input_sentence):
        prompt = self.prompt_template.format(input=input_sentence)
        response = self.llm.invoke(prompt)
        return response