frame(X) -->
    [0,1,1,1,1,1,1,0],
    stuff(X),
    [0,1,1,1,1,1,1,0],
    checksum(X).

stuff([]) --> ``.
stuff([0,1,1,1,1,1|Xs]) --> {!}, [0,1,1,1,1,1,0], stuff(Xs).
stuff([0|Xs]) --> [0], stuff(Xs).
stuff([1|Xs]) --> [1], stuff(Xs).

unframe(X) -->
    [0,1,1,1,1,1,1,0],
    unstuff(X),
    [0,1,1,1,1,1,1,0],
    checksum(X).

unstuff([]) --> [].
unstuff([0,1,1,1,1,1,0|Xs]) --> {!}, [0,1,1,1,1,1], unstuff(Xs).
unstuff([0|Xs]) --> [0], unstuff(Xs).
unstuff([1|Xs]) --> [1], unstuff(Xs).


checksum(_) --> ``.