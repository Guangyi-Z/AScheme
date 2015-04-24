##ActorScm

A toy Scheme interpreter written in Python, with extra built-in concurrency support, a simple Actor-Model framework.
Let’s name it ActorScm.

The concurrency mechanism is based on Python’s ``gevent`` framework.

###Syntax

stage 1

```scheme
(spawn f args...)   ; => pid
(join pid)  ; => result
```

final stage

```scheme
(defactor ANAME [args] body)
(make-msg sender-aid info)  ; => msg
(get-sender msg)    ; => aid
(get-info msg)   ; => info
(self)  ; => aid

(spawn ANAME args)  ; => aid
(! aid msg)
```

####libactor

```c
void *pong_func(void *args) {
	actor_msg_t *msg;
	
	while(1) {
		msg = actor_receive();
		if(msg->type == PING_MSG) {
			printf("PING! ");
			actor_reply_msg(msg, PONG_MSG, NULL, 0);
		}
		arelease(msg);
	}
	return 0;
}

void *ping_func(void *args) {
	actor_msg_t *msg;
	actor_id aid = spawn_actor(pong_func, NULL);
	while(1) {
		actor_send_msg(aid, PING_MSG, NULL, 0);
		msg = actor_receive();
		if(msg->type == PONG_MSG) printf("PONG!\n");
		arelease(msg);
		sleep(5);
	}
	return 0;
}
```

####Pulsar

    (spawn f arg1 arg2)
This will create a new actor, and start running it in a new fiber.

An actor’s mailbox is a channel, that can be obtained with the ``mailbox-of`` function. 
You can therefore send a message to an actor like so:
Instead of snd we normally use the ! (bang) function to send a message to an actor, like so:
    (snd (mailbox-of actor) msg)
    (snd actor msg)
    (! actor msg)

In many circumstances, an actor sends a message to another actor, and expects a reply. 
In those circumstances, using !! instead of ! might offer reduced latency

The value @self, when evaluated in an actor, returns the actor.
    (rcv (mailbox-of @self))
    (rcv @mailbox)
    (rcv @self)
    (receive)

pattern matching
When an actor receives a message, it usually takes different action based on the type and content of the message.

####Actor-Based Concurrency

* Actor
* Mailbox
* Load Factor Buffer
* Message
* Executor

###Concurrency Support

###Modules Dependency

```
┌──────────┐
│  InPort  │
└──────────┘
      ▲     
      │     
┌──────────┐
│   read   │
└──────────┘
      ▲     
      │     
┌──────────┐
│   Env    │
└──────────┘
      ▲     
      │     
┌──────────┐
│   eval   │
└──────────┘
      ▲     
      │     
┌──────────┐
│  expand  │
└──────────┘
      ▲     
      │     
┌──────────┐
│  parse   │
└──────────┘
```
