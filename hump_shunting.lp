
#program base.

before(I, J, T, 0) :- initbefore(I, J, T).
last(I, T, 0) :- initlast(I, T).

#program step(t).

%% derive

% last(i, t, m)
% car i is the last car on track T during move t
last(J, T, t) :- car(I),
					 			 car(J),
					 			 track(T),
								 before(I, J, T, t),
					 			 #count{ K : before(J, K, T, t), car(K) } = 0.

{ last(I, T, t) : track(T) } = 1 :- car(I),
																			#count{ J : before(I, J, T, t), car(J) } = 0.

% on(i, t, m)
% car i is on track t during move m
on(I, T, t) :- before(I, J, T, t).
on(I, T, t) :- last(I, T, t).

% predecessor(i, j, m)
% car i is before car j on some track during move m
predecessor(I, J, t) :- before(I, J, T, t).
predecessor(I, K, t) :- predecessor(I, J, t), before(J, K, T, t).

before(I, J, T, t) :- before(I, J, T, t-1),
					 				 		not shunt(T, t-1).

last(I, T, t) :- last(I, T, t),
					 			 not shunt(T, t-1).


%% choose

{ shunt(T, t) : track(T) } = 1.

0 { before(I, J, T, t) : car(J), track(T) } 1 :- car(I).

%% constrain

% a car can not be its own predecessor
:- before(I, I, _, _).

% each track has at most one rightmost car
:- #count{ I : car(I), last(I, T, t) } > 1, track(T).

% each car has at most one predecessor
:- #count{ I,T : before(I, J, T, t), car(I), track(T)} > 1, car(J).

% the order of two cars on the same track can't be changed in one shunt
:- predecessor(I, J, t), predecessor(J, I, t-1).

% shunting adds cars always to the back of a track
% (new cars come "after" the cars that were already on the track)
:- on(I, T1, t-1), on(J, T2, t-1), shunt(T2, t-1), T1 != T2, before(J, I, T1, t).

% cars that aren't shunted stay on their track
:- on(I, T1, t-1), not shunt(T1, t-1), on(I, T2, t), T1 != T2.

#program check(t).

#external query(t).

% Cars are ordered in ascending order on each track
:- before(I, J, T, t), I > J, query(t).

