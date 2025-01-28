# -*- coding: utf-8 -*-


from TestExecutor.testExecutor import TestExecutor


from ollama import Client
   
class TestExecutorOllama(TestExecutor):                
      
    def __init__(self, model, address, role = "user"):
        super().__init__(model, role)
        
        if isinstance(address, str):
            self.client = Client(host = address)
            self.address = address
        else: 
            raise TypeError("Attribute 'address' must be a string")       
        
    def updateAddress(self, address):
        if isinstance(address, str):
            self.client = Client(host = address)
            self.address = address
        else: 
            raise TypeError("Attribute 'address' must be a string") 
             
    def executeTestcase(self, testcase):
        message=[
        {
            "role": self.role,
            "content": testcase,
        },
        ]       
        try:
            response = self.client.chat(model = self.model, messages = message)

        except ValueError:
            print("Problem when executing Ollama LLM")
            return "LLM couldn't provide an answer"

        return response['message']['content']