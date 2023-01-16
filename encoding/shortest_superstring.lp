%% INPUT of the form 'c(X,Y,C)' storing the overlap of x-th and y-th string in the value 'C'

node(X) :- w(X,_,_).

%% (SCS1)
%% for each node, select exactly one out-going edge
1 { cycle(X, Y) : w(X, Y, _) } 1 :- node(X).

%% for each node, select exactly one in-coming edge
1 { cycle(X, Y) : w(X, Y, _) } 1 :- node(Y).

%% (SCS2)
%% define the transitive closure of `cycle` via reachability
reach(X, Y) :- cycle(X, Y).
%% (SCS3)
reach(X, Z) :- reach(X, Y), cycle(Y, Z).

%% (SCS4)
%% enforce reachability
:- not reach(X, Y), node(X), node(Y).

%% (SCS5)
%% we omit the incoming arc of one node of the Hamilton cycle such that this node becomes our starting string
1 { startnode(X) : node(X) } 1. 

%%% gain costs except when traversing to the start node
%gain(X,C) :- cycle(X,Y), w(X,Y,C), not startnode(Y).
%
%%% sum up the gained values
%gainsum(D) :- D = #sum { C,X : gain(X,C) }. 

%% (SCS6)
%% maximize the gained values
gainsum(D) :- D = #sum { C,X : cycle(X,Y), w(X,Y,C), not startnode(Y) }. 
#maximize { D : gainsum(D) }. 

#show cycle/2.
#show startnode/1.

%% for debugging
% #show gain/2. 
% #show gainsum/1. 

