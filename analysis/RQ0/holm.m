function ret = holm(x,g,varargin)
%Holm-Sidak procedure for multiple Student's t tests.
%This file is applicable for equal or unequal sample sizes
%
% Syntax: 	HOLM(X,GROUP,CTRL,ALPHA,TAIL)
%      
%     Inputs:
%           X: data vector
%           GROUP - specifies grouping variables G. Grouping variables must
%           have one column per element of X.
%           CTRL: The first sample is a control group (1); there is not a
%           control group (0). (default=0).
%           ALPHA: significance level (default = 0.05).
%           TAIL: 2 (2-tailed, default);
%                -1 (left tailed)
%                 1 (right tailed)
%     Outputs:
%           - Mean and Standard Deviation vectors.
%           - degrees of freedom and combined variance.
%           - p-value for each comparison.
%           - alpha value corrected by Sidak procedure.
%           - whether or not Ho is rejected.
%
%      Example: 
%
%                                 Sample
%                   ---------------------------------
%                       1       2       3       4
%                   ---------------------------------
%                      7.68    7.71    7.74    7.71
%                      7.69    7.73    7.75    7.71
%                      7.70    7.74    7.77    7.74
%                      7.70    7.74    7.78    7.79
%                      7.72    7.78    7.80    7.81
%                      7.73    7.78    7.81    7.85
%                      7.73    7.80    7.84    7.87
%                      7.76    7.81            7.91
%                   ---------------------------------
%                                       
%       Data matrix must be:
%    x=[7.68 7.69 7.70 7.70 7.72 7.73 7.73 7.76 7.71 7.73 7.74 7.74 7.78 ...
%    7.78 7.80 7.81 7.74 7.75 7.77 7.78 7.80 7.81 7.84 7.71 7.71 7.74 7.79...
%    7.81 7.85 7.87 7.91];
%    g=[ones(1,8) repmat(2,1,8) repmat(3,1,7) repmat(4,1,8)];
%
%           Calling on Matlab the function: holm(x,g) (there is not a control group)
%
%           Answer is:
%
%     Group    N     Mean     Standard_deviation
%     _____    _    ______    __________________
% 
%     1        8    7.7138    0.026152          
%     2        8    7.7613    0.036031          
%     3        7    7.7843    0.035051          
%     4        8    7.7988    0.075107          
% 
% Degrees of freedom: 27 - Combined variance: 0.0022
%  
%     Comparison     p_value         Sidak_alpha               Comment      
%     __________    _________    ____________________    ___________________
% 
%     '1-4'          0.001314    [            0.0085]    'Reject H0'        
%     '1-3'         0.0078145    [            0.0102]    'Reject H0'        
%     '1-2'          0.055306    [            0.0127]    'Fail to reject H0'
%     '2-4'           0.12544    'No comparison made'    'H0 is accepted'   
%     '2-3'           0.35633    'No comparison made'    'H0 is accepted'   
%     '3-4'           0.56058    'No comparison made'    'H0 is accepted'   
%
%           Calling on Matlab the function: holm(x,g,1) (sample 1 is the control group)
%
%           Answer is:
%
%     Group    N     Mean     Standard_deviation
%     _____    _    ______    __________________
% 
%     1        8    7.7138    0.026152          
%     2        8    7.7613    0.036031          
%     3        7    7.7843    0.035051          
%     4        8    7.7988    0.075107          
% 
% Degrees of freedom: 27 - Combined variance: 0.0022
%  
%     Comparison     p_value     Sidak_alpha          Comment      
%     __________    _________    ___________    ___________________
% 
%     '1-4'          0.001314    0.016952       'Reject H0'        
%     '1-3'         0.0078145    0.025321       'Reject H0'        
%     '1-2'          0.055306        0.05       'Fail to reject H0'
%
%
%           Created by Giuseppe Cardillo
%           giuseppe.cardillo-edta@poste.it
%
% To cite this file, this would be an appropriate format:
% Cardillo G. (2006). Holm-Sidak t-test: a routine for multiple t-test comparisons.
% http://www.mathworks.com/matlabcentral/fileexchange/12786


