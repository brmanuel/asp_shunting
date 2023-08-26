

% input
% 1,3,5,4,6,8,7,2

#const l = 8.
#const tracklength = 3.

track(1..l).
car(1..l).

inseq(1, 1).
inseq(2, 3).
inseq(3, 5).
inseq(4, 4).
inseq(5, 6).
inseq(6, 8).
inseq(7, 7).
inseq(8, 2).


% derive

before(P, Q) :- inseq(I, P), inseq(J, Q), I < J.

% choose

{ move(P, T) : track(T) } = 1 :- inseq(_, P).

% restrict

:- move(P, T), move(Q, T), before(P, Q), P < Q.

:- #count { P : move(P, T), car(P) } > tracklength, track(T).


% optimize

#minimize { 1,T : move(P, T), track(T), car(P)} .
