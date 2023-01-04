%%INPUT: s(K,I, c), where the k-th string at position i has character c

%% set the entries in the matrix to true that are defined by the input
mat(K,I) :- s(K,I,_).

lambda(3).

%% select an offset for each string

1 { d(X, D) : 1..n-lambda } 1 :- mat(X,0).

%% CS1 to let T[i] point to one of the characters of s_k[i], we set f(K,I) to true
1 {f(K,I) : mat(K,I) } 1 :- mat(_,I).

%% CS2
c(Y,I) :- f(X,I), s(X,J, A), s(Y,K,B), A != B, d(X,D), d(Y,E), J+D == K+E, K+E == I, I < lambda.

% %% CS3  
% not c(L,I) :- f(K,I), s(K,I, C), s(L,I,C). 

%% CS4
cost(L,C) :- C = #sum { 1,I : c(L,I) }, mat(L,_).
maxcost(M) :- M = #max { C : cost(_,C) }.
#minimize { M : maxcost(M) }.


%% output

#show f/2.
#show maxcost/1.
#show cost/2.
