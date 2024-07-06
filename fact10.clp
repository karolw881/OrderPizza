(deftemplate Napoj
  (slot nazwa (type SYMBOL))
  (slot cena (type INTEGER)))

(deftemplate Pizza
  (slot nazwa (type SYMBOL))
  (slot cena (type INTEGER)))

(deftemplate ROZMIAR
  (slot nazwa (type SYMBOL))
  (slot cena (type INTEGER)))

(assert (Napoj (nazwa cola) (cena 5)))
(assert (Napoj (nazwa woda) (cena 100)))
(assert (Pizza (nazwa marg) (cena 250)))
(assert (Pizza (nazwa Lepper) (cena 30)))
(assert (Pizza (nazwa polska) (cena 770)))
(assert (ROZMIAR (nazwa MALA) (cena 9)))
(assert (ROZMIAR (nazwa DUZA) (cena 10)))

(defrule r1
  (pizza (nazwa marg) (cena ?cena))
  (ROZMIAR (nazwa MALA) (cena ?rozmiar))
  (test (= ?rozmiar 9))
  =>
  (assert (pizza_marg_mala (cena ?cena))))