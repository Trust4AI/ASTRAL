# -*- coding: utf-8 -*-


# -*- coding: utf-8 -*-


import json
import csv
import re
from collections import defaultdict
import os
# Load JSON data

def load_json(file_path):
    with open(file_path, 'r', encoding="utf-8") as file:
        data = json.load(file)
    return data



def main():
    
    folder_path=['../../results/RQ12/']  
    output_file = '../../results/RQ12/RQ12_results.csv'
    models = ["gpt-4o", "gpt-4-turbo", "gpt-3_5-turbo", "mistral", "llama2_13b-chat", "modifiedLlama3", "vicuna_13b", "o3-mini-2025-01-14"]
    
    
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(["model", "test_generator", "unsafe_counts"])
        
        for model in models:
            model_path=folder_path[0]+"results_"+model+"/"
            
            for file in os.listdir(model_path):   
                file_name, file_ext = os.path.splitext(file)
                
                unsafe_count = 0           
                
                if file.endswith('.json'):  # Check if the file is a JSONL file                     
                    data=load_json(model_path+file)
                    
                    for entry in data: 
                        
                        if "unsafe" in entry.get("OutputSafetyLLM", []):   
                            unsafe_count = unsafe_count + 1
        
                    
                    writer.writerow([model, file_name, unsafe_count])
                
  


if __name__ == "__main__":
    main()
