%%INPUT: s(K,I, c), where the k-th string at position i has character c

%% assume that the shortest string is the first string!

%% set the entries in the matrix to true that are defined by the input
mat(X,I) :- s(X,I,_).

% {text(X,L,I) : mat(X,I), I >= L} 1 :- mat(X,L). %% (LCS1) 
%% defines the range in which we can the values of c
0 {text(X,L,I) : mat(X,I), I >= L} :- mat(X,L). %% (LCS1)

% only for security:
% I >= L :- text(X,L,I), mat(X,L). 

1 {text(X,L,J) : J < I, mat(X,J)} 1 :- text(X,L+1,I), mat(X,L), mat(X,L+1). %% (LCS2)


v(X,L) :- text(X,L,I), mat(X,I), mat(X,L).  %% (LCS3)

% only for security:
% :- not v(X,L), mat(X,L), mat(X,L+1), v(X,L+1). 
% v(X,L-1) :- mat(X,L-1), mat(X,L), v(X,L).  

v(X+1,L) :- v(X,L), mat(X,L), mat(X+1,L). %% (LCS4)
v(0,L) :- v(m-1,L).

:- text(X+1,L,J), text(X,L,I), s(X,I,D), not s(X+1,J,D). %% (LCS5)
:- text(0,L,J), text(m-1,L,I), s(m-1,I,D), not s(0,J,D).


1 {text(X,L,I) : mat(X,I), I >= L} :- v(X,L).  %% (LCS6)

%% (LCS5')

% 1 { text(X+1,L,J) : s(X+1,J,C) } 1 :- text(X,L,I), s(X,I,C), mat(X+1,L).    
% 1 { text(0,L,J) : s(0,J,C) } 1 :- text(m-1,L,I), s(m-1,I,C). 


#maximize {1,L : v(0,L)}.  %% (LCS7)

%% output

#show text/3.
% #show v/2. 
% #show v/2. 
