%%% copyright by an anonymous reviewer of CPM 2023


%% INPUT of the form 'c(X,Y,C)' storing the overlap of x-th and y-th string in the value 'C'

node(X) :- w(X,_,_).

%% build a Hamiltonian path `path`

%% for each node, select at most one out-going edge

{path(X,Y) : w(X,Y,C)} 1 :- node(X).

%% for each node, select at most one in-coming edge

{path(X,Y) : w(X,Y,C)} 1 :- node(Y).

%% we want that each node is exactly once on the left hand side of an edge in the path

:- #count{X : node(X), not path(X,_)} != 1.

%% we want that each node is exactly once on the right hand side of an edge in the path

:- #count{Y : node(Y), not path(_,Y)} != 1.

%% define the transitive closure of `path` via reachability treating path as undirected
%% start with the smallest node ID as start node

reach(X) :- X = #min{Y : node(Y)}.
reach(X) :- path(X,Y), reach(Y).
reach(Y) :- path(X,Y), reach(X).

%% enforce that all nodes have been reached by the start node

:- node(X), not reach(X).

%% maximize the weight on the obtained path

#maximize{C,X : path(X,Y), w(X,Y,C)}.

#show path/2.
