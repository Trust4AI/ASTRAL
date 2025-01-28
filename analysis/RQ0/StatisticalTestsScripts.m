clear;
clc;

%Add the path
restoredefaultpath;
addpath('Results/ACEngine');
addpath('../../');
numOfRepetitions = 50;
numOfStudies=4;
numOfFunctions=6;
global number;
number=numOfStudies*numOfFunctions;

%Get Data
[num, txt, raw] = xlsread('resultsExec_GANormal');
%[num, txt, raw] = xlsread('resultsExec_IOF_PlatEMO_nonSeeded');
cont = 1;
for i=1:number
    for j=1:numOfRepetitions
        resultsNonSeeded(j,i) =raw{cont+1,5};
        cont = cont +1;
    end
end

%Get Data Dynamic
[num, txt, raw] = xlsread('resultsExec_BalancedSeed');
%[num, txt, raw] = xlsread('resultsExec_IOF_PlatEMO_Balanced');
cont = 1;
for i=1:number
    for j=1:numOfRepetitions
        resultsDynamicSeed(j,i) =raw{cont+1,5};
        cont = cont +1;
    end
end

%Get Data Static 30
[num, txt, raw] = xlsread('resultsExec_30PercSeed');
%[num, txt, raw] = xlsread('resultsExec_IOF_PlatEMO_Size30');
cont = 1;
for i=1:number
    for j=1:numOfRepetitions
        results30perc(j,i) =raw{cont+1,5};
        cont = cont +1;
    end
end

%Get Data Static 70
[num, txt, raw] = xlsread('resultsExec_70PercSeed');
%[num, txt, raw] = xlsread('resultsExec_IOF_PlatEMO_Size70');
cont = 1;
for i=1:number
    for j=1:numOfRepetitions
        results70perc(j,i) =raw{cont+1,5};
        cont = cont +1;
    end
end

%Get Data Orthogonal
[num, txt, raw] = xlsread('resultsExec_Dissimilarity');
%[num, txt, raw] = xlsread('resultsExec_IOF_PlatEMO_Dissimilarity');
cont = 1;
for i=1:number
    for j=1:numOfRepetitions
        resultsARP(j,i) =raw{cont+1,5};
        cont = cont +1;
    end
end

%Get Data Orthogonal
[num, txt, raw] = xlsread('resultsExec_OrthogonalPopSeed');
%[num, txt, raw] = xlsread('resultsExec_IOF_PlatEMO_OrthogonalPop');
cont = 1;
for i=1:number
    for j=1:numOfRepetitions
        resultsOrthogonalPop(j,i) =raw{cont+1,5};
        cont = cont +1;
    end
end

%Get Data Dynamic+ARPG
[num, txt,raw]=xlsread('resultsExec_DissimilarityAndBalanced');
%[num, txt,raw]=xlsread('resultsExec_IOF_PlatEMO_DissimilarityAndBalanced');
cont=1;
for i=1:number
    for j=1:numOfRepetitions
        resultsDynamicAndARPG(j,i)=raw{cont+1,5};
        cont=cont+1;
    end
end
% Non seeded vs dynamic
% Results.perc30=zeros(24,1);
% Results.perc70=zeros(24,1);
% Resutls.Arpg=zeros(24,1);
% Results.Dynamic=zeros(24,1);
% Results.DynamicAndArpg=zeros(24,1);
% Results.Orthogonal=zeros(24,1);
% Results.NonSeeded=zeros(24,1);
Results=zeros(1,24)
for i=1:number
%     [~, pValue, ~] = swtest(results30perc(:,i));
%     Results.perc30(i,1)=pValue;
%     [~, pValue, ~] = swtest(results70perc(:,i));
%     Results.perc70(i,1)=pValue;
%     [~, pValue, ~] = swtest(resultsARP(:,i));
%     Resutls.Arpg(i,1)=pValue;
%     [~, pValue, ~] = swtest(resultsDynamicSeed(:,i));
%     Results.Dynamic(i,1)=pValue;
%     [~, pValue, ~] = swtest(resultsDynamicAndARPG(:,i));
%     Results.DynamicAndArpg(i,1)=pValue;
%     [~, pValue, ~] = swtest(resultsOrthogonalPop(:,i));
%     Results.Orthogonal(i,1)=pValue;
%     [~, pValue, ~] = swtest(resultsNonSeeded(:,i));
%     Results.NonSeeded(i,1)=pValue;

    x=[resultsNonSeeded(:,i),resultsDynamicSeed(:,i),results30perc(:,i),results70perc(:,i),resultsARP(:,i),resultsOrthogonalPop(:,i),resultsDynamicAndARPG(:,i)];
    [p,tbl,stats] = kruskalwallis(x,[],'off');
    c = multcompare(stats);
    Results(i,1)=p;
