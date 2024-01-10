(defrule regla_1
	(declare (CF 0.7))
	(or	(motor no_arranca)
		(luces no_se_encienden)
	)
=>
	(assert (problema electrico))
)

(defrule regla_2
	(declare (CF 0.2))
	(motor no_arranca)
=>
	(assert (problema combustion))
)

(defrule regla_3
	(declare (CF 0.2))
	(luces no_se_encienden)
=>
	(assert (bateria en_mal_estado))
)

(defrule regla_4
	(declare (CF 0.1))
	(bateria en_mal_estado)
	(problema combustion)
=>
	(assert (revisar en_taller))
)

(defrule regla_5
	(declare (CF 0.6))
	(problema electrico)
=>
	(assert (revisar en_taller))
)