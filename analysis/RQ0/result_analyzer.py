import pandas as pd
import csv
import numpy as np
import os
# Open the CSV file in append mode

NUM_OF_RUNS=20


EVALUATORS=["gpt_4o", "gpt_4_turbo","gpt_3.5_turbo","mistral","llama2_13b_chat","modifiedllama3","llama3_chatqa","llamaguard_latest"];

path="../../results/RQ0/"

for evaluator in EVALUATORS:

    results=pd.DataFrame({"TP":[],"TN":[],"FP":[],"FN":[],"NR":[],"Accuracy":[],"Recall":[],"Precission":[]})
    for i in range(0,NUM_OF_RUNS):
        data=pd.read_csv(path+"test_evaluation_results_"+evaluator+"_run_"+str(i)+".csv")
        tp=data["Value"][0]
        tn=data["Value"][1]
        fp=data["Value"][2]
        fn=data["Value"][3]
        nr=data["Value"][4]
        accuracy=(tp+tn)/(tp+tn+fp+fn+nr)
        recall=tp/(tp+fp)
        precission=tp/(tp+fn)
        results=pd.concat([results, pd.DataFrame([{"TP":tp,"TN":tn,"FP":fp,"FN":fn, "NR":nr, "Accuracy":accuracy,"Recall":recall,"Precission":precission}])], ignore_index=True)

    results.to_csv(path+"analyzed_results_"+evaluator+".csv", index=False)

    with open(path+"analyzed_results_"+evaluator+".csv", 'a', newline='') as csvfile:
        # Create a CSV writer object
        csv_writer = csv.writer(csvfile)
        
        # Add a line to the CSV file
        line_to_add = [np.mean(results['TP']),np.mean(results['TN']),np.mean(results['FP']),np.mean(results['FN']),np.mean(results['NR']),np.mean(results['Accuracy']),np.mean(results['Recall']),np.mean(results['Precission'])]  # Replace with your data
        csv_writer.writerow(line_to_add)

    with open(path+"analyzed_results_RQ1.csv", 'a',newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        
        # Add a line to the CSV file
        line_to_add = [evaluator,np.mean(results['TP']),np.std(results['TP']),np.mean(results['TN']),np.std(results['TN']),np.mean(results['FP']),np.std(results['FP']),np.mean(results['FN']),np.std(results['FN']),np.mean(results['NR']),np.std(results['NR'])]  # Replace with your data
        csv_writer.writerow(line_to_add)