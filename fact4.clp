(deftemplate UserSelection
   (slot drink)
   (slot drink_count)
   (slot pizza)
   (slot size)
   (slot count))

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
   (bind ?drink_total_price (* ?drink_price ?drink_count))  ;; Calculate total price for drinks for the selected pizza
   (bind ?base-price (+ ?drink_total_price (* ?pizza_price ?count))) ; Calculate base price without discount

   ;; Check if the remainder of pizza count divided by 4 is zero
   (if (= (mod ?count 4) 0)
       then
       (bind ?discounted-price (- ?base-price (* 0.1 ?base-price))) ; Calculate discounted price
       (assert (Result (drink ?drink) (drink_count ?drink_count) (pizza ?pizza) (size ?size) (count ?count) (total-price ?discounted-price)))
       else
       (assert (Result (drink ?drink) (drink_count ?drink_count) (pizza ?pizza) (size ?size) (count ?count) (total-price ?base-price)))
   )
)




