(defrule regla_1
	(declare (CF 0.9))
	(hora punta)
=>
	(assert (frecuencia_paso_Metro alta))
	(assert (gente_tiene prisa))
)

(defrule regla_2
	(declare (CF 0.5))
	(estacion_Metro llena_gente)
	(gente_tiene prisa)
=>
	(assert (se_producen empujones_entrar_salir))
)

(defrule regla_3
	(declare (CF 0.3))
	(dia laborable)
=>
	(assert (se_producen empujones_entrar_salir))
)

(defrule regla_4
	(declare (CF 0.7))
	(or 	(hora punta)
		(fin_de_mes)
	)
=>
	(assert (estacion_Metro llena_gente))
)

(defrule regla_5
	(declare (CF 0.6))
	(frecuencia_paso_Metro alta)
=>
	(assert (se_producen empujones_entrar_salir))
)