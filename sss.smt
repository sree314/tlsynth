(set-logic QF_SLIA)
(set-option :produce-models true)

; simple demo of solving SplitSelect using SMT

(define-fun SplitSelect ((s String) (sep String) (k Int)) String
  (let ((p (str.indexof s sep 0)))
    (ite (= k 0)
         (str.substr s 0 p)
         (str.substr s (+ p 1) (str.len s))
         )
    )
  )


; this definition while complete causes cvc5 to take too long since I
; suspect it doesn't recognize that sep will never not occur in s
; given additional constraints

;; (define-fun SplitSelect ((s String) (sep String) (k Int)) String
;;   (let ((p (str.indexof s sep 0)))
;;     (ite (< p (- 1))
;;          s
;;          (ite (= k 0)
;;               (str.substr s 0 p)
;;               (str.substr s (+ p 1) (str.len s))
;;               )
;;          )
;;     )
;;   )

(declare-const alpha String)
(declare-const beta String)
(declare-const gamma String)
(declare-const sep1 String)
(declare-const sep2 String)
(declare-const x String)

(declare-const start Int)
(declare-const length Int)
(declare-const m Int)
(declare-const k1 Int)


(assert (= alpha (SplitSelect x sep1 k1)))
(assert (str.contains x sep1))
(assert (= beta (SplitSelect alpha sep2 m)))
(assert (str.contains alpha sep2))
(assert (= gamma (str.substr beta start length)))

(assert (str.contains x gamma))
(assert (str.contains alpha gamma))
(assert (str.contains beta gamma))

(assert (= x "Obama, Barack(1961-)"))
(assert (= gamma "Obama"))
(assert (not (= sep1 ")")))
(check-sat)
(get-model)

