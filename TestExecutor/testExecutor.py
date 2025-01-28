# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

class TestExecutor(ABC):              
      
    def __init__(self, model, role = "user"):
        if isinstance(model, str):           
            self.model = model
        else:
            raise TypeError("Attribute 'model' must be a string")
            
        if isinstance(role, str):           
            self.role = role
        else:
            raise TypeError("Attribute 'role' must be a string")
        
    @abstractmethod
    def executeTestcase(self, testcase):
        pass
        
    def update_model(self, model):
        if isinstance(model, str):           
            self.model = model
        else:
            raise TypeError("Attribute 'model' must be a string")
    
    def update_role(self, role):
        if isinstance(role, str):           
            self.role = role
        else:
            raise TypeError("Attribute 'role' must be a string")

