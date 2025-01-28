# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 14:45:21 2024

@author: mugarte
"""
import csv
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

category_to_style = {
    "slang": "S1",
    "uncommon_dialects": "S2",
    "technical_terms": "S3",
    "role_play": "S4",
    "misspellings": "S5",
    "question": "S6",
}


category_to_persuasion = {
    "evidence-based_persuasion": "P1",
    "expert_endorsement": "P2",
    "misrepresentation": "P3",
    "authority_endorsement": "P4",
    "logical_appeal": "P5",
}

category_category_to_key = {
    "animal_abuse": "C1",
    "child_abuse": "C2",
    "controversial_topics,politics": "C3",
    "discrimination,stereotype,injustice": "C4",
    "drug_abuse,weapons,banned_substance": "C5",
    "financial_crime,property_crime,theft": "C6",
    "hate_speech,offensive_language": "C7",
    "misinformation_regarding_ethics,laws_and_safety": "C8",
    "non_violent_unethical_behavior": "C9",
    "privacy_violation": "C10",
    "self_harm": "C11",
    "sexually_explicit,adult_content": "C12",
    "terrorism,organized_crime": "C13",
    "violence,aiding_and_abetting,incitement": "C14",
}

category_to_stylePersuasion_key = {
    "slang + evidence-based_persuasion": ("S1", "P1"),
    "uncommon_dialects + evidence-based_persuasion": ("S2", "P1"),
    "technical_terms + evidence-based_persuasion": ("S3", "P1"),
    "role_play + evidence-based_persuasion": ("S4", "P1"),
    "misspellings + evidence-based_persuasion": ("S5", "P1"),
    "question + evidence-based_persuasion": ("S6", "P1"),
    
    "slang + expert_endorsement": ("S1", "P2"),
    "uncommon_dialects + expert_endorsement": ("S2", "P2"),
    "technical_terms + expert_endorsement": ("S3", "P2"),
    "role_play + expert_endorsement": ("S4", "P2"),
    "misspellings + expert_endorsement": ("S5", "P2"),
    "question + expert_endorsement": ("S6", "P2"),
    
    "slang + misrepresentation": ("S1", "P3"),
    "uncommon_dialects + misrepresentation": ("S2", "P3"),
    "technical_terms + misrepresentation": ("S3", "P3"),
    "role_play + misrepresentation": ("S4", "P3"),
    "misspellings + misrepresentation": ("S5", "P3"),
    "question + misrepresentation": ("S6", "P3"),
    
    "slang + authority_endorsement": ("S1", "P4"),
    "uncommon_dialects + authority_endorsement": ("S2", "P4"),
    "technical_terms + authority_endorsement": ("S3", "P4"),
    "role_play + authority_endorsement": ("S4", "P4"),
    "misspellings + authority_endorsement": ("S5", "P4"),
    "question + authority_endorsement": ("S6", "P4"),
    
    "slang + logical_appeal": ("S1", "P5"),
    "uncommon_dialects + logical_appeal": ("S2", "P5"),
    "technical_terms + logical_appeal": ("S3", "P5"),
    "role_play + logical_appeal": ("S4", "P5"),
    "misspellings + logical_appeal": ("S5", "P5"),
    "question + logical_appeal": ("S6", "P5"),
}


# Define the order of models for each style
model_order = [
    "results_gpt-4-turbo",     # GPT4
    "results_gpt-4o",          # GPT4o
    "results_gpt-3_5-turbo",   # GPT3.5
    "results_mistral",         # Mistral
    "results_llama2_13b-chat", # Llama2
    "results_modifiedLlama3", # Llama3
    "results_vicuna_13b"       # Vicuna
]


astral_versions=["ASTRAL_RAG_FS","ASTRAL_RAG_FS_TS"]  #change to "ASTRAL_RAF_FS_TS" for Tavily Search heatmap

for astral in astral_versions:

    style_file = '../../results/RQ3/unsafe_style_'+astral+'.csv'
    persuasion_file = '../../results/RQ3/unsafe_persuasion_'+astral+'.csv'
    category_file = '../../results/RQ3/unsafe_category_'+astral+'.csv'
    stylePersuasion_file= '../../results/RQ3/unsafe_persuasionStyle_'+astral+'.csv'

    # Initialize a dictionary to store the aggregated data
    data = {
        "Style": {key: [0] * len(model_order) for key in category_to_style.values()},
        "Persuasion": {key: [0] * len(model_order) for key in category_to_persuasion.values()},
        "Category": {key: [0] * len(model_order) for key in category_category_to_key.values()}
    }

    data1 = {style: {persuasion: [0] * len(model_order) for persuasion in category_to_persuasion.values()} for style in category_to_style.values()}


    # Function to process a CSV file and populate the data
    def process_csv(file_path, cat, category_mapping, target_key):
        with open(file_path, 'r', encoding='utf-8-sig') as file:
            csv_reader = csv.DictReader(file, delimiter=';')
            for row in csv_reader:
                model = row['Model']
                category = row[cat]
                count = int(row['Count'])

                # Map the category to the corresponding key
                key = category_mapping.get(category)
                if key:
                    # Find the index of the model in the specified order
                    if model in model_order:
                        model_index = model_order.index(model)
                        # Update the count in the appropriate key and model position
                        data[target_key][key][model_index] = count
                        

    # Process both CSV files
    process_csv(style_file, "Type", category_to_style, "Style")
    process_csv(persuasion_file, "Type", category_to_persuasion, "Persuasion")
    process_csv(category_file, "Category", category_category_to_key, "Category")


    # Convert data into one DataFrame
    all_data = pd.concat([pd.DataFrame(data["Style"]), pd.DataFrame(data["Persuasion"]), pd.DataFrame(data["Category"])], axis=1)
    all_data.index = ["GTP 4", "GTP 4o", "GTP 3.5", "Mistral", "Llama 2", "Llama 3", "Vicuna"]

    # Plotting the single heatmap
    # Plotting the heatmap
    plt.figure(figsize=(20, 3))
    ax= sns.heatmap(all_data, annot=True, fmt="d", cmap="YlGnBu", cbar_kws={'label': 'Number of Unsafe Results'},  linewidths=1)

    # Add dotted vertical lines to separate Style, Persuasion, and Category groups
    plt.axvline(x=6, color='black', linestyle=':', linewidth=2)  # After Style columns
    plt.axvline(x=11, color='black', linestyle=':', linewidth=2)  # After Persuasion column

    # Add labels at the bottom for Style, Persuasion, and Category
    ax.text(3, len(all_data) + 1.5, "Style", ha='center', va='center', fontsize=10, fontweight='bold')
    ax.text(8.5, len(all_data) + 1.5, "Persuasion", ha='center', va='center', fontsize=10, fontweight='bold')
    ax.text(18, len(all_data) + 1.5, "Category", ha='center', va='center', fontsize=10, fontweight='bold')
    plt.yticks(rotation=0)
    # Adding labels and title
    plt.title("Number of Unsafe Results by Feature Across Models", fontsize=13, fontweight='bold')
    #plt.xlabel("Features (Style, Persuasion, Category)")
    plt.ylabel("Execution Models", fontsize=10, fontweight='bold')
    plt.tight_layout()
    plt.show()




