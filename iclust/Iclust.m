%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% Iclust.m
%
% Iclust_1.0 - Information based clustering, Version 1.0
% Copyright (C) Dec. 2004 Noam Slonim, Gurinder S. Atwal, Gasper Tkacik, and William Bialek
%
%    This program is free software; you can redistribute it and/or modify
%    it under the terms of the GNU General Public License as published by
%    the Free Software Foundation; either version 2 of the License, or
%    (at your option) any later version.
%
%    This program is distributed in the hope that it will be useful,
%    but WITHOUT ANY WARRANTY; without even the implied warranty of
%    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
%    GNU General Public License for more details.
%
%    You should have received a copy of the GNU General Public License
%    along with this program; if not, write to the Free Software
%    Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%%%%%%%%%%%%%%%%
% Introduction %
%%%%%%%%%%%%%%%%
%
% Iclust is an iterative clustering algorithm which finds a (perhaps local) maximum to the cost
% function:
%
%   F = \sum_{c,i1,i2} q(c)q(i1|c)q(i2|c)S(i1,i2) - T I(C;i) ,
%
% where S(i1,i2) is an input similarity matrix, T is a (temperature)
% tradeoff parameter, and I(C;i) is the ("compression") information between
% the cluster variable, C, and the data variable, i.
%
%%%%%%%%%
% INPUT %
%%%%%%%%%
%
% S: S(i1,i2) is the similarity between i1 and i2. In the paper we measure
% this through the information that i1 and i2 share about each other. HOWEVER, the algorithm
% can work with ANY similarity matrix as an input. NOTICE, that the
% diagonal values should be maximal. 
% The code can easily be turned to handle distortion relations as input. 
%
% T: A tradeoff parameter. Default is 1/30 but we strongly recommend to
% explore other values as well. SMALLER T values yield more deterministic
% clustering solutions. 
%
% Csize: Requested number of clusters. Default is sqrt of the number of
% data items. Again, we strongly recommend to explore different values
% here.
%
% InitNum: Determines how many local maxima will be extracted, from which
% only the best one is returned. Default is 10.
%
%%%%%%%%%%%%%%%%%%%%%%%%%
% Command line examples %
%%%%%%%%%%%%%%%%%%%%%%%%%
%
% (1) [C,prm] = Iclust (S,[],[],[]); % use default values for T, Nc, and InitNum.
% (2) [C,prm] = Iclust (S,1/25,5,10);; % Specify T, Nc, and InitNum through input.
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%%%%%%%%%%
% OUTPUT %
%%%%%%%%%%
%
% C: C{InitInd} records the results for the InitInd run.
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function [C,prm] = Iclust (S,T,Nc,InitNum)

[C,prm] = InitParameters (S,T,Nc,InitNum);
for InitInd = 1:prm.InitNum  
    fprintf ('Iclust run number %d...\n',InitInd);  
    [tmpC] = Iclust_InitC (S,prm);
    [tmpC] = Iclust_SingleRun (S,tmpC,prm);  
    if tmpC.F_end > C.F_end
        C = tmpC;
    end
end  

return
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


function [C,prm] = InitParameters (S,T,Nc,InitNum)

% Check input similarity matrix
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if size(S,1)~=size(S,2)
    error ('D must be a squared matrix')
end

if min(min(S))<0
    fprintf ('The SIMILARITY matrix includes NEGATIVE values -- do you wish to continue? (press any key)\n');
    pause
end

