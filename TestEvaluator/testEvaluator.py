# -*- coding: utf-8 -*-


from abc import ABC, abstractmethod

class TestEvaluator(ABC):              
      
    def __init__(self, model, system_prompt, user_message):
        if isinstance(model, str):           
            self.model = model
        else:
            raise TypeError("Attribute 'model' must be a string")
        
        if isinstance(system_prompt, str):           
            self.system_prompt = system_prompt
        else:
            raise TypeError("Attribute 'system_prompt' must be a string")
            
        if isinstance(user_message, str):           
            self.user_message = user_message
        else:
            raise TypeError("Attribute 'user_message' must be a string")

        
    @abstractmethod
    def evaluateLLMOuput(self, ouput):
        pass
    
    def update_model(self, model):
        if isinstance(model, str):           
            self.model = model
        else:
            raise TypeError("Attribute 'model' must be a string")
        
    def update_systemPrompt(self, system_prompt):
        if isinstance(system_prompt, str):           
            self.system_prompt = system_prompt
        else:
            raise TypeError("Attribute 'system_prompt' must be a string")
    
    def update_userMessage(self, user_message):
        if isinstance(user_message, str):           
            self.user_message = user_message
        else:
            raise TypeError("Attribute 'user_message' must be a string")

