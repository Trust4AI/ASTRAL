# -*- coding: utf-8 -*-


import os
import json
import uuid

class JSONWriter:

    def write_to_json(json_data, json_file):
        if not os.path.isfile(json_file) or os.path.getsize(json_file) == 0:
            with open(json_file, 'w', newline='', encoding='utf-8') as f:
                json.dump(json_data, f, indent=4)
               
    def append_to_json(json_data, json_file):
        
        directory = os.path.dirname(json_file)
        
        if not os.path.exists(directory) and directory != '':
            os.makedirs(directory)
        
        if not os.path.isfile(json_file) or os.path.getsize(json_file) == 0:
            with open(json_file, 'w', newline='', encoding='utf-8') as f:
                f.write("[\n")
                json.dump(json_data, f, indent=4)
        else:
           
            with open(json_file, 'a', newline='', encoding='utf-8') as f:
                f.write(',\n')  # Ensure the new data starts on a new line
                json.dump(json_data, f, indent=4)
                
    
    def close_json(filepath):
         """Close the JSON array by adding a closing bracket."""
         with open(filepath, 'a') as f:
             f.write("\n]\n")


    def append_data_to_json(json_output, testcase, llmOutput, **kwargs):
         
        try:
            data = {
                "ID": uuid.uuid1().hex,
                "testcase": testcase,
                "LLM output": llmOutput
            }
            
            for key, value in kwargs.items():
                data[key] = value
        
            json_output.append(data)

        except ValueError:
        
            print("failed appending ")
            
        return json_output