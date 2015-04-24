
from parse import parse
from eval import eval

########## built-in macro

eval(parse("""(begin
;; and
(define-macro and (lambda args
   (if (null? args) #t
       (if (= (length args) 1) (car args)
           `(if ,(car args) (and ,@(cdr args)) #f)))))

;; More macros can also go here
)"""))

eval(parse("""
;; cond
(define-macro cond (lambda args
  (let ((hd (car args)))
    (if (= "else" (car hd))
      (cadr hd)
      (if (car hd)
        (cadr hd)
        `(cond ,@(cdr args)))))))
"""))
