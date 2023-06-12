%%% copyright by an anonymous reviewer of CPM 2023
%% Compared to the CPM version, we added another dimension for each possible shift

%% INPUT: 
% s(X,I,c), where the k-th string at position i has character c
% #const lambda=8. 



%% set the entries in the matrix to true that are defined by the input
mat(X,J) :- s(X,J,_).

%% represent all possible shifts with the second dimension such that seq_x[j+d,d] models the d-th character in S_x[j..j+lambda), for which j+lamda-1 \le |S_x|

seq(X,J+D,D) :- mat(X,J), mat(X,J+lambda-1), D = 0..lambda-1.

%% for T[i] we select a character equal to S_x[j] if seq_x[i,j] = True

1 {t(I,C) : s(X,J,C), seq(X,J,I)} 1 :- I = 0..lambda-1.

%% the costs are modelled like for CSP
%% the variable j is for the shift

% if T[i] != s[j] with seq_x[i,j] then C_x[i,j] \ge 1 

c(X,J,I,1) :- seq(X,J,I), s(X,J,C), not t(I,C).

% if T[i] != s[j] with seq_x[i,j] and C_x[i+1,j+1] \ge n-1, then C_x[i,j] \ge n

c(X,J,I,N) :- seq(X,J,I), s(X,J,C), c(X,J+1,I+1,N-1), not t(I,C).

% if C_x[i+1,j+1] \ge n => C_x[i,j] \ge n

c(X,J,I,N) :- seq(X,J,I), c(X,J+1,I+1,N).

% reduce by selecting the shift with the least amount of errors
% if c_x(j,0) < n then set ok(x) = n where j is the first compared character

ok(X,N) :- seq(X,J,0), N = 1..lambda, not c(X,J,0,N).

%% we minimize ok(x) for all x

#minimize{1,N : seq(X,N,N), not ok(X,N+1)}.

#show t/2.

