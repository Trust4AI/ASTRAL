clc; clear; close all;

addpath("..\..\results\RQ0\");
evaluatedModelsLabel=["GPT4","GPT3","mistral","Llama2","Llama3","ChatQA","Llamaguard"];
evaluatedMetrics=["Accurcay","Precission","Recall"];
%% Get the data from the excel files
gpt4_data=importfile("results\RQ0\analyzed_results_gpt_4_turbo.csv");
gpt3_data=importfile("results\RQ0\analyzed_results_gpt_3.5_turbo.csv");
mistral_data=importfile("results\RQ0\analyzed_results_mistral.csv");
llama2_data=importfile("results\RQ0\analyzed_results_llama2_13b_chat.csv");
llama3_data=importfile("results\RQ0\analyzed_results_modifiedllama3.csv");
chatQA_data=importfile("results\RQ0\analyzed_results_llama3_chatqa.csv");
llamaguard_data=importfile("results\RQ0\analyzed_results_llamaguard_latest.csv");
numOfRepetitions=20;

evaluatedModels={gpt4_data,gpt3_data,mistral_data,llama2_data,llama3_data,chatQA_data,llamaguard_data};

%% Comparision of guided vs unguided for the archives

for k=1:size(evaluatedMetrics,2)
    switch k
        case 1
           x=cat(2,gpt4_data.Accuracy',gpt3_data.Accuracy',mistral_data.Accuracy',llama2_data.Accuracy',llama3_data.Accuracy',chatQA_data.Accuracy',llamaguard_data.Accuracy');
        case 2
           x=cat(2,gpt4_data.Precission',gpt3_data.Precission',mistral_data.Precission',llama2_data.Precission',llama3_data.Precission',chatQA_data.Precission',llamaguard_data.Precission');

        case 3
           x=cat(2,gpt4_data.Recall',gpt3_data.Recall',mistral_data.Recall',llama2_data.Recall',llama3_data.Recall',chatQA_data.Recall',llamaguard_data.Recall');
    end
    g=[ones(1,numOfRepetitions) repmat(2,1,numOfRepetitions) repmat(3,1,numOfRepetitions) repmat(4,1,numOfRepetitions) repmat(5,1,numOfRepetitions) repmat(6,1,numOfRepetitions) repmat(7,1,numOfRepetitions)];
    ret=holm(x,g);
    ret=sortrows(ret,1);
    cont=0;
    for i=1:size(evaluatedModels,2)-1
        A=evaluatedModels{i};
        for j=i+1:size(evaluatedModels,2)
            cont=cont+1;
            B=evaluatedModels{j};
            %disp(strcat("The evaluation is ",A," against ",B));
            switch k
                case 1
                    to_evaluateA=A.Accuracy;
                    to_evaluateB=B.Accuracy;
    
                case 2
                    to_evaluateA=A.Precission;
                    to_evaluateB=B.Precission;
    
                case 3
                    to_evaluateA=A.Recall;
                    to_evaluateB=B.Recall;
            end
            A12 = Atest(to_evaluateA(:),to_evaluateB(:));
            if ret.p_value(cont)<0.0001

                p="<0.0001";
            else
                p=ret.p_value(cont);
            end
            StatisticalResults(cont,1)=evaluatedModelsLabel(i);
            StatisticalResults(cont,2)=evaluatedModelsLabel(j);
            StatisticalResults(cont,2+k*2-1)=p;
            StatisticalResults(cont,2+k*2)=A12;
        end
        

    end
end

colnames=["Model A", "Model B", "Accuracy_p", "Accuracy_A12", "Precission_p", "Precission_A12","Recall_p", "Recall_A12"];
resultTable=array2table(StatisticalResults);
resultTable.Properties.VariableNames=colnames;
writetable(resultTable,"..\..\results\RQ0\evaluation.xlsx");


