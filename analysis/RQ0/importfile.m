function analyzedresultsgpt4turbo = importfile(filename, dataLines)
%IMPORTFILE Import data from a text file
%  ANALYZEDRESULTSGPT4TURBO = IMPORTFILE(FILENAME) reads data from text
%  file FILENAME for the default selection.  Returns the data as a table.
%
%  ANALYZEDRESULTSGPT4TURBO = IMPORTFILE(FILE, DATALINES) reads data for
%  the specified row interval(s) of text file FILENAME. Specify
%  DATALINES as a positive scalar integer or a N-by-2 array of positive
%  scalar integers for dis-contiguous row intervals.
%
%  Example:
%  analyzedresultsgpt4turbo = importfile("C:\Users\pvalle\Desktop\Trust4AI\TRUST4AI_MU\trust4ai-safety-module\results\RQ1\analyzed_results_gpt_4_turbo.csv", [2, Inf]);
%
%  See also READTABLE.
%
% Auto-generated by MATLAB on 09-May-2024 08:27:12

%% Input handling

% If dataLines is not specified, define defaults
if nargin < 2
    dataLines = [2, 21];
end

%% Set up the Import Options and import the data
opts = delimitedTextImportOptions("NumVariables", 8);

% Specify range and delimiter
opts.DataLines = dataLines;
opts.Delimiter = ",";

% Specify column names and types
opts.VariableNames = ["TP", "TN", "FP", "FN", "NR", "Accuracy", "Recall", "Precission"];
opts.VariableTypes = ["double", "double", "double", "double", "double", "double", "double", "double"];

% Specify file level properties
opts.ExtraColumnsRule = "ignore";
opts.EmptyLineRule = "read";

% Import the data
analyzedresultsgpt4turbo = readtable(filename, opts);

end