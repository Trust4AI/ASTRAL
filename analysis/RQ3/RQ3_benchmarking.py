# -*- coding: utf-8 -*-


import json
import csv
import re
from collections import defaultdict



categories = ["animal_abuse", "child_abuse", "controversial_topics,politics", "discrimination,stereotype,injustice",               
      "drug_abuse,weapons,banned_substance", "financial_crime,property_crime,theft",
      "hate_speech,offensive_language", "misinformation_regarding_ethics,laws_and_safety",
      "non_violent_unethical_behavior", "privacy_violation", "self_harm",
      "sexually_explicit,adult_content", "terrorism,organized_crime", "violence,aiding_and_abetting,incitement"]
              
available_styles = ["slang","uncommon_dialects","technical_terms","role_play","misspellings","question"]
available_techniques = ["evidence-based_persuasion","expert_endorsement","misrepresentation","authority_endorsement","logical_appeal"]

def load_json(file_path):
    with open(file_path, 'r', encoding="utf-8") as file:
        data = json.load(file)
    return data

# Count "unsafe" cases by different combinations


def count_unsafe_cases(data, has_style_persuasion=False):
    # Counters
    category_count = dict.fromkeys(categories, 0)
    persuasion_count = dict.fromkeys(available_techniques, 0)
    style_count = dict.fromkeys(available_styles, 0)
    persuasion_style_count = defaultdict(int, {(persuasion, style): 0 for persuasion in available_techniques for style in available_styles})
    category_style_count = defaultdict(int, {(category, style): 0 for category in categories for style in available_styles})
    category_persuasion_count = defaultdict(int, {(category, persuasion): 0 for category in categories for persuasion in available_techniques})
      
    for testcase in data:
    
        if "unsafe" in testcase.get("OutputSafetyLLM", []):
            # Base count by category
            category = testcase.get("category", "Unknown")
            category_count[category] += 1

            if has_style_persuasion:
                # Count by persuasion + style
                style = testcase.get("style", "Unknown")
                persuasion = testcase.get("persuasion_technique", "Unknown")
                persuasion_style_count[(persuasion, style)] += 1
                persuasion_count[persuasion] += 1
                style_count[style] += 1
                category_style_count[(category, style)] += 1
                category_persuasion_count[(category, persuasion)] += 1

                                                
    return category_count, persuasion_style_count, persuasion_count, style_count, category_style_count, category_persuasion_count 




def main():
    
    files=['ASTRAL_RAG_FS','ASTRAL_RAG_FS_TS']  # ASTRAL versions
    
    N_TESTS = 3
    
    for astral_file in files: 

          
        test_files = ['../../results/RQ12/results_gpt-3_5-turbo/'+astral_file+'.json',
                      '../../results/RQ12/results_gpt-4o/'+astral_file+'.json',
                      '../../results/RQ12/results_gpt-4-turbo/'+astral_file+'.json',
                      '../../results/RQ12/results_llama2_13b-chat/'+astral_file+'.json',
                      '../../results/RQ12/results_mistral/'+astral_file+'.json',
                      '../../results/RQ12/results_modifiedLlama3/'+astral_file+'.json',
                      '../../results/RQ12/results_vicuna_13b/'+astral_file+'.json']

        output_file = '../../results/RQ3/benchmark_results_'+astral_file+'.csv'
        style_output = '../../results/RQ3/unsafe_style_'+astral_file+'.csv'
        persuasion_output = '../../results/RQ3/unsafe_persuasion_'+astral_file+'.csv'
        category_output = '../../results/RQ3/unsafe_category_'+astral_file+'.csv'
        persuasionStyle_output = '../../results/RQ3/unsafe_persuasionStyle_'+astral_file+'.csv'
        categoryStyle_output = '../../results/RQ3/unsafe_categoryStyle_'+astral_file+'.csv'
        categoryPersuasion_output = '../../results/RQ3/unsafe_categoryPersuasion_'+astral_file+'.csv'

        test_file_counts = {}
        
        with open(output_file, mode='w', newline='') as file, open(style_output, mode='w', newline='') as style_file,  open(persuasion_output, mode='w', newline='') as persuasion_file,  open(category_output, mode='w', newline='') as category_file,  open(persuasionStyle_output, mode='w', newline='')  as categoryStyle_file, open(categoryStyle_output, mode='w', newline='') as categoryPersuasion_file, open(categoryPersuasion_output, mode='w', newline='') as persuasionStyle_file:
            writer = csv.writer(file, delimiter=';')
            style_writer = csv.writer(style_file, delimiter=';')
            persuasion_writer = csv.writer(persuasion_file, delimiter=';')
            category_writer = csv.writer(category_file, delimiter=';')
            persuasionStyle_writer = csv.writer(persuasionStyle_file, delimiter=';')
            categoryStyle_writer = csv.writer(categoryStyle_file, delimiter=';')
            categoryPersuasion_writer = csv.writer(categoryPersuasion_file, delimiter=';')
            
            # Write header
            #writer.writerow(["Model", "Category", "Style", "Persuasion", "Count", "nPrompts", "totalPrompts"]) #MODE 1
            writer.writerow(["Model", "Category", "Type", "Count", "nPrompts", "totalPrompts"]) 
            style_writer.writerow(["Model", "Category", "Type", "Count", "nPrompts", "totalPrompts"]) 
            persuasion_writer.writerow(["Model", "Category", "Type", "Count", "nPrompts", "totalPrompts"]) 
            category_writer.writerow(["Model", "Category", "Type", "Count", "nPrompts", "totalPrompts"]) 
            persuasionStyle_writer.writerow(["Model", "Category", "Type", "Count", "nPrompts", "totalPrompts"]) 
            categoryStyle_writer.writerow(["Model", "Category", "Type", "Count", "nPrompts", "totalPrompts"]) 
            categoryPersuasion_writer.writerow(["Model", "Category", "Type", "Count", "nPrompts", "totalPrompts"]) 
            
            
            for n in range(len(test_files)):
                
                
                test_data = load_json(test_files[n])
                
                category_count, persuasion_style_count, persuasion_count, style_count, category_style_count, category_persuasion_count = count_unsafe_cases(test_data, has_style_persuasion=True)      
               
                              
                model = re.search(r"results_[^/]+", test_files[n]).group(0)
                
                # Style counts
                for style, count in style_count.items():
                    writer.writerow([model, "", style, count, (14*5*3),1260])
                    style_writer.writerow([model, "", style, count, (14*5*3),1260])

                # Persuasion Technique counts
                for persuasion, count in persuasion_count.items():
                    writer.writerow([model, "", persuasion, count, (14*6*3),1260])
                    persuasion_writer.writerow([model, "", persuasion, count, (14*6*3),1260])

                # Style + Persuasion Technique counts
                for (persuasion, style), count in persuasion_style_count.items():
                    writer.writerow([model, "", f"{style} + {persuasion}", count, (14*3),1260])
                    persuasionStyle_writer.writerow([model, "", f"{style} + {persuasion}", count, (14*3),1260])

                # Category counts
                for category, count in category_count.items():
                    writer.writerow([model, category, "", count, (5*6*3),1260])
                    category_writer.writerow([model, category, "", count, (5*6*3),1260])
                    
                # Category Style counts
                for (category, style), count in category_style_count.items():                  
                    categoryStyle_writer.writerow([model, category, style, count, (14*5*3),1260])

                # Category Persuasion counts
                for (category, persuasion), count in category_persuasion_count.items():                  
                    categoryPersuasion_writer.writerow([model, category, persuasion, count, (14*6*3),1260])
        
        
    


if __name__ == "__main__":
    main()
