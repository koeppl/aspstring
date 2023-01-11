
%% the maximum length of the string we want to output
target_length(n*m).

%% enumerate the characters of the alphabet
alphabet(C) :- s(_,_,C).

%% assume that 0 is a special character of the input!
alphabet(0).


targetposition(I) :- I = 0..N-1, target_length(N).

%% (CSS1)

1 { t(I,C) : alphabet(C) } 1 :- targetposition(I).

%% (CSS2)

t(I+1,0) :- t(I,0), targetposition(I+1).

%% (CSS3) 

t(I,C) :- m(I,X,J), s(X,J,C).

%% (CSS4)

m(I-1,X,J-1) :- m(I,X,J), J > 0.

%% (CSS5)

1 { m(I,X,n-1) : t(I,_), I >= n-1 }  :- s(X,n-1,_).

%% optimization

#maximize { 1,I : t(I,0) }.

%% output

#show t/2.
#show m/3.
