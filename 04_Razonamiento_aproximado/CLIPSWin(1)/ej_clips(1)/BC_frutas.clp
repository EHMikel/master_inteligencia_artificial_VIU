(defrule regla_1
	(forma alargada)
	(color verde)
=>
	(assert (fruta banana))
)

(defrule regla_2
	(forma alargada)
	(color amarillo)
=>
	(assert (fruta banana))
)

(defrule regla_3
	(forma redonda)
	(diametro <4)
=>
	(assert (fruta pera))
)

(defrule regla_4
	(forma alargada)
	(diametro <4)
=>
	(assert (fruta pera))
)
	
(defrule regla_5
	(forma redonda)
	(diametro >4)
=>
	(assert (fruta de_arbol))
)

(defrule regla_6
	(semillas una)
=>
	(assert (tipo_semilla pepita))
)


(defrule regla_7
	(semillas >1)
=>
	(assert (tipo_semilla multiple))
)

(defrule regla_8
	(tipo_fruta pera)
	(color verde)
=>
	(assert (fruta sandia))
)

(defrule regla_9
	(tipo_fruta pera)
	(superficie suave)
	(color amarillo)
=>
	(assert (fruta melon))
)

(defrule regla_10
	(tipo_fruta pera)
	(superficie rugosa)
	(color verde)
=>
	(assert (fruta melon))
)
 
(defrule regla_11
	(tipo_fruta de_arbol)
	(color naranja)
	(tipo_semilla pepita)
=>
	(assert (fruta albaricoque))
)

(defrule regla_12
	(tipo_fruta de_arbol)
	(color naranja)
	(tipo_semilla multiple)
=>
	(assert (fruta naranja))
)

(defrule regla_13
	(tipo_fruta de_arbol)
	(color rojo)
	(tipo_semilla pepita)
=>
	(assert (fruta cereza))
)

(defrule regla_14
	(tipo_fruta de_arbol)
	(color naranja)
	(tipo_semilla pepita)
=>
	(assert (fruta melocoton))
)

(defrule regla_15
	(tipo_fruta de_arbol)
	(color rojo)
	(tipo_semilla multiple)
=>
	(assert (fruta manzana))
)

(defrule regla_16
	(tipo_fruta de_arbol)
	(color verde)
	(tipo_semilla multiple)
=>
	(assert (fruta manzana))
)

(defrule regla_17
	(tipo_fruta de_arbol)
	(color morado)
	(tipo_semilla pepita)
=>
	(assert (fruta ciruela))
)


(defrule regla_18
	(fruta ?x)
=>
	(printout t "La fruta es una " ?x crlf)
)