if any(S-S')
    fprintf ('NON SYMMETRIC similarity matrix -- abort\n');
    fprintf ('Note that the code can be easily turned to handle non-symmetric input matrices as well\n');
    error ('S is not symmetric');
end

maxS = max(S);
diagS = diag(S)';
if any(find(maxS > diagS))
    fprintf ('DIAGONAL values are not MAXIMAL in S - do you wish to continue? (press any key)\n');    
    pause
    warning ('Non maximal diagonal values can lead to unreliable output!')
end

% Set parameters
%%%%%%%%%%%%%%%%%%
prm.N = size(S,1);
if isempty (T)
    T = 1/30; %default
end
if isempty (Nc)
    Nc = floor(sqrt(size(S,1))); % default
end
if isempty (InitNum)
    InitNum = 10; % default
end
prm.T = T;
prm.Nc = Nc;
prm.InitNum = InitNum;

% More default parameters
%%%%%%%%%%%%%%%%%%%%%%%%%
prm.Pi = ones(1,prm.N)./prm.N; % Assume uniform prior over X, for convenience -- this can be easily changed if necessary
prm.HardInit = 0;
prm.LoopLimit = 200;
prm.LocalEps = 1e-10;
prm.SmallChange = prm.LocalEps;
prm.RunStart = datestr(now);
prm.RunSeed = 0; % use 'sum(100*clock)' for "random" seed
rand('state',prm.RunSeed);

C.F_end = -inf;

return
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function [tmpC] = Iclust_InitC (S,prm)

tmpC.T = prm.T;
tmpC.Qc_i = zeros(prm.N,prm.Nc); % P(c|i), Each ROW should sum to 1
tmpC.Qc = zeros(1,prm.Nc); % Q(c)

if prm.HardInit  % Initialize by a random "HARD" partition into (more or less) equal-sized clusters
    perm = randperm(prm.N);  
    AvgSize = ceil(prm.N/prm.Nc);  
    for c=1:prm.Nc
        i1 = (c-1)*AvgSize+1;
        i2 = min(c*AvgSize,prm.N);
        inds = perm(i1:i2);
        tmpSizes(c) = length(inds);
        tmpC.Qc_i(inds,c) = 1;
        tmpC.Qc(c) = tmpSizes(c)/prm.N;
    end
else             % Initialize by a random "SOFT" partition into (more or less) equal-sized clusters
    tmpC.Qc_i = rand(prm.N,prm.Nc);
    for i=1:prm.N
        tmpC.Qc_i(i,:) = tmpC.Qc_i(i,:)./sum(tmpC.Qc_i(i,:));
    end
    tmpC.Qc = sum(tmpC.Qc_i)./prm.N;  
end

tmpC.IterNum = 0;
tmpC.Converge = 0;
tmpC.Change = [];
tmpC.Ici_start = Calc_Ici (tmpC,prm);
tmpC.avgS_start = Calc_avgS (S,tmpC,prm);
tmpC.F_start = tmpC.avgS_start - prm.T*tmpC.Ici_start;

return
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function Ici = Calc_Ici (tmpC,prm)

Ici = 0;
for i=1:prm.N
    for c=1:prm.Nc 
        if tmpC.Qc_i(i,c)>0
            Ici = Ici + prm.Pi(i)*tmpC.Qc_i(i,c)*Local_Log(tmpC.Qc_i(i,c)/tmpC.Qc(c));
        end
    end
end

return
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function avgS = Calc_avgS (S,tmpC,prm)

avgS = 0;
for i1=1:prm.N
    for c=1:prm.Nc 
        for i2=1:prm.N
            if tmpC.Qc(c)>0
                avgS = avgS + prm.Pi(i1)*tmpC.Qc_i(i1,c)*tmpC.Qc_i(i2,c)*prm.Pi(i2)*S(i1,i2)/tmpC.Qc(c);
            end
        end
    end
end

return
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            
function [tmpC] = Iclust_SingleRun (S,tmpC,prm)

while ~tmpC.Converge
    tmpC.IterNum = tmpC.IterNum+1;   
    if mod(tmpC.IterNum,100)==0, IterNum=tmpC.IterNum, end
    tmpC = Update_Qc_i_Qc (S,tmpC,prm); 
    tmpC = CheckLoopLimit (tmpC,prm);
end

tmpC.Ici_end = Calc_Ici (tmpC,prm);
tmpC.avgS_end = Calc_avgS (S,tmpC,prm);
tmpC.F_end = tmpC.avgS_end - prm.T*tmpC.Ici_end;

return
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function tmpC = Update_Qc_i_Qc (S,tmpC,prm)

N = prm.N;
Beta = 1./prm.T;
prevQc_i = tmpC.Qc_i;
Qc_i = tmpC.Qc_i;
Qc = tmpC.Qc;
invQc = 1./Qc;

for i=1:prm.N

    E_i1 = (2/N) * invQc .* ( S(i,:) * Qc_i ); % 2*S(c,i)
    E_i2 = (1/N^2) * invQc .* invQc .* ( diag ( Qc_i' * ( S * Qc_i ) ) )'; % S(c)
    E_i = Beta * (E_i1 - E_i2); %  = 1/T { 2*S(c,i) - S(c) }

    Qc_i(i,:) = Qc.*exp(E_i); % Use " - E_i " if S is a DISTORTION matrix (with zeros on the diagonal)
    Qc_i(i,:) = Qc_i(i,:)./sum(Qc_i(i,:)); % normalization        
    tmpC.Qc_i = Qc_i; 
    
    Qc = sum(Qc_i)./prm.N;    
    invQc = 1./Qc;    
    tmpC.Qc = Qc;

end

tmpC.Change(end+1) = max(max(abs(Qc_i - prevQc_i)));
if tmpC.Change(end) <= prm.SmallChange
    tmpC.Converge = 1;
end

return
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function tmpC = CheckLoopLimit (tmpC,prm)
    
if tmpC.IterNum >= prm.LoopLimit    
    msg = sprintf('NO CONVERGENCE. Last Change:%f. Break since LoopLimit (%d) exceeded',tmpC.Change(end),prm.LoopLimit);
    warning (msg);
    tmpC.WARNING = msg;
    tmpC.Converge = 1;
end
    
return
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function log_inp = Local_Log (inp)

log_inp = log2(inp);

return
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

