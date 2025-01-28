# -*- coding: utf-8 -*-

from TestExecutor.testExecutor import TestExecutor

from openai import OpenAI 
import openai

class TestExecutorGPT(TestExecutor):
    
    def __init__(self, model, token, role = "user"):
        #if isinstance(attribute, type) -ekin konprobatu type egokiak direla
        super().__init__(model, role)
        
        if isinstance(token, str):
            self.client = OpenAI(
               api_key = token
               )
            self.token = token
        else: 
            raise TypeError("Attribute 'GPT_token' must be a string")       
        
    def updateToken(self, token):
        if isinstance(token, str):
            self.client = OpenAI(
               api_key = token
               )
            self.token = token
        else: 
            raise TypeError("Attribute 'GPT_token' must be a string")

        
    def executeTestcase(self, testcase):
        try:
            completion = self.client.chat.completions.create(model = self.model, messages = [{"role": self.role, "content": testcase}])
        
        except openai.BadRequestError as e:
            error_message = str(e)
            print("LLM couldn't provide an answer due to a policy violation in the prompt")
            return "policy violation"
        
        except ValueError:
            print("Problem when executing GPT LLM")
            return "error"
    
        
        return completion.choices[0].message.content
    
