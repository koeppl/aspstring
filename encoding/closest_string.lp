%%INPUT: s(X,I, c), where the k-th string at position i has character c

%% set the entries in the matrix to true that are defined by the input
mat(X,I) :- s(X,I,_).


%% CS1 to let T[i] point to one of the characters of s_k[i], we set t(X,I) to true
1 {t(I,C) : s(_,I,C)} 1 :- mat(_,I). %% (CSP1)

% %% represent the distinct characters at the i-th position of all input strings 
% sigma(I,C) :- s(_,I,C).  
% %1 {t(I,C) : sigma(I,C)} 1 :- mat(_,I). %% (CSP1) 

c(X,I) :- t(I,C), s(X,I,A), C != A. %% (CSP2)

%TODO: rename cost to weight, C to W
cost(X,C) :- C = #sum {1,I : c(X,I)}, mat(X,_). %% (CSP3)
mcost(M) :- M = #max {C : cost(_,C)}.
#minimize {M : mcost(M)}. 


%% output

#show t/2. #show mcost/1. #show cost/2.
