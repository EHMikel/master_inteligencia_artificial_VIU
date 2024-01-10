(deftemplate V1
	0 6
	(
		(baja (0 1) (1 1) (3 0))
		(media (1 0) (3 1) (5 0))
		(alta (3 0) (5 1) (6 1))
	)
)


(deftemplate V2
	0 6
	(
		(baja (0 1) (1 1) (3 0))
		(media (1 0) (3 1) (5 0))
		(alta (3 0) (5 1) (6 1))
	)
)

(deftemplate potencia
	0 10
	(
		(muy_baja (0 1) (1 1) (3 0))
		(baja (1 0) (3 1) (5 0))
		(media (3 0) (5 1) (7 0))
		(alta (5 0) (7 1) (9 0))
		(muy_alta (7 0) (9 1) (10 1))
	)
)





(defrule regla_1
	(V1 baja)
	(V2 baja)
=>
	(assert (potencia muy_alta))
)

(defrule regla_2
	(V1 baja)
	(V2 media)
=>
	(assert (potencia alta))
)

(defrule regla_3
	(V1 baja)
	(V2 alta)
=>
	(assert (potencia media))
)

(defrule regla_4
	(V1 media)
	(V2 baja)
=>
	(assert (potencia alta))
)

(defrule regla_5
	(V1 media)
	(V2 media)
=>
	(assert (potencia media))
)

(defrule regla_6
	(V1 media)
	(V2 alta)
=>
	(assert (potencia baja))
)

(defrule regla_7
	(V1 alta)
	(V2 baja)
=>
	(assert (potencia media))
)

(defrule regla_8
	(V1 alta)
	(V2 media)
=>
	(assert (potencia baja))
)

(defrule regla_9
	(V1 alta)
	(V2 alta)
=>
	(assert (potencia muy_baja))
)
