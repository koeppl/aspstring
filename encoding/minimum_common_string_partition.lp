%%INPUT: s(K,I, c), where the k-th string at position i has character c

%% set the entries in the matrix to true that are defined by the input
spos(I) :- s(0,I,_).
tpos(J) :- s(1,J,_).

%% positions 0 are factor starting positions
p(0).
q(0).

%% potential reference from T[t] to S[s]
arc(I,J) :- s(0,I,C), s(1,J,C).

1 { ref(I,J) : arc(I,J) } 1 :- spos(I).  %% (MCSP1)

1 { ref(I,J) : arc(I,J) } 1 :- tpos(J).  %% (MCSP2)

q(J) :- p(I), ref(I,J). %% (MCSP3)

p(I) :- q(J), ref(I,J). %% (MCSP4)

p(I) :- ref(I,J), s(0,I-1,C), s(1,J-1,D), C != D.  %% (MCSP5)

p(I) :- not ref(I-1, J-1), ref(I, J). %% (MCSP6)

%% objective
#minimize { 1,X : p(X) }. %% (MCSP7)

#show ref/2.
#show p/1.
#show q/1.