%     Results(:,1)=c(:,1);
%     Results(:,2)=c(:,2);
%     Results(:,i+2)=c(:,6);
end
% result= struct2table(Results);
% writetable(result, 'Hypervolume_kruskalwallis.xlsx', 'Sheet','IOF');
writematrix(Results, 'Hypervolume_kruskalwallis2.xlsx', 'Sheet','ACEngine');
% Initialize Data structure


% Initialize Data structure
StatisticalResults.AbtterB = zeros(21,1);
StatisticalResults.AworseB = zeros(21,1);
StatisticalResults.AequalB = zeros(21,1);
StatisticalResults.A_PlusPlus = zeros(21,1);
StatisticalResults.A_Plus = zeros(21,1);
StatisticalResults.A_Value = zeros(21,1);
StatisticalResults.B_PlusPlus = zeros(21,1);
StatisticalResults.B_Plus = zeros(21,1);
StatisticalResults.B_Value = zeros(21,1);
StatisticalResults.A12Values = zeros(21,number);
StatisticalResults.pValues = zeros(21,number);

for j=1:number
    x=cat(2,resultsNonSeeded(:,j).',resultsDynamicSeed(:,j).',results30perc(:,j).',results70perc(:,j).',resultsARP(:,j).',resultsOrthogonalPop(:,j).',resultsDynamicAndARPG(:,j).');
    g=[ones(1,numOfRepetitions) repmat(2,1,numOfRepetitions) repmat(3,1,numOfRepetitions) repmat(4,1,numOfRepetitions) repmat(5,1,numOfRepetitions) repmat(6,1,numOfRepetitions) repmat(7,1,numOfRepetitions)];

    ret=holm(x,g);
    ret=sortrows(ret,1);
    for i=1:size(ret,1)
%         if strcmp(char(table2cell(ret(i,4))),'Reject H0')
            switch i
                case 1
                    A = resultsNonSeeded(:,j);
                    B = resultsDynamicSeed(:,j);
                case 2
                    A = resultsNonSeeded(:,j);
                    B = results30perc(:,j);
                case 3
                    A = resultsNonSeeded(:,j);
                    B = results70perc(:,j);
                case 4
                    A = resultsNonSeeded(:,j);
                    B = resultsARP(:,j);
                case 5
                    A = resultsNonSeeded(:,j);
                    B = resultsOrthogonalPop(:,j);
                case 6
                    A = resultsNonSeeded(:,j);
                    B = resultsDynamicAndARPG(:,j);
                case 7
                    A = resultsDynamicSeed(:,j);
                    B = results30perc(:,j);
                case 8
                    A = resultsDynamicSeed(:,j);
                    B = results70perc(:,j);
                case 9
                    A = resultsDynamicSeed(:,j);
                    B = resultsARP(:,j);
                case 10
                    A = resultsDynamicSeed(:,j);
                    B = resultsOrthogonalPop(:,j);
                case 11
                    A = resultsDynamicSeed(:,j);
                    B = resultsDynamicAndARPG(:,j);
                case 12
                    A = results30perc(:,j);
                    B = results70perc(:,j);
                case 13
                    A = results30perc(:,j);
                    B = resultsARP(:,j);
                case 14
                    A = results30perc(:,j);
                    B = resultsOrthogonalPop(:,j);
                case 15
                    A = results30perc(:,j);
                    B = resultsDynamicAndARPG(:,j);
                case 16
                    A = results70perc(:,j);
                    B = resultsARP(:,j);
                case 17
                    A = results70perc(:,j);
                    B = resultsOrthogonalPop(:,j);
                case 18
                    A = results70perc(:,j);
                    B = resultsDynamicAndARPG(:,j);
                case 19
                    A = resultsARP(:,j);
                    B = resultsOrthogonalPop(:,j);
                case 20
                    A = resultsARP(:,j);
                    B = resultsDynamicAndARPG(:,j);
                case 21
                    A = resultsOrthogonalPop(:,j);
                    B = resultsDynamicAndARPG(:,j);
                otherwise
            end
            [AbtterB, AworseB, AequalB, A12Values, A_Value,B_Value, A_Plus, B_Plus, A_PlusPlus, B_PlusPlus] = obtainStatistics(A,B);

            StatisticalResults.AbtterB(i,1) = StatisticalResults.AbtterB(i,1)+AbtterB;
            StatisticalResults.AworseB(i,1) = StatisticalResults.AworseB(i,1)+AworseB;
            StatisticalResults.AequalB(i,1) = StatisticalResults.AequalB(i,1)+AequalB;
            StatisticalResults.A_PlusPlus(i,1) = StatisticalResults.A_PlusPlus(i,1)+A_PlusPlus;
            StatisticalResults.A_Plus(i,1) = StatisticalResults.A_Plus(i,1)+A_Plus;
            StatisticalResults.A_Value(i,1) = StatisticalResults.A_Value(i,1)+A_Value;
            StatisticalResults.B_PlusPlus(i,1) = StatisticalResults.B_PlusPlus(i,1)+B_PlusPlus;
            StatisticalResults.B_Plus(i,1) = StatisticalResults.B_Plus(i,1)+B_Plus;
            StatisticalResults.B_Value(i,1) =  StatisticalResults.B_Value(i,1)+B_Value;
            StatisticalResults.A12Values(i,j) = A12Values;
            StatisticalResults.pValues(i,j) = cell2mat(table2cell(ret(i,2)));
%         else
%             StatisticalResults.AbtterB(i,1) =StatisticalResults.AbtterB(i,1)+0;
%             StatisticalResults.AworseB(i,1) = StatisticalResults.AworseB(i,1)+0;
%             StatisticalResults.AequalB(i,1) =  StatisticalResults.AequalB(i,1)+1;
%             StatisticalResults.A_PlusPlus(i,1) = StatisticalResults.A_PlusPlus(i,1)+0;
%             StatisticalResults.A_Plus(i,1) = StatisticalResults.A_Plus(i,1)+0;
%             StatisticalResults.A_Value(i,1) = StatisticalResults.A_Value(i,1)+0;
%             StatisticalResults.B_PlusPlus(i,1) =  StatisticalResults.B_PlusPlus(i,1)+0;
%             StatisticalResults.B_Plus(i,1) = StatisticalResults.B_Plus(i,1)+0;
%             StatisticalResults.B_Value(i,1) = StatisticalResults.B_Value(i,1)+0;
%             StatisticalResults.A12Values(i,j) = 0;
%             StatisticalResults.pValues(i,j) = cell2mat(table2cell(ret(i,2)));
%         end


    end
end

result= struct2table(StatisticalResults);
writetable(result, 'resultsIOF_HV2_A.xlsx');
function [AbtterB, AworseB, AequalB, A12Values, A_Value,B_Value, A_Plus, B_Plus, A_PlusPlus, B_PlusPlus] = obtainStatistics(A, B)
    AbtterB = 0;
    AworseB = 0;
    AequalB = 0;
    A_Value=0;
    B_Value=0;
    A_Plus=0;
    A_PlusPlus=0;
    B_Plus=0;
    B_PlusPlus=0;
        
    A12 = Atest(A(:),B(:));

    A12Values=A12;
    if A12<0.5
        d=2*abs(A12-0.5);
        if d<0.147
            AequalB=AequalB+1;
        elseif d<0.33 
            AworseB = AworseB+1;
            B_Value=B_Value+1;
        elseif d<0.474
            AworseB = AworseB+1;
            B_Plus=B_Plus+1;
        elseif d>=0.474
            AworseB = AworseB+1;
            B_PlusPlus=B_PlusPlus+1;
        end
    elseif A12>0.5
        
        A12=A12-0.5;
        d=2*abs(A12-0.5);
        if d<0.147
            AequalB=AequalB+1;
        elseif d<0.33
            A_Value=A_Value+1;
            AbtterB = AbtterB+1;
        elseif d<0.474
            A_Plus=A_Plus+1;
            AbtterB = AbtterB+1;
        elseif d>=0.474
            A_PlusPlus=A_PlusPlus+1;
            AbtterB = AbtterB+1;
        end
    end
    
    
    
end
