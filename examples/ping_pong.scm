
(begin
  (define-actor (Ping pong)
    (define (f)
      (let ((m (rcv)))
        (let ((info (get-info m)))
          (display "Ping < ")
          (display info)
          (display "\n")
          (cond ((= "finish" info) (! pong "finish") (display "Ping finished"))
                (else (display "ping") (display "\n") (! pong "ping") (f))))))
    (f))
  (define-actor (Pong)
    (define (f)
      (let ((m (rcv)))
        (let ((info (get-info m))
              (sdr (get-sender m)))
          (display "Pong < ")
          (display info)
          (display "\n")
          (cond ((= "ping" info) (display "pong") (display "\n") (! sdr "pong") (f))
              (else (display "Pong finished"))))))
    (f))
  (define pong (spawn-actor Pong))
  (define ping (spawn-actor Ping pong))
  (start-actor pong ping)
  (! ping "pong")
  (sleep 1)
  (! ping "finish"))
  (join-actor ping pong)
