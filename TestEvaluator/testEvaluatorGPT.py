# -*- coding: utf-8 -*-

from TestEvaluator.testEvaluator import TestEvaluator

from openai import OpenAI

class TestEvaluatorGPT(TestEvaluator):
    
    def __init__(self, model, system_prompt, user_message, token):
        super().__init__(model, system_prompt, user_message)
        
        if isinstance(token, str):
            self.client = OpenAI(
               api_key = token
               )
            self.token = token
        else: 
            raise TypeError("Attribute 'token' must be a string")       
        
    def updateToken(self, token):
        if isinstance(token, str):
            self.client = OpenAI(
               api_key = token
               )
            self.token = token
        else: 
            raise TypeError("Attribute 'token' must be a string")       

        
    def evaluateLLMOuput(self, output):
        message = self.user_message.format(LLMOutput=output)
        
        try:           
            completion = self.client.chat.completions.create(model=self.model, messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": message},
                ])

        except ValueError:
            print("Problem when evaluating LLM ouput")
            return "LLM couldn't provide an answer"
        
        return completion.choices[0].message.content
    
