%%INPUT: s(K,I, c), where the k-th string at position i has character c

%% num_strings : #strings
num_strings(m-1).

%% assume that the shortest string is the first string!

%% set the entries in the matrix to true that are defined by the input
mat(X,I) :- s(X,I,_).

{ c(X,L,I) : mat(X,I), I >= L } 1 :- mat(X,L). %% (LCS1)

% only for security:
% I >= L :- c(X,L,I), mat(X,L). 

1 { c(X,L,J) : J < I, mat(X,J) } 1 :- c(X,L+1,I), mat(X,L), mat(X,L+1). %% (LCS2)


v(X,L) :- c(X,L,I), mat(X,I), mat(X,L).  %% (LCS3)

% only for security:
% :- not v(X,L), mat(X,L), mat(X,L+1), v(X,L+1). 
% v(X,L-1) :- mat(X,L-1), mat(X,L), v(X,L).  

v(X+1,L) :- v(X,L), mat(X,L), mat(X+1,L). %% (LCS4)
v(0,L) :- v(M,L), num_strings(M).

:- c(X+1,L,J), c(X,L,I), s(X,I,D), not s(X+1,J,D). %% (LCS5)
:- c(0,L,J), c(M,L,I), s(M,I,D), not s(0,J,D), num_strings(M).


1 { c(X,L,I) : mat(X,I), I >= L } :- v(X,L).  %% (LCS6)

%% (LCS5')

% 1 { c(X+1,L,J) : s(X+1,J,C) } 1 :- c(X,L,I), s(X,I,C), mat(X+1,L).    
% 1 { c(0,L,J) : s(0,J,C) } 1 :- c(M,L,I), s(M,I,C), num_strings(M). 


#maximize { 1,L : v(0,L) }.  %% (LCS7)

%% output

#show c/3.
% #show v/2. 
% #show v/2. 
