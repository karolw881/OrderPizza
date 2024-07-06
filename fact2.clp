(deftemplate UserSelection
   (slot drink)
   (slot pizza)
   (slot size)


(deftemplate Result
   (slot drink)
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
   (Pizza (name wiejska) (size small) (price 15))
   (Pizza (name wiejska) (size medium) (price 25))
   (Pizza (name wiejska) (size large) (price 30))
   (Pizza (name polska) (size small) (price 10))
   (Pizza (name polska) (size medium) (price 15))
   (Pizza (name polska) (size large) (price 20))
   (Pizza (name morska) (size small) (price 22))
   (Pizza (name morska) (size medium) (price 33))
   (Pizza (name morska) (size large) (price 44)))

(defrule calculate-price
   ?selection <- (UserSelection (drink ?drink) (pizza ?pizza) (size ?size) (count ?count))
   ?drink_fact <- (Drink (name ?drink) (price ?drink_price))
   ?pizza_fact <- (Pizza (name ?pizza) (size ?size) (price ?pizza_price))
   =>
   (bind ?item-price (+ ?drink_price (* ?pizza_price ?count)))
   (assert (Result (drink ?drink) (pizza ?pizza) (size ?size) (count ?count) (total-price ?item-price)))
   (retract ?selection))


