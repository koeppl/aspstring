%%% copyright by an anonymous reviewer of CPM 2023

%%INPUT: s(K,I, c), where the k-th string at position i has character c

mat(X,I) :- s(X,I,_).

%% potential reference from T[t] to S[s]

arc(I,J) :- s(0,I,C), s(1,J,C).

1 {ref(I,J) : arc(I,J)} 1 :- mat(0,I). %% (MCSP1)
1 {ref(I,J) : arc(I,J)} 1 :- mat(1,J). %% (MCSP2)

%% Since there cannot exist a reference for position -1 for either of the input strings, we need to count one reference 

#minimize{1,I : ref(I,J), not ref(I-1,J-1)}.

#show ref/2.
