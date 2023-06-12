%% copyright by an anonymous reviewer of CPM 2023
% this solutions does not use the directive #sum

mat(X,I) :- s(X,I,_).

1 {t(I,C) : s(_,I,C)} 1 :- mat(_,I).

% model the cost as integers C[x,i] \ge c that we increment

% start: if T[i] != s_x[i], then C[x] \ge 1
c(X,I,1) :- s(X,I,C), not t(I,C).

% if T[i] != s_x[i] and C[i+1,x] \ge n-1, then C[i,x] \ge n
c(X,I,N) :- s(X,I,C), c(X,I+1,N-1), not t(I,C).

% if C[i+1,x] \ge n => C[i,x] \ge n

c(X,I,N) :- mat(X,I), c(X,I+1,N).

#minimize{1,N : c(X,I,N), not mat(X,I-1)}. 

#show t/2.
