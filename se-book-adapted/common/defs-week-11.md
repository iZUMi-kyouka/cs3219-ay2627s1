{# Definitions for week-11. Owned by the agent populating this week.
   Each definition lives in its own anchored span; chapters include it:
   <box type="definition" seamless><include src="common/defs-week-11.md#def-<term>" trim /></box>
   se-book phrasing: short, testable, no filler. Cite the course source where applicable. #}

<span id="def-message-construction">

**Message construction** is the choice of what a message should contain and what the receiver should do with it. The three payload kinds are the **command message** (tells the receiver to do something), the **document message** (gives the receiver data to process) and the **event message** (notifies the receiver that something has happened).

(Sources: L11 slides 16–18; Enterprise Integration Patterns, eaipatterns.com.)

</span>

<span id="def-pipes-and-filters">

**Pipes and filters** is a message-flow pattern that connects single-purpose processing steps (*filters*) with message channels (*pipes*): each filter consumes a message, performs one transformation or routing decision, and passes the result to the next filter. A splitter feeding a content-based router feeding an aggregator is a pipes-and-filters flow.

(Sources: L11 slides 15, 46–51; Enterprise Integration Patterns, eaipatterns.com.)

</span>

<span id="def-content-filter">

**Content filter** is a message-transformation pattern that removes data items the receiver does not need from a message before passing it on, so that each message carries only what its consumer requires.

(Sources: L11 slide 15 (pattern map); Enterprise Integration Patterns, eaipatterns.com.)

</span>

<span id="def-content-enricher">

**Content enricher** is a message-transformation pattern that adds data items a message needs but does not carry, typically by looking them up from another source, before passing the message on.

(Sources: L11 slide 15 (pattern map); Enterprise Integration Patterns, eaipatterns.com.)

</span>

<span id="def-request-reply">

**Request-reply** is an asynchronous messaging pattern in which a requestor sends a request message on one channel — carrying a *return address* saying where the reply should go — and later matches the reply message to the request using a *correlation identifier*, instead of blocking on a synchronous call.

(Sources: L11 slides 20–25; Enterprise Integration Patterns, eaipatterns.com.)

</span>
