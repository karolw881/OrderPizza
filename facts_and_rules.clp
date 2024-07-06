(deftemplate Drink
   (slot name)
   (slot price))

(deftemplate Pizza
   (slot name)
   (slot price))

(deftemplate Promotion
   (slot type)
   (slot discount))

(deftemplate UserSelection
    (slot drink)
    (slot pizza)
    (slot promotion)
    (slot count))

(deftemplate Result
   (slot total-price)
   (slot drink)
   (slot pizza)
   (slot promotion))

(deffacts initial-facts
   (Drink (name cola) (price 10))
   (Drink (name pepsi) (price 10))
   (Drink (name sprite) (price 10))
   (Drink (name water) (price 10))
   (Pizza (name margarita) (price 50))
   (Pizza (name pepperoni) (price 50))
   (Pizza (name hawajska) (price 50))
   (Pizza (name wiejska) (price 30))
   (Pizza (name polska) (price 20))
   (Pizza (name morska) (price 44))
   (Promotion (type "2_big_pizzas") (discount 0.25))
   (Promotion (type student) (discount 0.15))
   (Promotion (type kods) (discount 0.20)))

(defrule calculate-total
   ?selection <- (UserSelection (drink ?drink) (pizza ?pizza) (promotion ?promotion))
   ?drink-fact <- (Drink (name ?drink) (price ?drink-price))
   ?pizza-fact <- (Pizza (name ?pizza) (price ?pizza-price))
   ?promotion-fact <- (Promotion (type ?promotion) (discount ?discount))
   =>
   (retract ?selection)
   (assert (Result (total-price (* (- 1 ?discount) (+ ?drink-price ?pizza-price))) (drink ?drink) (pizza ?pizza) (promotion ?promotion))))
(defrule calculate-total
   ?selection <- (UserSelection (drink ?drink) (pizza ?pizza) (promotion ?promotion))
   ?drink-fact <- (Drink (name ?drink) (price ?drink-price))
   ?pizza-fact <- (Pizza (name ?pizza) (price ?pizza-price))
   ?promotion-fact <- (Promotion (type ?promotion) (discount ?discount))
   =>
   (printout t "Rule triggered with: " ?drink " " ?pizza " " ?promotion crlf)
   (retract ?selection)
   (assert (Result (total-price (* (- 1 ?discount) (+ ?drink-price ?pizza-price))) (drink ?drink) (pizza ?pizza) (promotion ?promotion))))
