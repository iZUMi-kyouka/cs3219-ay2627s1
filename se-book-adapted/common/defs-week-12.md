{# Definitions for week-12. Owned by the agent populating this week.
   Each definition lives in its own anchored span; chapters include it:
   <box type="definition" seamless><include src="common/defs-week-12.md#def-<term>" trim /></box>
   se-book phrasing: short, testable, no filler. Cite the course source where applicable. #}

<span id="def-scalability">

**Scalability** is the property of a system to handle a growing amount of work by adding resources to the system. The growth may be in requests processed per time window or in the amount of data managed, while response times stay stable and consistent.

(Sources: L12 slides 4–6; recap of L3, slide 3.)

</span>

<span id="def-vertical-scaling">

**Vertical scaling (scale up)** adds capability to the machines a system is deployed on — e.g. more CPU or memory on the same node — without adding more nodes. It is simple but capped by the hardware limits of a single machine.

(Sources: L12 slides 3, 11.)

</span>

<span id="def-horizontal-scaling">

**Horizontal scaling (scale out)** adds additional machines (nodes) running copies of the service, so that requests are distributed across the replicas. With N replicas and R requests, each server processes about R/N requests.

(Sources: L12 slides 3, 12.)

</span>

<span id="def-load-balancing">

**Load balancing** sends all user requests to a component that chooses which service replica will process each request — aiming to keep every replica equally busy — and relays the responses back to the clients.

(Sources: L12 slide 13.)

</span>

<span id="def-stateless-service">

**Stateless service** is a service whose API implementation retains no state associated with an individual client's session, so any replica can process any request. Session state is kept in a shared session store that every replica can access, which is what makes stateless services cheap to replicate.

(Sources: L12 slide 14.)

</span>
