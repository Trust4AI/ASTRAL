# -*- coding: utf-8 -*-

from TestEvaluator.testEvaluator import TestEvaluator
from abc import ABC, abstractmethod

from ollama import Client
   
class TestEvaluatorOllama(TestEvaluator, ABC):                
      
    def __init__(self, model, system_prompt, user_message, address):
        super().__init__(model, system_prompt, user_message)
        
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


    def evaluateLLMOuput(self, output):
        
        pass