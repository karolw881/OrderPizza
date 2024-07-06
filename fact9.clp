(deftemplate UserSelection
   (slot drink)
   (slot drink_count)
   (slot pizza)
   (slot size)
   (slot count))

(deftemplate Promocja
   (slot pizza)
   (slot size)
   (slot ilosc)
   (slot cena)
   (slot oszczednosc))

(deftemplate PromocjaNapoje
   (slot drink)
   (slot size)
   (slot ilosc)
   (slot cena)
   (slot oszczednosc))

(deftemplate Result
   (slot drink)
   (slot drink_count)
   (slot pizza)
   (slot size)
   (slot count)
   (slot total-price))

(deftemplate Drink
   (slot name)
   (slot price))

(deftemplate Pizza
   (slot name)
   (slot size)
   (slot price))

(deffacts initial-facts
   (Drink (name none) (price 0))
   (Drink (name cola) (price 10))
   (Drink (name pepsi) (price 10))
   (Drink (name sprite) (price 10))
   (Drink (name water) (price 10))
   (Pizza (name margarita) (size small) (price 20))
   (Pizza (name margarita) (size medium) (price 35))
   (Pizza (name margarita) (size large) (price 50))
   (Pizza (name pepperoni) (size small) (price 20))
   (Pizza (name pepperoni) (size medium) (price 35))
   (Pizza (name pepperoni) (size large) (price 50))
   (Pizza (name hawajska) (size small) (price 20))
   (Pizza (name hawajska) (size medium) (price 35))
   (Pizza (name hawajska) (size large) (price 50))
   (Pizza (name wiejska) (size small) (price 20))
   (Pizza (name wiejska) (size medium) (price 35))
   (Pizza (name wiejska) (size large) (price 50))
   (Pizza (name polska) (size small) (price 20))
   (Pizza (name polska) (size medium) (price 35))
   (Pizza (name polska) (size large) (price 50))
   (Pizza (name morska) (size small) (price 20))
   (Pizza (name morska) (size medium) (price 35))
   (Pizza (name morska) (size large) (price 50)))


(defrule calculate-price
   ?selection <- (UserSelection (drink ?drink) (drink_count ?drink_count) (pizza ?pizza) (size ?size) (count ?count))
   ?drink_fact <- (Drink (name ?drink) (price ?drink_price))
   ?pizza_fact <- (Pizza (name ?pizza) (size ?size) (price ?pizza_price))
   =>
   (bind ?drink_total_price (* ?drink_price ?drink_count))
   (bind ?base-price (+ ?drink_total_price (* ?pizza_price ?count)))
   (assert (Result (drink ?drink) (drink_count ?drink_count) (pizza ?pizza) (size ?size) (count ?count) (total-price ?base-price))))

(defrule promocja-3-za-pol-ceny
   ?f1 <- (UserSelection (pizza ?pizza) (size large) (count ?count&:(>= ?count 3)))
   =>
   (bind ?promocja-ilosc (div ?count 3))
   (bind ?cena-podstawowa (* ?promocja-ilosc 50))
   (bind ?cena-promocyjna (* ?promocja-ilosc 25))
   (bind ?oszczednosc (* ?promocja-ilosc 25))
   (assert (Promocja (pizza ?pizza) (size large) (ilosc ?promocja-ilosc) (cena ?cena-promocyjna) (oszczednosc ?oszczednosc))))

;;silnik reguluowy , speceficznr elementy gdzie w innych miejscach to nie wystepuja w jezykach .
;; potym opisujemy strukjtury faktow i reguly

;; cel projektu programowanie regułowe poprzezzamowienia pizzeri zalozono naliczanie aplikacj ama umoLiwac wybranie pizzy i innych napojow i wyliczenie ceny zamownie po promocji , jakie technologie uzyte , załozono ze technologia aplkiacja silnik regulowy vlips i poznij przechodzimuy do opisu produktyu wyniku działania aplikacji jest screen shot a pote opisanie aplikacji bebbechy uruchomenie silnika regulowego , elementy specyficzny
(defrule promocja-3-rozne-duze-pizze
   (UserSelection (pizza ?pizza1) (size large) (count ?count1&:(>= ?count1 1)))
   (UserSelection (pizza ?pizza2&:(neq ?pizza2 ?pizza1)) (size large) (count ?count2&:(>= ?count2 1)))
   (UserSelection (pizza ?pizza3&:(and (neq ?pizza3 ?pizza1) (neq ?pizza3 ?pizza2))) (size large) (count ?count3&:(>= ?count3 1)))
   =>
   (bind ?total-count (+ ?count1 ?count2 ?count3))
   (if (>= ?total-count 3)
       then
           (bind ?promocja-ilosc (div ?total-count 3))
           (bind ?cena-podstawowa (* ?promocja-ilosc 50))
           (bind ?cena-promocyjna (* ?promocja-ilosc 25))
           (bind ?oszczednosc (* ?promocja-ilosc 25))
           (assert (Promocja (pizza large_promotion) (size large) (ilosc ?promocja-ilosc) (cena ?cena-promocyjna) (oszczednosc ?oszczednosc)))))

;; Rule for the "Buy 3, Get 1 Free" drink promotion
(defrule promocja-3-drinki-1-za-darmo
   ?f1 <- (UserSelection (drink ?drink) (drink_count ?drink_count&:(>= ?drink_count 4)))
   ?drink_fact <- (Drink (name ?drink) (price ?drink_price))
   =>
   (bind ?free_drinks (div ?drink_count 4)) ;; Number of free drinks
   (bind ?paid_drinks (- ?drink_count ?free_drinks)) ;; Drinks to be paid
   (bind ?cena-promocyjna (* ?paid_drinks ?drink_price)) ;; Promotional price for drinks
   (bind ?oszczednosc (* ?free_drinks ?drink_price)) ;; Savings from the promotion
   (assert (PromocjaNapoje (drink ?drink) (size none) (ilosc ?free_drinks) (cena ?cena-promocyjna) (oszczednosc ?oszczednosc))))
