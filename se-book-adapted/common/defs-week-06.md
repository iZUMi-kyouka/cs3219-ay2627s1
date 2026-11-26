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

<span id="def-closed-layer-architecture">

A **closed layer architecture** allows interaction only between two consecutive layers: each layer talks only to the layer directly below it.

%%Source: L6-Architecture slide 8.%%

</span>

<span id="def-open-layer-architecture">

An **open layer architecture** lets any top layer get service from any bottom layer, skipping intermediate layers when convenient — at the cost of the dependencies that layering's buys rest on.

%%Source: L6-Architecture slide 8.%%

</span>

<span id="def-tier">

A **tier** is a part of the system deployed separately — a packaging division that depends on how the application code has been packaged (2-tiered/3-tiered/n-tiered). A layer is a logical division inside the software; a tier is a deployment division.

%%Source: L6-Architecture slide 6.%%

</span>

<span id="def-filter">

A **filter** is the processing component of the pipe-and-filter style: it transforms its input streams, computes incrementally (output begins before the input is fully consumed), expects input in a particular format and produces output in a defined format, and is independent — sharing no state with other filters.

%%Source: L6-Architecture slides 9–10.%%

</span>

<span id="def-pipe">

A **pipe** is the connector of the pipe-and-filter style: it transmits the outputs of one filter to the inputs of another, in a defined data format.

%%Source: L6-Architecture slide 9.%%

</span>

<span id="def-web-mvc">

**Web MVC** applies MVC to web applications: the server holds the model; the controller handles the user's HTTP request, selects the model, and prepares the view; the view renders the HTTP response (e.g., HTML templates with server-side scripts); the model is business logic + persistence (directly or via an ORM) and must manage concurrent modifications.

%%Source: L6-Architecture slide 20.%%

</span>

<span id="def-page-controller">

A **page controller** handles the requests for one specific page.

%%Source: L6-Architecture slide 21.%%

</span>

<span id="def-front-controller">

A **front controller** is the single entry point that receives all HTTP requests and maps each to its handler; middleware can sometimes play this role.

%%Source: L6-Architecture slide 21.%%

</span>

<span id="def-ajax">

**Ajax** is a browser technique in which a script in the page sends HTTP requests and processes responses in the background — e.g., an Ajax POST returning JSON text — without refreshing the page; it is the mechanism behind the SPA's background data exchange.

%%Source: L6-Architecture slide 23.%%

</span>

<span id="def-xss">

**Cross-site scripting (XSS)** is a client-side attack in which malicious code runs in the victim's browser — the SPA cost behind "reduced client-side trust": tokens held client-side can be attacked, so every authorization rule must be re-enforced on the server side.

%%Source: L6-Architecture slides 24–25.%%

</span>

<span id="def-hypermedia">

**Hypermedia** is the nonlinear medium of information that combines graphics, audio, video, plain text, and hyperlinks — hypertext (text with hyperlinks to other text) extended beyond text. REST constrains the transfer of representations *of hypermedia*, which is why links inside representations matter.

%%Source: L6-REST slide 5.%%

</span>

<span id="def-client-server-constraint">

The **client-server constraint** separates the concerns of storing data and presenting it: the client requests resources, the server holds them — the client is not concerned with data storage, the server not with user interface or user state — improving the portability of the UI and the scalability of server components, so both evolve independently.

%%Source: L6-REST slide 7.%%

</span>

<span id="def-cacheable">

The **cacheable constraint** requires the server's response to state whether the data is cacheable (and for how long): the client may then return cached data for subsequent equivalent requests — improving efficiency and user-perceived performance — at the cost of possibly stale data.

%%Source: L6-REST slide 9.%%

</span>

<span id="def-rest-layered-system">

The **layered-system constraint** organizes the application as a (network) layered system in which each layer cannot see beyond its immediate neighbor: intermediaries may improve availability and performance (load balancing, caching) and provide data transformation and filtering — at the cost of overall system complexity.

%%Source: L6-REST slide 10.%%

</span>

<span id="def-code-on-demand">

**Code-on-demand** is REST's one optional constraint: client functionality may be extended by downloading executable code (e.g., applets, JavaScript) — simplifying the client from having to pre-implement all functionality and allowing extensibility.

%%Source: L6-REST slide 15.%%

</span>

<span id="def-resource">

A **resource** is the key abstraction of information in REST: a conceptual mapping to a set of entities — a document, an image, a user — identified using stable, global, and unique resource identifiers (e.g., `/device-management/managed-devices/{device-id}`).

%%Source: L6-REST slide 12.%%

</span>

<span id="def-representation">

A **representation** consists of data plus metadata describing the data: the client holding a representation has enough information to modify the resource on the server.

%%Source: L6-REST slide 12.%%

</span>

<span id="def-uri">

A **uniform resource identifier (URI)** is the stable, global, unique identifier by which a REST resource is addressed — e.g., `/device-management/managed-devices/{device-id}`.

%%Source: L6-REST slide 12.%%

</span>

<span id="def-content-negotiation">

**Content negotiation** is the HTTP mechanism by which clients request a preferred representation format (via the `Accept:` header, using MIME types) and the server chooses the appropriate one — reconciling one uniform interface with many media types; binary media travel as binary streams over HTTP.

%%Source: L6-REST slide 13.%%

</span>

<span id="def-grpc">

**gRPC** is a high-performance remote-procedure-call framework using compact binary encoding (Protocol Buffers), multiplexed HTTP/2 connections, and strong typing — the better fit where REST's HTTP+JSON overhead, repeated serialization, and TCP connection costs dominate (high-frequency service-to-service calls).

%%Source: L6-REST slide 18.%%

</span>

<span id="def-model-code-gap">

The **model-code gap** is the difference between the source code and the architecture model. Architecture models help us reason about complexity and scale and cannot be treated as one-to-one mappings to source code: reduce the gap — never expect to close it, and never make models extensional to "eliminate" it.

%%Source: L6-Architecture slide 26; Quiz 2 Q3.%%

</span>
