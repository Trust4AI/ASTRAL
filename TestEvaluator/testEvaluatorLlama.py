# -*- coding: utf-8 -*-


from TestEvaluator.testEvaluatorOllama import TestEvaluatorOllama
   
class TestEvaluatorLlama(TestEvaluatorOllama):                
      
    def __init__(self, model, system_prompt, user_message, address):
        super().__init__(model, system_prompt, user_message, address)
        

    def evaluateLLMOuput(self, output):
        
        enforcing_message = "Provide your response in json format, nothing else"
                  
        message=[
        {
            "role": "system",
            "content":  self.system_prompt + enforcing_message
        },
        {
            "role": "user",
            "content":  self.user_message.format(LLMOutput=output)
        },
        ]
        try:
            response = self.client.chat(model = self.model, messages = message)

        except ValueError:
            print("Problem when executing LLM")
            return "LLM couldn't provide an answer"

        return response['message']['content']