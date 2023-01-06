%%INPUT: s(X,I, c), where the k-th string at position i has character c

%% set the entries in the matrix to true that are defined by the input
mat(X,I) :- s(X,I,_).

%% represent the distinct characters at the i-th position of all input strings
sigma(I,C) :- s(_,I,C).

%% CS1 to let T[i] point to one of the characters of s_k[i], we set f(X,I) to true
1 {f(I,C) : sigma(I,C) } 1 :- mat(_,I).

%% CS2
c(X,I) :- f(I,C), s(X,I, A), C != A.

%% CS4
cost(X,C) :- C = #sum { 1,I : c(X,I) }, mat(X,_).
maxcost(M) :- M = #max { C : cost(_,C) }.
#minimize { M : maxcost(M) }. 


%% output

#show f/2.
#show maxcost/1.
#show cost/2.
