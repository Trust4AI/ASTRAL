function A = Atest(X, Y)
% Given a column vector, ie, data stored in the rows of a matrix rather than the columns, this function will calculate 
% the A score between samples represented by X and Y. 
% Note that this test is only valid if samples X and Y are of the same size. 
%
    [p,h,st] = ranksum(X,Y,'alpha',0.05);                       % calculate the rank sum.
    N = size(X,1);                                              % store how many samples there are in each distribution.
    M = size(Y,1);
    A = (st.ranksum/N - (N+1)/2)/M;                             % calculate A test score. 
end