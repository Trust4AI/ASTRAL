# -*- coding: utf-8 -*-

from TestGenerator.testGenerator_coverage import TestGenerator #ASTRAL (RAG+FS)
from TestGenerator.assistant import Assistant
from JSONWriter.jsonWriter import JSONWriter

import uuid
import time
import settings


def main(): 
    
    API_KEY = settings.API_KEY 
    assistant_id = settings.assistant_id_ASTRAL_RAG 
    
    outputFolder="results/RQ12/" #update this
    filename="ASTRAL_RAG_FS.json"
    DEFAULT_TESTS = 3    
       
    # Retrieve an existing assistant
    assistant = Assistant(API_KEY)
    assistant.retrieveAssistant(assistant_id)
    
    numTests=1
    test_generators=[]
    N = len(TestGenerator.categories)
    M = len(TestGenerator.available_styles)
    Z = len(TestGenerator.available_techniques)

    # Initialize coverage matrix 
    coverage = [[[0 for _ in range(Z)] for _ in range(M)] for _ in range(N)]
     
           
    for category in TestGenerator.categories:
        for style in TestGenerator.available_styles: 
            for technique in TestGenerator.available_techniques: 
                test_generators.append(TestGenerator(assistant, numTests, category, style, technique))
    
            
    for test_generator in test_generators:        
        
        for k in range(DEFAULT_TESTS):
            t_start=time.time()
            testcases = test_generator.generateTestcases()
            t_end=time.time()
            
            for testcase in testcases:
                coverage[TestGenerator.categories.index(test_generator.category)][TestGenerator.available_styles.index(test_generator.style)][TestGenerator.available_techniques.index(test_generator.technique)] += 1
                data={
                "testcase":testcase,
                "category":test_generator.category,
                "technique": test_generator.technique,
                "style": test_generator.style,
                "id": uuid.uuid4().hex,
                "gen_time":t_end-t_start
                }
                JSONWriter.append_to_json(data, outputFolder+filename) 
                
    JSONWriter.close_json(outputFolder+filename)
                                                                     
   

            
if __name__ == "__main__":
    main()
