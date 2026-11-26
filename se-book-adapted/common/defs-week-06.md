{# Definitions for week-06. Owned by the agent populating this week.
   Each definition lives in its own anchored span; chapters include it:
   <box type="definition" seamless><include src="common/defs-week-06.md#def-<term>" trim /></box>
   se-book phrasing: short, testable, no filler. Cite the course source where applicable. #}

<span id="def-mvc">

**Model-View-Controller (MVC)** is an architectural style that separates an interactive application into three components: the **view** (the UI widgets the user sees), the **controller** (which coordinates between the model and the view, handling user input), and the **model** (which represents the business logic and holds the state of the system).

%%Source: L6-Architecture slides 18–19.%%

</span>

<span id="def-spa">

**A single-page application (SPA)** is a (JavaScript) program downloaded into the browser that runs continuously there, sending queries and retrieving data in the background without refreshing the web page.

%%Source: L6-Architecture slides 23–25.%%

</span>

<span id="def-rest">

**REST (REpresentational State Transfer)** is an architectural style for distributed hypermedia systems, defined by a set of constraints — client-server, stateless, cacheable, layered system, uniform interface, and optionally code-on-demand — for transferring, accessing, and manipulating textual representations of resources in a stateless manner across a network.

%%Source: L6-REST slides 3–6.%%

</span>

<span id="def-statelessness">

**Statelessness** is the REST constraint that each client-server interaction must be entirely self-contained: the full information needed to serve a request travels in the request itself (URI, headers, query parameters), and the server maintains no client session state.

%%Source: L6-REST slide 8.%%

</span>

<span id="def-uniform-interface">

**The uniform interface** is the REST constraint that there be one standard way of interacting with a server, irrespective of the client's device or application type: requests use the HTTP verbs (GET, PUT, POST, DELETE), responses use HTTP status codes, and the resource representation travels in the HTTP body.

%%Source: L6-REST slides 11–12.%%

</span>

<span id="def-layered-architecture">

**The layered architectural style** organizes software as layers of components whose dependencies all point downward: each layer has a distinct and specific responsibility, and a layer obtains services from the layer(s) below it.

%%Source: L6-Architecture slides 6–8.%%

</span>

<span id="def-pipe-and-filter">

**The pipe-and-filter architectural style** divides an application's task into a sequence of self-contained processing steps (**filters**) connected by intermediate data channels (**pipes**): each filter transforms its input stream, computes incrementally, produces output in a defined format, and shares no state with the other filters.

%%Source: L6-Architecture slides 9–12.%%

</span>
