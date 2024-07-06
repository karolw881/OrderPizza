(deftemplate TestFact
    (slot value))

(deffacts initial-facts
    (TestFact (value "Initial Fact")))

(defrule sample-rule
    =>
    (assert (TestFact (value "Hello, CLIPS!"))))
