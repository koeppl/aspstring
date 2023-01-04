%%INPUT: s(K,I, c), where the k-th string at position i has character c

%% num_strings : #strings
num_strings(m-1).

%% assume that the shortest string is the first string!

%% set the entries in the matrix to true that are defined by the input
mat(X,I) :- s(X,I,_).

%% (LCS1)

{ c(X,L,I) : mat(X,I), I >= L } 1 :- mat(X,L).

% only for security:
% I >= L :- c(X,L,I), mat(X,L). 

%% (LCS2)
1 { c(X,L,J) : J < I, mat(X,J) } 1 :- c(X,L+1,I), mat(X,L), mat(X,L+1).


%% (LCS3)
value(X,L) :- c(X,L,I), mat(X,I), mat(X,L).

% only for security:
% :- not value(X,L), mat(X,L), mat(X,L+1), value(X,L+1). 
% value(X,L-1) :- mat(X,L-1), mat(X,L), value(X,L).  

%% (LCS4)

value(X+1,L) :- value(X,L), mat(X,L), mat(X+1,L).
value(0,L) :- value(M,L), num_strings(M).

%% (LCS5)

:- c(X+1,L,J), c(X,L,I), s(X,I,D), not s(X+1,J,D).
:- c(0,L,J), c(M,L,I), s(M,I,D), not s(0,J,D), num_strings(M).

%% (LCS6)

1 { c(X,L,I) : mat(X,I), I >= L } :- value(X,L).

%% (LCS5')

% 1 { c(X+1,L,J) : s(X+1,J,C) } 1 :- c(X,L,I), s(X,I,C), mat(X+1,L).    
% 1 { c(0,L,J) : s(0,J,C) } 1 :- c(M,L,I), s(M,I,C), num_strings(M). 

%% (LCS7)

#maximize { 1,L : value(0,L) }.

%% output

#show c/3.
% #show value/2. 
