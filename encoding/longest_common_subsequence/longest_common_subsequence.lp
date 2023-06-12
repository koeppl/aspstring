%%% copyright by an anonymous reviewer of CPM 2023

%%INPUT: 
% s(X,I,C), where the x-th string at position i has character c
% assume that the shortest string is the first string s(0,_,_)!

mat(X,I) :- s(X,I,_).

%% select characters from the first string with c_x(i)

{selected(I)} :- mat(X,I), not mat(X-1,0).

%% emulate a successor query : for each position in [1..n], find the next position selected by `c`
%% For that, successor(i,j) = 1 if c[j] = 1 and there is no `c` between i+1..j

%% If the next position i+1 is set, then i points to i+1

successor(I,I+1) :- mat(0,I), selected(I+1).

%% if the next value c[i+1] is set, then c[i+1] is the successor, and we have set this by the above statement
%% otherwise copy the arc from position i+1 since it must have the same successor

successor(I,J)   :- mat(0,I), successor(I+1,J), not selected(I+1).

%% Optimization:
%% If successor(i) = j but S_0[i] = S_1[j] = c, then we could have already started with selected(i) = 1 (so select the leftmost occurrence if we have the choice). In that sense we enforce that i and j are selected.

:- s(0,I,C), s(0,J,C), successor(I,J), not selected(I).

%% We code the longest common subsequence `T` we try to build as a three-dimensional array `subsequence(i,n,c)` such that T[n] = c = S_0[i]

%% We start with two cases: whether 0 is selected or not
%% If 0 is selected, then T[0] = c = S_x[0] 

subsequence(0,0,C) :- s(0,0,C), selected(0).

%% Otherwise, we take the successor of 0. If that is position i, then T[0] = S_0[i] = c 

%%TODO: We can reduce that to subsequence(I,0,C) :- s(0,I,C), successor(0,I), not selected(0). since it cannot be that S_0[0] = c

subsequence(I,0,C) :- s(0,I,C), successor(0,I), not s(0,0,C), not selected(0).

%% If |T| \ge n-1, the last selected character was $S_0[i]$ and successor(i,j) then T[n] = S_0[j] = c

subsequence(J,N,C) :- s(0,J,C), successor(I,J), subsequence(I,N-1,C').

%% set T[n] = c

subsequence(N,C)     :- subsequence(I,N,C).

%% set |T| \ge n 

subsequence(N)       :- subsequence(N,C).

%% check whether the subsequence `subsequence` is a subsequence of the other strings
%% First, we define the matchings we need to perform, which we call `compare` since we are unsure whether we can match

%% go from string Y-1 to Y unless Y does not exist, start matching $T[0] = c $ with S_y[0..]

compare(Y,0,0,C) :- mat(Y,0), subsequence(0,C), mat(Y-1,0).

%% if we compared S_y[i-1] <> T[n-1], then start comparing S_y[i..] <> T[n] = c
%% Note that this can spawn unnecessary comparisons as we are unsure whether S_y[i] <> T[n] directly matches. Anyway, those unnecessary comparisons must hold if T is a subsequence of S_y since we here treat T[n-1] kind of as a wildcard

compare(Y,I,N,C) :- mat(Y,I), subsequence(N,C), compare(Y,I-1,N-1,_).

%% we failed to match T[n] = c with the character S_y[i-1] != c, so we try to match $S_y[i]$ with $c$

compare(Y,I,N,C) :- mat(Y,I), compare(Y,I-1,N,C), not s(Y,I-1,C).

%% The following enforces that we have to successfully find $T$ as a subsequence in $S_y$
%% if we need to compare T[n] = c <> S_y[i], then either S_y[i] = c and we are done, or we have to compare with S_y[i+1]

:- compare(Y,I,N,C), not s(Y,I,C), not mat(Y,I+1).

%% In case that we try to match T[n] <> S_y[i] = c, but |T| > n, then we also need to match $T[n+1]$ with some character in $S_y[i+1..]$

:- compare(Y,I,N,C), subsequence(N+1), s(Y,I,C), not mat(Y,I+1).

#maximize{1,N : subsequence(N)}.

% #show subsequence/2. 
% #show c/1.  
% #show successor/2. 
#show subsequence/2.
