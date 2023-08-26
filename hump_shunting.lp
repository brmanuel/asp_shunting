
%% input

#const tracks = 2.
#const cars = 3.

track(1..tracks).
car(1..cars).

% before(i, j, t, m)
% car i precedes car j on track t during move m
init_before(3, 2, 1).
init_before(2, 1, 1).

#program base.

before(I, J, T, 0) :- init_before(I, J, T).


#program step(t).

%% derive

% last(i, t, m)
% car i is the last car on track t during move m
{ last(I, T, t) : track(T) } = 1 :- car(I),
																			#count{ J : before(I, J, T, t), car(J) } = 0.

% predecessor(i, j, m)
% car i is before car j on some track during move m
predecessor(I, J, t) :- before(I, J, T, t).
predecessor(I, K, t) :- predecessor(I, J, t), before(J, K, T, t).

before(I, J, T, t) :- before(I, J, T, t-1),
					 				 		not shunt(T, t-1),
											car(I),
											car(J),
											track(T).

%% choose

{ shunt(T, t) : track(T) } = 1.

0 { before(I, J, T, t) : car(J), track(T) } 1 :- car(I).

%% constrain

:- before(I, I, _, _).

:- #count{ I : car(I), last(I, T, t) } > 1, track(T).

:- predecessor(I, J, t), predecessor(J, I, t-1).

:- #count{ I,T : before(I, J, T, t), car(I), track(T)} > 1, car(J).

#program check(t).

:- before(I, J, T, t), I > J, query(t).

