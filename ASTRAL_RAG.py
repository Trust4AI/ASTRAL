# -*- coding: utf-8 -*-

from TestGenerator.testGenerator import TestGenerator           # ASTRAL (RAG)
from TestGenerator.assistant import Assistant
from JSONWriter.jsonWriter import JSONWriter

import uuid
import time
import settings 


def main():  
    
    API_KEY = settings.API_KEY 
    assistant_id = settings.assistant_id_ASTRAL_RAG  
    
    outputFolder="results/RQ12/" 
    filename="ASTRAL_RAG.json"
    DEFAULT_TESTS = 3    
        
    # Retrieve an existing assistant
    assistant = Assistant(API_KEY)
    assistant.retrieveAssistant(assistant_id)

    numTests=1
    test_generators=[]


    for category in TestGenerator.categories:
        test_generators.append(TestGenerator(assistant, numTests, category))
            
    
    for test_generator in test_generators:        
        
        for k in range(DEFAULT_TESTS):
            t_start=time.time()
            testcases = test_generator.generateTestcases()
            t_end=time.time()
            
            for testcase in testcases:

                data={
                "testcase":testcase,
                "category":test_generator.category,
                "id": uuid.uuid4().hex,
                "gen_time":t_end-t_start
                }
                JSONWriter.append_to_json(data, outputFolder+filename) 
                
    JSONWriter.close_json(outputFolder+filename)
    
                                                  

            
if __name__ == "__main__":
    main()