%Input Error handling
p=inputParser;
addRequired(p,'x',@(x) validateattributes(x,{'numeric'},{'row','real','finite','nonnan','nonempty'}));
addRequired(p,'g',@(x) validateattributes(x,{'numeric'},{'row','real','finite','integer','nonnan','nonempty'}));
addOptional(p,'ctrl',0, @(x) isnumeric(x) && isreal(x) && isfinite(x) && isscalar(x) && (x==0 || x==1));
addOptional(p,'alpha',0.05, @(x) validateattributes(x,{'numeric'},{'scalar','real','finite','nonnan','>',0,'<',1}));
addOptional(p,'tail',2, @(x) isnumeric(x) && isreal(x) && isfinite(x) && isscalar(x) && (x==-1 || x==1 || x==2));
parse(p,x,g,varargin{:});
assert(length(x)==length(g),'Warning: X and G must have the same length')
ctrl=p.Results.ctrl; alpha=p.Results.alpha; tail=p.Results.tail;
clear p

k=max(g); %groups
I = [find(g(1:end-1) ~= g(2:end)) length(g)];
N = diff([ 0 I ]); %elements of each group
Idx=g(I);
n=sum(N); %total elements
Md=ones(1,k); %Means vector preallocation
Sd=ones(1,k); %Standard deviations vector preallocation
% Calculate mean and standard deviation of each group
for I=1:k
    Md(I)=mean(x(g==I));
    Sd(I)=std(x(g==I));
end
disp(array2table([Idx' N' Md' Sd'],'VariableNames',{'Group','N','Mean','Standard_deviation'}))


df=n-k; %degrees of freedom
s2=sum((N-1).*Sd.^2)/df; %combined variance

clear n Sd %clear unnecessary variables

fprintf('Degrees of freedom: %d - Combined variance: %0.4f\n',df,s2)
disp(' ')

%if there is not a control group, the max number of comparisons are
%k*(k-1)/2; otherwise there it is k-1.
switch ctrl
    case 0 %without a control group
        a=k-1; %rows of probability matrix
        c=0.5*k*(k-1); %max number of comparisons
     case 1
        a=1; %row of probability matrix
        c=k-1; %max number of comparisons
end

count=0; %counter
%preallocation of p-value vectors
p=ones(1,c); pb{c,4} = []; 
for I=1:a
    for J=I+1:k
        count=count+1;
        t=diff(Md([I J]))/realsqrt(s2*sum(1./N([I J]))); %t-value
        switch tail
            case -1
                p(count)=tcdf(t,df); %2-tailed p-value vector
            case 1
                p(count)=tcdf(-t,df); %2-tailed p-value vector
            case 2
                p(count)=2*tcdf(-abs(t),df); %2-tailed p-value vector
        end
        pb(count,1:2)={strcat(int2str(I),'-',int2str(J));p(count)}; %vectors of comparisons
    end
end
clear df Md N s2 a k t count i j %clear unnecessary variables

[p,I]=sort(p); %sorted p-value vector
pb=pb(I,:);
J=1:c; %How many corrected alpha value?
alphacorr=1-((1-alpha).^(1./(c-J+1))); %Sidak alpha corrected values

%Compare the p-values with alpha corrected values. 
%If p<a reject Ho; else don't reject Ho: no more comparison are required.
comp=1; %compare checker
for J=1:c
    if comp %Comparison is required
        if p(J)<alphacorr(J)
            pb(J,3:4)={alphacorr(J);'Reject H0'};
        else
            pb(J,3:4)={alphacorr(J);'Fail to reject H0'};
            comp=0; %no more comparison are required
        end
    else %comparison is unnecessary
        pb(J,3:4)={'No comparison made';'H0 is accepted'};
    end
end
disp(cell2table(pb,'VariableNames',{'Comparison','p_value','Sidak_alpha','Comment'}))
ret=cell2table(pb,'VariableNames',{'Comparison','p_value','Sidak_alpha','Comment'});
end