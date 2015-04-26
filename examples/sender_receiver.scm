
(begin
  (define-actor (receiver)
    (let ((m (rcv)))
      (let ((msg (get-info m)))
        (display msg)
        (display "\n"))))
  (define-actor (sender r)
    (! r "hello, world"))
  (define r (spawn-actor receiver))
  (define s (spawn-actor sender r))
  (start-actor r s)
  (sleep 1)
  (join-actor r s))
