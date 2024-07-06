(deftemplate UserSelection
   (slot drink)
   (slot pizza)
   (slot count)
   (slot promotion))

(deftemplate Result
   (slot drink)
   (slot pizza)
   (slot count)
   (slot promotion)
   (slot total-price))

(deftemplate Drink
   (slot name)
   (slot price))

(deftemplate Pizza
   (slot name)
   (slot price))

(deffacts initial-facts
   (Drink (name cola) (price 10))
   (Drink (name pepsi) (price 10))
   (Drink (name sprite) (price 10))
   (Drink (name water) (price 12))
   (Pizza (name margarita) (price 50))
   (Pizza (name pepperoni) (price 50))
   (Pizza (name hawajska) (price 50))
   (Pizza (name wiejska) (price 30))
   (Pizza (name polska) (price 20))
   (Pizza (name morska) (price 44))
   (Promotion (type "2_big_pizzas") (discount 0.25))
   (Promotion (type student) (discount 0.15))
   (Promotion (type kods) (discount 0.2)))

(defrule calculate-price
   ?selection <- (UserSelection (drink ?drink) (pizza ?pizza) (count ?count) (promotion ?promotion))
   ?drink_fact <- (Drink (name ?drink) (price ?drink_price))
   ?pizza_fact <- (Pizza (name ?pizza) (price ?pizza_price))
   ?promotion_fact <- (Promotion (type ?promotion) (discount ?discount))
   =>
   (bind ?base-price (+ ?drink_price (* ?pizza_price ?count)))
   (bind ?discounted-price (* ?base-price (- 1 ?discount)))
   (assert (Result (drink ?drink) (pizza ?pizza) (count ?count) (promotion ?promotion) (total-price ?discounted-price))))
