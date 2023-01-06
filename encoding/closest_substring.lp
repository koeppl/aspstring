%%INPUT: s(X,I, c), where the k-th string at position i has character c

#const lambda=3.

%% set the entries in the matrix to true that are defined by the input
mat(X,I) :- s(X,I,_).



%% select an offset for each string

1 { d(X, D) : D = 0..n-lambda} 1 :- mat(X,0).

%% represent the distinct characters at the i-th position of all input strings

sigma(I,C) :- s(X,J,C), d(X,D), J-D >= 0, I = J-D.

%% CS1 to let T[i] point to one of the characters of s_k[i], we set t(X,I) to true
1 {t(I,C) : sigma(I,C) } 1 :- mat(_,I), I < lambda.

%% CS2
c(X,I) :- t(I,C), s(X,J, A), d(X,D), I+D == J, I < lambda, A != C.

% %% CS3  
% not c(L,I) :- t(X,I), s(X,I, C), s(L,I,C). 

%% CS4
cost(X,C) :- C = #sum { 1,I : c(X,I) }, mat(X,_).
maxcost(M) :- M = #max { C : cost(_,C) }.
#minimize { M : maxcost(M) }.


%% output

#show t/2.
#show maxcost/1.
#show cost/2.
% #show d/2. 
