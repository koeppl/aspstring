%%% Acyclic encoding
% Time-stamp: <2024-01-22 14:52:07 banbara>

node(X) :- w(X,_,_).
edge(X,Y) :- w(X,Y,_), X<Y.

1 { start(X) : node(X) } 1.

%{ cycle(X,Y) ; cycle(Y,X) } :- edge(X,Y).
{ cycle(X,Y) ; cycle(Y,X) } 1 :- edge(X,Y).

:- not 1 { cycle(X,_) } 1, node(X).
:- not 1 { cycle(_,X) } 1, node(X).

#edge(X,Y): cycle(X,Y), not start(Y).

#maximize { C,X,Y : cycle(X,Y), w(X,Y,C), not start(Y) }. 

