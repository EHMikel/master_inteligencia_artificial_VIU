(deftemplate X1
	0 7
	(
		(baja (0 1) (2 0))
		(media (1 0) (3 1) (5 0))
		(alta (3 0) (7 1))
	)
)


(deftemplate X2
	0 7
	(
		(baja (0 1) (2 0))
		(media (1 0) (3 1) (5 0))
		(alta (3 0) (7 1))
	)
)


(deftemplate Y
	0 100
	(
		(poca (0 1) (25 1) (40 0))
		(media (30 0) (50 1) (70 0))
		(mucha (60 0) (80 1) (100 0))
	)
)


(defrule regla_1
	(X1 baja)
	(X2 baja)
=>
	(assert (Y poca))
)

(defrule regla_2
	(X1 baja)
	(X2 media)
=>
	(assert (Y poca))
)

(defrule regla_3
	(X1 media)
	(X2 baja)
=>
	(assert (Y media))
)

(defrule regla_4
	(X1 alta)
	(X2 media)
=>
	(assert (Y mucha))
)

(defrule regla_5
	(X1 alta)
	(X2 alta)
=>
	(assert (Y mucha))
)