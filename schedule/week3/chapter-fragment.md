{% from "schedule/macros-fragment.md" import term, example with context %}
<h2>Week 3 — Requirements</h2>

<span>

This chapter builds on [Week 1]({{baseUrl}}/se-book-adapted/chapters/week-01-software-development-processes.html#W1-c3)'s software process and product backlog (W1.3): requirements are what fills that backlog. No other background is needed.

</span>

<span>

* Can explain what a requirement is and walk a requirement through elicitation, analysis, specification, and validation
* Can distinguish functional from non-functional requirements and write requirements in usage-centric and product-centric form
* Can build a two-level product backlog with priorities, sprints, and traceable identifiers for a concrete product
* Can classify quality attributes as external or internal and specify security, performance, scalability, deployability, and usability requirements
* Can analyze quality-attribute trade-offs and choose what to prioritize under constraints

</span>

<div>

<box type="important" seamless>

**Revision priority:** ★ = core; ★★ = supporting detail; ★★★ = extension; ★★★★ = optional context.
</box>

<box type="info" seamless>

**The running example — FoC, a campus errand and pickup platform.** Students (requesters) post errands — e.g., collecting an order from a campus vendor — and couriers accept and deliver them for credits held in a wallet. The credit economy is *closed*: credits exist only inside FoC — assigned at sign-up and moved between users as errands are posted, delivered, or refunded — never bought with or cashed out into real money (Tutorial 2 appendix F4). Vendors (suppliers) and their handover points are administered by the platform; users register with university email and password. This is the project-style platform used in the course's example decks and Tutorial 2: its requirements are organized by {{ term("microservice", "an independently deployable service modeled around a business domain") }} — a **user service** (accounts, trust), a **supplier service** (vendors and pickup points), a **credit service** (the wallet), and an **order service** (errand lifecycle, courier matching) (Source: L4-AlternativeExamplesForProductBacklog deck, all slides; Tutorial 2 appendix). When a requirement below is quoted from that deck, it names the service.
</box>

## Core concepts

<span id="W3-c1"></span>


<panel type="seamless" expanded>
  <span slot="header" class="card-title"><markdown>### W3.1 Requirements and their development ★</markdown></span>


**Everything the team builds traces back to requirements — get them wrong and the best architecture delivers the wrong product.** A requirement is defined broadly enough to cover users' needs, system obligations, and the documents that record them.

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-03.md#def-requirement" trim />
</box>

**A requirement specification reads as a set of capabilities and constraints.** Capabilities state what users can do through the system; constraints bound where, how, or under what conditions those capabilities operate — and constraints typically end up among the non-functional requirements, as the operating boundaries of the product.

<box type="info" seamless>

**Telling apart — capability vs constraint.** One distinguishing question: **does the sentence enable an action, or bound one?**

| | Capability | Constraint |
|---|---|---|
| States | An action the system makes possible | A boundary the system operates within |
| FoC example | "The courier should be able to pick up an errand from a pickup point and hand it over at the drop-off point the requester specified" | "All locations supported by FoC are confined to campus" |
| Where it lands | Functional requirements | Usually non-functional requirements ("these are the operating boundaries of the product") |

%%Both sentences paraphrase the lecturer's FoC examples (L3 recording, ~[25:00]). Exam hint from the same passage: "spoiler alert — we'll be looking at these kinds of examples; noting them will help you come up with the requirements of the project later."%%

</box>

**Requirements development has four phases, and they loop.**

- {{ term("elicitation", "discovering requirements, e.g., by interview, workshop, document analysis, or prototyping") }} discovers requirements
- {{ term("analysis", "analyzing, decomposing, deriving, and negotiating requirements, and identifying gaps") }} clarifies and closes gaps
- {{ term("specification", "writing and illustrating requirements for comprehension, review, and use") }} rewrites them so others can review and use them
- {{ term("validation", "confirming the correct set of requirements that will enable developers to build a solution") }} re-evaluates and confirms and corrects — feeding back to elicitation

(Source: L3 slide 4)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-03.md#def-elicitation" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-03.md#def-requirements-analysis" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-03.md#def-specification" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-03.md#def-requirements-validation" trim />
</box>

<mermaid>
flowchart LR
    E["Elicitation<br/>discover"] --> A["Analysis<br/>clarify, close gaps"]
    A --> S["Specification<br/>rewrite"]
    S --> V["Validation<br/>re-evaluate, confirm & correct"]
    V -. "gaps & corrections" .-> E
</mermaid>

%%Notation: each box is one phase of requirements development; solid arrows show the forward path of a requirement; the dashed arrow is the rework loop — validation sends you back with what it found.%%

How to read it for the running example: FoC's "a student profile will be disabled after 3 failed password or OTP attempts" (OTP — a one-time passcode, a code valid for a single login) did not appear fully formed — someone elicited the account-safety concern from the platform's rules, analyzed it into a testable rule, wrote it into the user-service backlog, and validated that 3 (not 5) attempts matches the intended balance of safety and usability (Source: L4-AlternativeExamplesForProductBacklog, user service N2.2.1; L3 slide 4).

**Requirements come from many kinds of sources, not just stakeholders' first sentences.** The deck lists documents (descriptions of current or competing products, standards or regulations, help-desk problem reports), interviews (focus groups, use-case workshops, product champions — the slide's "key customer rep": a representative of one user class who supplies that class's requirements), questionnaires and marketing surveys (run a pilot first — difficult to ask clear questions), event-response tables (identify external stimuli and describe system responses), observation (watch users do their jobs; workflow diagrams, "day in the life" studies), and prototyping (useful for requirements, design, and implementation) (Source: L3 slide 5).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-03.md#def-event-response-table" trim />
</box>

{% call example("FoC — the same requirement surfacing from three sources") %}
For FoC, the wallet-refund rule ("if the requester removes the errand, the courier leaves it, or the pickup time is missed, the charged credits should be returned") could surface from all three source kinds: help-desk problem reports after a courier no-show leaves credits stuck, an interview with the campus office that owns the credit economy, and an event-response table listing the stimulus "courier marks delivered" against the response "held credits transfer to the courier" (Source: requirement quoted from L4-AlternativeExamplesForProductBacklog, credit service 5.5; source types from L3 slide 5).
{% endcall %}

{% call example("How elicitation and validation run in this course") %}
For the course project, elicitation is mostly **brainstorming** from the project context — plus **document analysis of competing products**: "take a look at other apps like Grab and Gojek and see what all they provide." Validation is the point where the team presents the requirement set and receives "ok / not ok / need more work" feedback — and a problem found there sends work back to any earlier phase, because the process is iterative, not linear (L3 recording, ~[27:00] and ~[30:00]; L3 slide 4).
{% endcall %}

<box type="tip" seamless>

**Real requirement inputs arrive underspecified — treat clarifying questions as part of elicitation.** The lecturer's project context deliberately leaves things open (e.g., "there should be an admin capability" — without saying who the admin is, how it works, or what interface it gets): "this is kind of a realistic way in which you can get software requirements from the field." The elicitation response is to ask, and to get assumptions validated before you build on them (L3 recording, ~[5:00]).

</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** A teammate says "requirements are just what the customer asks for on day one". Which part of the requirements-development loop does this ignore, and what does that loop contribute?

<panel type="seamless" minimized header="%%Answer%%">

It ignores analysis (decompose, derive, negotiate; identify gaps), specification (rewrite for comprehension, review, and use), and validation (confirm the correct set that enables developers to build a solution) — the loop is what turns raw stakeholder wishes into a buildable, reviewed set (Source: L3 slide 4).

</panel>

**Q2.** You must find out how campus vendors actually hand over orders today. Which two elicitation sources fit best, and why?

<panel type="seamless" minimized header="%%Answer%%">

Observation (watch users do their jobs; "day in the life" studies, workflow diagrams) and interviews (e.g., a product champion per vendor) — the knowledge is tacit and practiced, so watching and asking beats questionnaires (Source: L3 slide 5).

</panel>

**Q3.** Classify as capability or constraint: (a) "A requester can specify the pickup and drop-off points for an errand"; (b) "All locations supported by the platform are confined to campus".

<panel type="seamless" minimized header="%%Answer%%">

(a) Capability — it enables an action the system makes possible. (b) Constraint — it bounds the operating space without enabling anything, and lands among the non-functional requirements as an operating boundary (L3 recording, ~[25:00]).

</panel>

</panel>

</panel>

<span id="W3-c2"></span>


<panel type="seamless" expanded>
  <span slot="header" class="card-title"><markdown>### W3.2 Functional vs non-functional requirements ★</markdown></span>


**The FR/NFR split answers two different questions: what must the system do, and how well must it do it.** Mixing them up is how teams ship complete-but-unusable systems.

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-03.md#def-functional-requirement" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-03.md#def-non-functional-requirement" trim />
</box>

**FRs specify behavior; NFRs constrain how the system works and is built.** An FR "specifies something the system should do — typically, specify a behavior or function". An NFR "describes something not directly related to the functionality of the system — may describe how well the system works — can include other attributes too (see quality attributes later)": {{ term("reliability", "the ability of the system to keep working correctly over time") }}, efficiency, usability (Source: L3 slide 9).

**The same capability can generate both an FR and NFRs.** FoC's errand flow shows this: F7.1 ("a student should only be matched to one outstanding errand, and any race condition in reassignment should be shown and rejected") is functional — a *race condition* being two overlapping attempts (say, two reassignments at the same instant) whose outcome would depend on timing rather than on the rules; its sibling NFR ("publishing an errand, replacing a courier, recording pickup, holding or releasing credits, completing delivery and sending notifications shall never become inconsistent when services restart, messages arrive late or operations are retried") constrains how well that behavior must hold (Source: L4-AlternativeExamplesForProductBacklog, order service F7.1 and NFR).

<box type="info" seamless>

**Telling apart — FR vs NFR.** One distinguishing question: **does the sentence state something the system *does*, or a bound on *how well / under what constraints* it does it?** The se-book's split — "functional requirements specify what the system should do; non-functional requirements specify the constraints under which the system is developed and operated" — comes with the performance example "the system should respond within two seconds." A pair to test the question on: "The system should allow a user to search for a book by its title" (what it does → FR) vs "The search should return results within two seconds" (how well → NFR).

Two traps the definitions don't warn you about:

| Trap | Example from the course | Why it bites |
|---|---|---|
| **Topic ≠ type.** A security-flavored sentence can still be an FR | "FoC should only store hashed email address in the database" (L3 slide 8) — an **F**-numbered backlog row | It specifies a *behavior* of the user service; the security *concern* doesn't make it an NFR |
| **The same subject changes type with the verb.** | "The system validates passwords" (FR — a behavior) vs "Password checks must complete in under 100 ms" (NFR — a bound on that behavior) | What gets constrained decides the class, not the subject matter |

Test each sentence against the se-book wording: FR = "what the system should do"; NFR = "the constraints under which the system is developed and operated" — and remember the W3.2 rule that only measurable NFRs can be verified.

</box>

{% call example("L3 slide 9 — one airline, one FR, one NFR") %}
FR: "The passenger shall be able to print boarding passes for all flight segments for which she has checked in" — a behavior the system must offer. NFR: "Mean time between failure >= 9000 hrs" — a constraint on how reliably the system runs, with no single feature attached (Source: L3 slide 9).
{% endcall %}

<panel type="seamless" minimized header="%%Common question — why does the boarding-pass FR insist on *all* flight segments?%%">

The lecturer walked the multi-leg case: flying from Singapore to a far-off destination with two transits means three flights — and an airline cannot check you in for the first leg and "not care what happens in between." Processing the check-in "should be reliable, meaning all segments should be included at minimum", so once you check in you know you are safe to travel to your destination without worrying about the middle legs (L3 recording, ~[43:00]). One sentence of FR text, one reliability expectation behind it — the two requirement classes travel together.

</panel>

**Write NFRs in measurable terms where possible.** A testable NFR lets the requirement be verified or tested objectively — Quiz 1 makes exactly this point: NFRs are stated in measurable terms "to allow the requirement to be verified or tested objectively" (Quiz 1 Q5, model answer). FoC's NFRs do this: "Support an initial capacity of up to 30000 registered users", "Response time for all page loads should take no more than 2 seconds", "A student profile will be disabled after 3 failed password or OTP attempts" (Source: Tutorial 2 appendix N1.1, N2.1.1; L4-AlternativeExamplesForProductBacklog N2.2.1).

<panel type="seamless" minimized header="%%Common question — can a requirement be dropped because it cannot be tested?%%">

Yes — a requirement no one can verify cannot be accepted or enforced, so it does not belong in the set. The lecturer applied this while scoping the course project: courier GPS location tracking was declared out of scope with the reasoning "I cannot test this … cannot test [it] means no point trying to force you to do it" (L3 recording, ~[15:00]). The same logic underlies the measurable-NFR rule above: if you cannot state the test, you cannot state the requirement.

</panel>

<box type="warning" seamless>

**Pitfall / trade-off:** NFRs are easier to miss because stakeholders think of features first — and a web application that is too slow or insecure fails even with all the right functionality. Mine for NFRs deliberately: Tutorial 2 Task 2.2 has you probe for "hidden information such as pain points, constraints, and exceptions that will lead to NFRs".
</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** Classify each FoC requirement as FR or NFR: (a) "The system loads bonus credits into every account after university email verification"; (b) "Only useful information should be collected and old activity data should be removed when no longer required"; (c) "An errand should be frozen for 10 minutes when a courier opens the replacement screen".

<panel type="seamless" minimized header="%%Answer%%">

(a) FR — a behavior the credit service performs. (b) NFR — privacy/data constraint (user service N2.1.2), not a feature. (c) FR — defined behavior of the order service's replacement flow (Source: L4-AlternativeExamplesForProductBacklog, credit service 5.1; user service N2.1.2; order service F7.2).

</panel>

**Q2.** (From Quiz 1 Q9.) Which of these are written in a usage-centric manner: (I) "As a user, I can upload images to the portal for others to view"; (II) "The portal will only support JPEG images of max 5MB"; (III) "A unique public link will be given to users to share their uploaded images"; (IV) "The portal shall store all images in a secure cloud service"; (V) "As a user, I can edit or delete my uploaded images at any time"?

<panel type="seamless" minimized header="%%Answer%%">

I, III, and V — they state the capability from the user's point of view. II and IV are product-centric system statements (Quiz 1 Q9, model answer; see W3.3 for the two styles).

</panel>

</panel>

</panel>

<span id="W3-c3"></span>


<panel type="seamless" expanded>
  <span slot="header" class="card-title"><markdown>### W3.3 Specifying requirements: usage-centric vs product-centric, and the product backlog ★★</markdown></span>


**There are two legitimate ways to state the same capability — and the product backlog is where both live, organized for planning.** Choose the view per requirement deliberately.

**Usage-centric requirements state the capability from the user's point of view.** "As a user, I can upload an image into the system so that I can showcase my photography skills to the world"; "As a user, I can upload a 20 mb image file into the system so that I can retain the original image without loss of quality" (Source: L3 slide 6).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-03.md#def-usage-centric-requirement" trim />
</box>

**Product-centric requirements state what the system will do.** "The system will support a range of graphic file formats up to 20 mb in size", refined to "The system will support the following file formats: jpeg, png, tiff, bmp" and "The system will support a maximum resolution of 5184 × 3888 pixels" (Source: L3 slide 6).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-03.md#def-product-centric-requirement" trim />
</box>

**Translate a usage-centric need by asking "what should I develop?" — not "what does the user want?"** User stories are deliberately vague about implementation — "don't talk about user interfaces … talk about how you want to use it, not what button to press" — so specification re-asks the question from the developer's side (L3 recording, ~[27:00]).

{% call example("The lecturer's trampoline analogy") %}
"A user wants to jump around — what should you develop? A trampoline." Likewise, "a user wants to see email by date — what should you develop? The capability to filter by date": provide a filter or a sort mechanism, whichever is more effective (L3 recording, ~[34:00]).
{% endcall %}

<box type="warning" seamless>

**Pitfall / trade-off:** "The user can do X" is still usage-centric. The lecturer flags this as a common student mistake in backlog exercises: renaming the user story to "the user can view suppliers" only swaps the grammatical subject — the product-centric move is to ask "if the user can do that, what should the *system* provide?" and answer from the system's side (L3 recording, ~[34:00]).

</box>

**Refinement goes at least two levels, from capability to testable rule.** FoC's user management does this in public: F1 "FoC should allow user to register using email/password" refines to F1.1 "FoC should validate email and password", which refines to "Password should be validated based on rules such as it should contain upper and lower case letters and numbers, minimum length, avoid dictionary attack etc.," %%— a dictionary attack being an attempt to get in by trying common words and known passwords, which is exactly what the length and character-mix rules make harder%% — and F2 "FoC should store user information securely" refines to "Password should be salted hashed using SHA256 or equivalent algorithm" and "FoC should only store hashed email address in the database" (Source: L3 slide 8 %%— dimmed: a salted hash stores the password only after mixing in a random value (the salt) and applying a one-way hash function such as SHA-256, so equal passwords never produce equal stored results and the original password cannot be recovered%%).

{% call example("L3 slide 8 — a second user story refined: update personal particulars") %}
"As a user, I can update my personal particulars in FoC" refines into rows the deck spells out: "FoC should authenticate the user before updating particulars" → "FoC should ask user for password and OTP to authenticate"; "New email provided should be confirmed using OTP based mechanism"; "FoC should allow selecting an image from the system for profile picture". The lecture's walkthrough supplies the *why*: changing your date of birth in a banking system demands proof that it is really you — so an update flow re-authenticates (password plus OTP), then validates the changed data with the same OTP mechanism registration used. "One user story got translated to so many things" that you can pick a single row and write its code (Source: L3 slide 8; L3 recording, ~[40:00]).
{% endcall %}

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-03.md#def-requirement-refinement" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-03.md#def-product-backlog" trim />
</box>

**Why a backlog?** It allows work allocation, developing test specifications, and design development — and unlike a traditional software requirements specification (SRS — W3.7 documents it among the textual requirement documents), which "only records what is to be done in the project", the product backlog "tells a team what needs to be done and can be used as a planning tool for sequencing the work" (Source: L3 slides 7, 29).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-03.md#def-software-requirements-specification" trim />
</box>

**The deck frames the SRS as the archaic alternative the backlog replaces.** The lecturer's gloss: an SRS is "a big fat document" that mixes in design decisions and which team implements what — a static artifact you develop once, sign off, and rarely update, which "doesn't suit many modern applications"; the backlog stays live and sequenced instead (L3 recording, ~[35:00]; L3 slide 29).

**Every backlog row carries traceability fields.** In FoC: type (FR/NFR), identifier (F1, F1.1, F1.1.1, F2 … N1, N1.1 …), description (the documented requirement), priority (H/M/L or 1/2/3), and sprint ID (the planned sprint/iteration); requirements should also be traced to use-case, design-document, code-module, and test-case references (Source: L3 slide 26).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-03.md#def-requirement-traceability" trim />
</box>

<panel type="seamless" minimized header="%%How should traceability reach the code?%%">

The lecturer's recommended practice: identify the functional requirements, keep each pull request small enough to satisfy specific requirements, and tag it with the requirement's identifier. He contrasted it with two real past reports: one dumped pull requests with no one-to-one correspondence to requirements — just "a dump of PRs" a reader must reverse-engineer — and a better one linking the requirement "system allows users to create an account using first name, last name, username, email, password" to PR24, which he rated only "somewhat traceable" because the PR still bundles admin routes and feedback messages. He also ranked the identifier as the most important traceability field: "who did what — you need to know who, you need to know what; both of them need an identifier" (L3 recording, ~[89:00]–~[92:00]).

</panel>

{% call example("Tutorial 2 appendix — the errand platform's backlog rows, quoted") %}
The tutorial's appendix shows the granularity expected for the project (FoC): "F1: Support user account creation" (High, sprint 1) → "F1.1: New users can create an account using their username, email and password" → "F1.1.1: The system should ensure that the account being created has a unique username and email to prevent duplicates"; "F2: Support viewing suppliers" → "F2.1: The system should display the suppliers with name and category visible when the user is logged in" (High, sprint 1) → "F2.1.1: The system should display the supplier details, such as descriptions, opening hours, etc., when the user selects a supplier" (Medium, sprint 1); "F3: Support managing orders" → "F3.1: FoC should allow creating an errand request" (High, sprint 2) → "F3.1.1: FoC should check if there are sufficient credits in the user's wallet to create an errand" (Medium, sprint 2); "F4: Support a closed credit economy on the platform" → "F4.1: The system should assign users with X number of credits when they first sign up" (High, sprint 3). NFRs follow the same pattern: "N1: Performance - Capacity" → "N1.1: Support an initial capacity of up to 30000 registered users" → "N1.1.1: Support data capacity increase up to 10x the initial planned user base" (Medium, sprint 1); "N2: Performance - Responsiveness" → "N2.1: FoC should have a responsive UI" → "N2.1.1: Response time for all page loads should take no more than 2 seconds" (Medium, sprint 1). The appendix also notes that "F2.1: Users can view supplier name and category when logged in" (usage-centric) and "F2.1: The system should display the supplier name and category when logged in" (product-centric) name the same capability — the product-centric wording defines the desired behavior better (Source: Tutorial 2 appendix). %%The appendix's own typos (e.g., "inital") are silently corrected in quotes above.%%
{% endcall %}

<box type="warning" seamless>

**Pitfall / trade-off:** Usage-centric wording is easy to write and easy to get wrong — "users can access supplier details" does not say what the system must show. Tutorial 2's appendix marks the product-centric restatement as the better specification of desired behaviour; use usage-centric statements to capture the need, then refine them into product-centric, testable rows (Source: Tutorial 2 appendix notes on F2.1 and F2.1.1).
</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** Rewrite this usage-centric requirement product-centrically, two levels deep: "As a courier, I can accept an errand so that I can earn credits."

<panel type="seamless" minimized header="%%Answer%%">

Sample answer (Tutorial 2 pattern): F: "Support accepting errands by couriers" → F.x: "The system should allow a logged-in courier to accept an errand that is waiting for a courier" → F.x.y: "The system should reject the accept request with an error code if the user is not an allowed courier" — mirroring the deck's trust rule F2.1 (Source: Tutorial 2 appendix F2; L4-AlternativeExamplesForProductBacklog, user service F2.1).

</panel>

**Q2.** Why does "F2.1: Users can view supplier name and category when logged in" need refinement before it can drive a test?

<panel type="seamless" minimized header="%%Answer%%">

It does not say what the system displays, where, or under which conditions — the product-centric refinement ("the system should display the suppliers with name and category visible when the user is logged in") makes the observable result explicit, which is what makes it testable (Source: Tutorial 2 appendix note on F2.1).

</panel>

**Q3.** A teammate writes in the backlog: "Users can register on FoC using email and password." Why is stopping there a mistake, and what is the product-centric rewrite?

<panel type="seamless" minimized header="%%Answer%%">

It restates the user story from the user's side — the "the user can do X" trap. The product-centric question is "what should the system provide?", answered by "FoC should allow users to register using email and password", which then refines into validation rows (F1.1) and secure-storage rows (F2) (Source: L3 slide 8; L3 recording, ~[37:00]).

</panel>

</panel>

</panel>

<span id="W3-c4"></span>


<panel type="seamless" expanded>
  <span slot="header" class="card-title"><markdown>### W3.4 Quality attributes: external vs internal ★</markdown></span>


**Quality attributes are how NFRs get named, measured, and traded — and the external/internal split decides who feels them.**

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-03.md#def-quality-attribute" trim />
</box>

**A combination of quality attributes defines software quality, and they are usually non-functional requirements.** The deck's taxonomy includes availability, performance, efficiency, scalability, robustness, safety, security, reliability, integrity, verifiability, deployability, compatibility, installability, portability, maintainability, usability, testability, modifiability, reusability, and interoperability (Source: L3 slide 10).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-03.md#def-availability" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-03.md#def-safety" trim />
</box>

**External attributes are observed when the software executes and shape the user's perception of quality.** Internal attributes are not directly observed during execution — developers and maintainers perceive them, and they encompass design aspects that may impact external attributes (Source: L3 slide 11).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-03.md#def-external-quality-attribute" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-03.md#def-internal-quality-attribute" trim />
</box>

<box type="info" seamless>

**Telling apart — external vs internal attribute.** One distinguishing question: **who can observe it — the user while the software runs, or the team by looking at the design and artifacts?**

| | External | Internal |
|---|---|---|
| Observable by | Users, while the software executes | Developers/maintainers, from the design and code |
| Felt as | The user's perception of quality | Nothing directly — it surfaces through the external attributes it enables |
| Course example | 2-second page loads (Tutorial 2 appendix N2.1.1); profile lockout after 3 failed attempts (L4 user-service N2.2.1) | Salted-hashed password storage; testability of the wallet service |

The connection is the point: an internal attribute is a *design property that may impact an external one* — the hashing (internal) is what the account security users feel (external) is made of. When classifying, ask who observes the sentence as written; "the team inspects the design" marks it internal even when users eventually benefit.

</box>

<panel type="seamless" minimized header="%%Common question — is integrity external or internal? (asked in lecture)%%">

The deck's classification lists integrity as external, and a student pushed back: "the user doesn't know data is compromised until you tell them." The lecturer's verdict: it is a *gray area that can be both* — corrupted data on a user-facing page is observed immediately (you get garbled things instead of the page), while corruption sitting in account records only surfaces "when you query and you get gibberish instead of the right valid ones" (L3 recording, ~[46:00], asked in lecture). Borderline cases exist; classify by who observes the sentence *as written*, and say which side you mean.

</panel>

{% call example("Efficiency is internal; the slowness users see is performance") %}
"You're using quicksort versus bubble sort — that's an efficiency matter. The user doesn't know whether you're using quicksort or bubble sort; the user only sees that the sorting takes a long time. That's basically performance" (L3 recording, ~[49:00], asked in lecture). The internal-to-external street runs one way: an inefficient algorithm for shifting through video frames (internal) degrades the streaming quality and lag the user sees (external) — "you need to be a bit careful about both; they are not mutually exclusive" (L3 recording, ~[50:00]).
{% endcall %}

{% call example("FoC — one attribute, two sides") %}
Scalability has an external side users feel ("the application must support the entire campus without slowing down" — order service NFR) and an internal side developers choose (run three Docker containers per microservice behind Nginx — a web server commonly used as the front proxy that spreads requests across replicas — and enable Kubernetes auto-scaling, an architecture decision made to deliver the external claim) (Source: L4-AlternativeExamplesForProductBacklog, order service NFR "Capacity").
{% endcall %}

**Different application types emphasize different attributes.** Embedded software: performance, efficiency, reliability, robustness, safety, security. Web applications: availability, integrity, interoperability, performance, scalability, security, usability. Desktop and mobile software: performance, security, usability (Source: L3 slide 13). The lecture's gloss on *why* web apps look like this: people move applications to the web so they are available "all the time" — or, more precisely, 99.999% of the time — and interoperable across desktop and phone (L3 recording, ~[60:00]).

**Deployment choices are quality-attribute decisions — and the lecture worked the mapping in detail.** The deck asks what attributes {{ term("blue-green deployment", "shifting traffic between two identical environments running different versions — near-zero downtime and easy rollback (defined in Week 1)") }} and Docker + Kubernetes support (Source: L3 slide 12; see W1.4–W1.5). The discussion first separated the rows: **blue-green is a deployment strategy, Docker + Kubernetes a deployment mechanism** — you can run blue-green without containers, and use containers for strategies other than blue-green (L3 recording, ~[52:00]). The class then mapped attributes to each (student answers, asked in lecture):

- **Availability — blue-green.** One environment serves users while the other is prepared; switching routes traffic to an already-running system, so requests keep going through (L3 recording, ~[54:00], asked in lecture).
- **Reliability — blue-green.** If the new version misbehaves, you switch back at once — from the user's point of view the service kept working (L3 recording, ~[56:00]).
- **Scalability — Docker + Kubernetes.** Kubernetes policies spawn extra nodes when load rises past a threshold and delete them when it falls: "scalability takes care of both sides, it's not just always expanding" (L3 recording, ~[58:00], asked in lecture).
- **Portability — Docker + Kubernetes.** A container runs on any system that runs the Docker engine — move it and it works (L3 recording, ~[59:00], asked in lecture).

<panel type="seamless" minimized header="%%Common question — doesn't blue-green also buy safety? Or verifiability? (asked in lecture)%%">

Two student proposals got corrected in the discussion:

- **"Safety?"** — no: *being bug-free is not necessarily safe*. Safety as a quality attribute is about harm to life or property — the lecture's example is a controller regulating wall pressure in a chemical plant, where bad software can let pressure build until the plant explodes. Blue-green deployment has no such physical stakes (L3 recording, ~[55:00], asked in lecture).
- **"Verifiability?"** — the reasoning offered (test one environment before switching, switch back on failure) actually describes *reliability* from the user's point of view. Verifiability is about how well you can test the system — work done before deployment (L3 recording, ~[56:00], asked in lecture).

</panel>

**Quality attributes can be satisfied without touching the code.** The lecturer's takeaway from the exercise: the application's code was finished — only the deployment changed — yet availability, reliability, scalability, and portability all moved. That is the requirements connection: the NFRs document the attributes the system must support, and the strategy or mechanism is then chosen to deliver them (L3 recording, ~[58:00]).

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** Classify as external or internal: (a) 2-second page loads; (b) salted-hashed password storage; (c) profile lockout after 3 failed attempts; (d) testability of the wallet service.

<panel type="seamless" minimized header="%%Answer%%">

External: (a) users feel response time; (c) users experience the lockout. Internal: (b) perceived by developers/maintainers (a design property that impacts the external security users feel); (d) perceived by the team, impacts how safely external behavior can be changed (Source: L3 slide 11; requirements from L4-AlternativeExamplesForProductBacklog N2.2.1 and Tutorial 2 appendix).

</panel>

**Q2.** A teammate claims "we use Docker + Kubernetes, so we are doing blue-green deployment." What is wrong with the claim, and which quality attribute does each actually buy?

<panel type="seamless" minimized header="%%Answer%%">

Blue-green is a deployment *strategy*; Docker + Kubernetes is a deployment *mechanism* — the two are independent (blue-green works without containers; containers serve other strategies too). Blue-green buys availability (an already-running environment takes traffic) and reliability (instant switch-back); container orchestration buys scalability (nodes added on load spikes, removed when load drops) and portability (containers run wherever the Docker engine runs) (L3 recording, ~[52:00]–~[59:00]).

</panel>

</panel>

</panel>

<span id="W3-c5"></span>


<panel type="seamless" expanded>
  <span slot="header" class="card-title"><markdown>### W3.5 Key quality attributes in depth ★★</markdown></span>


**Five attributes do most of the work in this course — security, performance, scalability, deployability, usability — and each has named concerns, measures, and design consequences.**

**Security is the system's ability to resist unauthorized use while still serving legitimate users.** Core concerns: confidentiality (protect data against unauthorized disclosure/access) and integrity (protect data against unauthorized modification); it relies on authentication, authorization, and auditing — who is the user, what are they allowed to do, and record actions so misuse can be detected or investigated (Source: L3 slide 14).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-03.md#def-security" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-03.md#def-confidentiality" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-03.md#def-integrity" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-03.md#def-authentication" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-03.md#def-authorization" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-03.md#def-auditing" trim />
</box>

{% call example("FoC — security requirements at three layers") %}
The user service's NFRs secure accounts:
- "A student profile will be disabled after 3 failed password or OTP attempts" (authentication), with re-enable "by clicking a verification link sent to the university email" (recovery)
- "Confidential account information in storage must be strongly protected" (confidentiality)
- "Only useful information should be collected and old activity data should be removed when no longer required" (privacy)

The user service's FRs add authorization: "Before a user edits a pickup place, withdraws an errand or marks delivery confirmed, the backend should verify that the user is allowed and return an error code otherwise", and the edge proxy — the entry-point service that fronts the platform's other services, from the FoC architecture in the example decks — "shall decode the JWT and answer with an error code when the credential is absent, expired or wrong" (a JWT — JSON Web Token — is a signed token that proves who the caller is; the proxy checks it before any request passes inward %%— dimmed: RFC 7519%%). The supplier service adds auditing-minded rules: "No confidential details should appear when a supplier request fails" and "Extra protection must be added to staff-only supplier URLs" (Source: L4-AlternativeExamplesForProductBacklog, user service F2, N2; supplier service NFR3).
{% endcall %}

**Security requirements come with working habits, not just definitions.** The lecture pressed three of them on the same slide:

- **Record them early in the product cycle** — not as an afterthought: the demo question "what happens if this user tries to delete that user's account?" should never be the first time the team has considered it (L3 recording, ~[68:00]).
- **Make them specific and testable** — "you can't say *make the system secure*. How do you verify? Put a lock? Doesn't work" (L3 recording, ~[68:00]).
- **Never argue "no money, no security"** — even the no-real-money course platform keeps its security requirements, because privacy remains: storing usernames and passwords in plain-text files is still unacceptable (L3 recording, ~[70:00]).

{% call example("A security requirement phrased to be verifiable") %}
"If the request is authenticated, then the data flow should be only through the HTTPS channel" — you can log the packets and check whether data appears unencrypted in plain HTTP; if it does, the requirement is violated (L3 recording, ~[68:00]). Contrast the unverifiable "make the system secure" (L3 recording, ~[70:00]).
{% endcall %}

<panel type="seamless" minimized header="%%Requirement questions per security mechanism%%">

The lecture turned each mechanism into questions a requirement should answer:

- **Authentication** — what is the preferred strategy for resolving forgotten passwords: an OTP, an emailed reset link, or security questions? And do critical transactions demand re-authentication — like a bank's push notification asking "we notice a transfer being made from the web; if this is you, press yes, otherwise contact the bank to lock your account" (L3 recording, ~[65:00]).
- **Auditing and logging** — what activity should be logged, and at what level of detail? ("Some user logged in" is potentially critical: if user A logged into user B's account, the log is where the investigation starts.) And who may access the logs — a bank will not hand your account logs to you; only certain people internally can investigate (L3 recording, ~[67:00]).

</panel>

**Performance is primarily responsiveness, and its requirements reach into architecture and hardware.** Low performance means unhappy users; in real-time systems it can impact safety (an overloaded system may miss critical alerts).
- Stringent query response times may demand replicated databases
- Latency requirements may lead to deploying caches
- Performance requirements affect the choice between {{ term("monolithic", "deployed as a single unit — Week 4 contrasts the monolith with decomposed styles like microservices") }} and microservice architectures, plus hardware and network choices

(Source: L3 slides 15–17)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-03.md#def-performance" trim />
</box>

{% call example("In real-time systems, performance failures become safety failures") %}
An autonomous car whose performance degrades does not just feel sluggish — the brake command that should fire within the next couple of processor cycles instead fires three to five seconds later, and "safety is compromised because of this" (L3 recording, ~[76:00]). In ordinary application development the stakes differ: performance reaches into the choice of architecture, design, and deployment instead (L3 recording, ~[77:00]).
{% endcall %}

**Performance is not one dimension — latency and throughput pull in different directions.** The lecture separated the two headline dimensions: **throughput is volume over time** — 10,000 transactions completed per minute — while **latency is the time to satisfy one request** — about a second normally, maybe ten in degraded mode (L3 recording, ~[74:00]).

<panel type="seamless" minimized header="%%What are latency and throughput? (defined in Weeks 9 and 12)%%">

<include src="../../se-book-adapted/common/defs-week-09.md#def-latency" trim />

<include src="../../se-book-adapted/common/defs-week-12.md#def-throughput" trim />

</panel>

<box type="info" seamless>

**Telling apart — latency vs throughput.** One distinguishing question: **are you measuring the wait for one request, or the work completed per unit time?**

| | Latency | Throughput |
|---|---|---|
| Measures | Time to satisfy one request | Volume of work over time |
| The lecture's numbers | ~1 s per transaction; ~10 s degraded | 10,000 transactions per minute |
| Application that prioritizes it | Gaming — if background graphics fail to load you keep playing, as long as the characters respond to input | Streaming — how many frames per second can be processed *is* the product |
| Deepened in | W9 (synchronous communication adds latency) | W12 (replication adds capacity) |

%%The numbers and the gaming/streaming pairing are the lecturer's (L3 recording, ~[74:00]–~[75:00]). Which dimension matters depends on the use case — the same NFR list can serve both a game and a stream; the weighting is the requirement (W3.6).%%

</box>

**Under overload, a system should fail gracefully — degrade, not die.** The lecture's phrase for designed degraded operation: "it's failing — don't die, fail gracefully, die slowly." Prefer the server that keeps working at reduced capacity over the one that simply stops answering (L3 recording, ~[72:00]).

{% call example("Degraded mode, with the lecturer's numbers") %}
A web server satisfies 10,000 requests per minute at peak. Something goes wrong. It can declare "I died — no more requests," or it can queue the incoming work and serve at reduced speed — 100 requests per minute, longer waits, but every request eventually satisfied. The degraded-but-alive option is the one to design for (L3 recording, ~[72:00]).
{% endcall %}

<panel type="seamless" minimized header="%%How does a performance requirement reach into architecture, design, deployment, and hardware?%%">

The lecture chained one requirement through all four layers:

- **Architecture** — a large data volume pushes toward a distributed application and a **sharded database**: split the data, e.g., names A–D in one database and E onward in another, so a query scans a small portion instead of the whole store. Netflix's multi-level caching — so a movie starts the moment you click — is the same layer's choice (L3 recording, ~[77:00]).
- **Design** — a cache must be accounted for up front: the query flow becomes "check the cache first; on a miss, go to the server, load the cache, then respond" (L3 recording, ~[78:00]).
- **Deployment** — Shopee's sale days bring a request spike, so the deployment enables Kubernetes + Docker auto-scaling: more requests, more instances (L3 recording, ~[79:00]).
- **Hardware** — a cache sitting on a 500 RPM hard disk, or behind a 1 Gbps link, is wasted money: the hardware must match the requirement (L3 recording, ~[79:00]).

</panel>

**Caching is the deck's worked performance technique.** Caching stores frequently accessed data closer to the user — high-speed, typically transient storage holding a subset of data (e.g., Amazon ElastiCache — AWS's managed cache service; Redis — an open-source, in-memory data store that answers reads far faster than a disk database and can double as fast lookup storage) (Source: L3 slide 18).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-03.md#def-caching" trim />
</box>

<mermaid>
flowchart LR
    U["Users"] --> APP["Application"] --> CACHE["Cache<br/>(frequently accessed subset)"]
    CACHE -->|"on miss: fetch & fill"| DB[("Data store")]
</mermaid>

%%Notation: boxes are components; the cylinder is a data store (the notation used across this book); the solid arrows are the request path, which reaches the data store only when the cache misses — a hit is answered from the cache alone.%%

How to read it for the running example: FoC's credit service keeps replay tags in Redis — markers that let the service recognize a wallet message it has already processed (W3.7's template example walks the full mechanism) — with the deck's rule "Redis shall save every tag after the balance update has finished", so the wallet check reads Redis (fast, hot) before touching the database, exactly the cache-in-front-of-store shape above (Source: L4-AlternativeExamplesForProductBacklog, credit service NFR6.1.2; L3 slide 18).

**Scalability is the ability to accommodate growth in usage — and it has both hardware and software consequences.** Growth can be more users, more deployment locations, more transactions. Hardware scaling adds disk capacity; software scaling may mean architecting for parallel and distributed computing. You cannot always future-proof, but an estimate of growth helps (Source: L3 slide 19).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-12.md#def-scalability" trim />
</box>

{% call example("FoC — planning for growth from pilot to campus") %}
Design FoC for 10,000 students as the pilot, deployed for SOC and CDE — then the platform goes NUS-wide: roughly 60,000 students, "six times more." The database must either be able to expand to that many rows for every service or be replaced by one that supports them: "either dynamically add capacity, or you relocate" (L3 recording, ~[80:00]). And the estimate has a horizon: you cannot future-proof for a hundred years — estimate the next ten, plan for them, then plan the following ten (L3 recording, ~[81:00]).
{% endcall %}

**Two scaling directions trade resilience against simplicity.** Vertical scaling adds capability to existing machines (upgrade and swap to a better configuration): easier to maintain, but a single point of failure. Horizontal scaling adds machines (nodes): more resilience and fault tolerance, but more cost and complexity — e.g., Kubernetes horizontal pod autoscaling, where Kubernetes (the container orchestrator of W1.4) watches the load and automatically adds or removes pods — its units of deployed containers, each running one of the service's replicas — to match demand. Microservices designed small, focused, and independently deployable suit horizontal scaling (Source: L3 slide 20). The lecture's software-scaling example: MapReduce-style distributed processing (Hadoop-class systems) — move the computation to where the data lives instead of pulling all the data to one node (L3 recording, ~[81:00]). FoC's capacity NFR makes the horizontal choice explicitly: "run three Docker containers for each microservice behind Nginx and enable Kubernetes auto-scaling" — three equivalent nodes behind a front proxy, consistent with the Kubernetes HPA example on the slide (Source: L4-AlternativeExamplesForProductBacklog, order service NFR). Week 12 redraws this same contrast on the room-booking platform and adds what scale-out needs to actually work — a load balancer and a session store (see [W12.4]({{baseUrl}}/se-book-adapted/chapters/week-12-scalability.html#W12-c4)). The lecture adds what horizontal scaling demands in return: **routing** — "you can't just say, oh, I have another pod, let's go" — incoming requests need a mechanism that decides where they go, and that is part of what makes the architecture harder (L3 recording, ~[84:00]).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-12.md#def-vertical-scaling" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-12.md#def-horizontal-scaling" trim />
</box>

<panel type="seamless" minimized header="%%What is container orchestration (Kubernetes)? (defined in Week 5)%%">

<include src="../../se-book-adapted/common/defs-week-05.md#def-container-orchestration" trim />

</panel>

<box type="info" seamless>

**Telling apart — requirement vs design decision.** One distinguishing question: **does the sentence pin down a *need the product must fulfill*, or a *choice about how to fulfill it*?**

| | Requirement | Design decision |
|---|---|---|
| States | A capability or bound the product must meet | A concrete way the system will be built to meet it |
| Passes the test | Survives a change of solution ("we could do this differently and still satisfy it") | Tied to a specific technology, component, or structure |
| FoC example | "The application must support the entire campus without slowing down" (order-service capacity NFR) | "Run three Docker containers for each microservice behind Nginx and enable Kubernetes auto-scaling" |

The FoC capacity pair shows how they travel together: the requirement is the *bound* (campus-scale load without slowdown); the container/proxy/auto-scaling split is the design *decision made to deliver it* — the chapter itself calls it "an architecture decision made to deliver the external claim" (W3.4) and "the stated design consequence" (self-check). Course requirement documents do record such decisions (the L3 service template even asks "what data does the service deal with", which invites them); the skill being tested is knowing which part is the *constraint* — so when a quiz asks you to *satisfy* a requirement, answer with the need it states, not the mechanism quoted alongside it.

</box>

**Deployability is the ease and speed of getting software to production.**

- Software may be allocated to an environment for execution within a predictable, acceptable amount of time and effort
- Measures include deployment frequency, change failure rate, and MTTR (mean time to repair)
- The processes and strategies that impact it are {{ term("CI/CD", "the automated build–test–release pipeline: continuous integration plus continuous delivery/deployment (Week 1)") }}, {{ term("containerization", "packaging an application with only the OS processes and dependencies it needs (Week 1)") }}, {{ term("DevOps", "practices combining development and operations to shorten commit-to-production at high quality (Week 1)") }}, and architectural decisions such as {{ term("serverless", "developers ship code; the provider provisions, scales, and manages the servers it runs on (Week 1)") }} and microservices

(Source: L3 slide 21 — all of which Week 1 covered as mechanisms)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-03.md#def-deployability" trim />
</box>

**Processes, not just products, satisfy quality attributes.** The lecture's remark on the slide's list: CI/CD and DevOps are "kind of a process way of doing" things — mechanisms that support deployability requirements. Evidence that a quality attribute can be delivered by *how the team works*, not only by what the system is (L3 recording, ~[85:00]).

**Usability measures the effort to prepare input, operate, and decipher output.** Measures include average time to specify inputs, number of interactions to get information, time to complete a task, user errors or trials needed, and waiting time; ease of learning (meaningful messages, verbose prompts, tooltips) and ease of use (customizations, autocompletion, autocorrection, scriptable) (Source: L3 slide 22).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-03.md#def-usability" trim />
</box>

**Usability requirements are counts and timings — and each error is a design lead.** Measuring "how many errors does the user make" is only half the job: ask *why* the errors happen — an over-complex interaction, badly placed icons — "so then you go fix those problems" (L3 recording, ~[85:00]).

{% call example("The lecturer's own unusable system") %}
Adding a student to a tutorial group in ModReg takes "at least eight to ten clicks": "is it usable? Definitely not, not by my definition" (L3 recording, ~[85:00]). The count of interactions is the measure; the number itself is the verdict.
{% endcall %}

**The course platform's "responsive UI" requirement is a usability requirement.** A responsive layout adjusts to the screen size and puts the most important content at the top; a non-responsive one forces scrolling and zooming and lets icons overlap (L3 recording, ~[86:00]).

{% call example("FoC — usability vs security, in one rule") %}
"A student profile will be disabled after 3 failed password or OTP attempts" is a security rule with a usability cost: a student who fat-fingers their password three times loses access until they click a verification link in their university email. The rule's balance (3 attempts; self-service recovery) is a usability decision as much as a security one (Source: L4-AlternativeExamplesForProductBacklog, user service N2.2.1–N2.2.2; L3 slides 14, 22).
{% endcall %}

<box type="warning" seamless>

**Pitfall / trade-off:** Attributes conflict by nature, not by bad luck — the next unit makes the conflicts explicit. When you write an NFR, ask what other attribute it silently taxes (Source: L3 slide 23).
</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** For each FoC requirement, name the attribute and one measure you would use: (a) "Response time for all page loads should take no more than 2 seconds"; (b) "The web browser shall generate the replay tag and place it in the Kafka message header" (Kafka — a distributed message streaming platform the course introduces properly in Week 10; here just read it as "the channel the wallet update travels on"); (c) "The application must support the entire campus without slowing down".

<panel type="seamless" minimized header="%%Answer%%">

(a) Performance — measure response time per page load against the 2-second bound. (b) Security/integrity — exactly-once wallet events: each wallet update takes effect once and only once, even if the same message arrives twice; measure duplicated wallet messages processed as errors (the replay-tag mechanism). (c) Scalability — measure users/transactions supported without breaching the SLO (SLO — service-level objective, the measurable target defined in W12.2; the deck writes SLOs, not SLAs); note the stated design consequence (3 containers per microservice, Kubernetes auto-scaling) (Source: Tutorial 2 appendix N2.1.1; L4-AlternativeExamplesForProductBacklog credit service NFR6.1.1 and order service NFR).

</panel>

**Q2.** Why can deployability be measured by deployment frequency, change failure rate, and MTTR — but not by "the system is easy to deploy"?

<panel type="seamless" minimized header="%%Answer%%">

Those three are observable quantities; "easy to deploy" is not. Measurable statements can be verified or tested objectively — the same principle Quiz 1 Q5 tests for NFRs (Source: L3 slide 21; Quiz 1 Q5).

</panel>

**Q3.** FoC's degraded mode serves 100 requests per minute instead of its usual 10,000, and each request now takes about 10 seconds instead of 1. Which performance dimensions changed, and what is this behavior called?

<panel type="seamless" minimized header="%%Answer%%">

Throughput dropped tenfold (work completed per minute); latency rose tenfold (wait per request). Serving slowly from a queue instead of refusing requests is failing gracefully — degraded-but-alive operation (L3 recording, ~[72:00]–~[74:00]).

</panel>

</panel>

</panel>

<span id="W3-c6"></span>


<panel type="seamless" expanded>
  <span slot="header" class="card-title"><markdown>### W3.6 Requirement trade-offs ★★</markdown></span>


**Improving one quality attribute often degrades another — so attribute selection is a prioritization problem, not a wish list.**

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-03.md#def-requirement-tradeoff" trim />
</box>

**Every quality attribute you improve is bought by paying somewhere else — architecture is the act of choosing where to pay.** The diagram shows the shape of that bargain: one design decision moves two quality attributes in opposite directions.

<mermaid>
flowchart TB
    subgraph SEESAW["One design decision, two quality attributes"]
        direction LR
        L["Improve<br/>scalability"] --- F["fulcrum:<br/>the design decision"] --- R["Cost & complexity<br/>degrade"]
    end
</mermaid>

%%Notation: the two pans are quality attributes pushed by one design decision (the fulcrum); the lower pan is the attribute that pays. The picture is a metaphor — read it as "this decision helps the left, hurts the right".%%

How to read it: with Quiz 3's room-booking platform, extracting the search module as an independently scaled microservice lifts *scalability* (the summer load is absorbed by more search instances) but pays in *cost and complexity* — more deployables, more moving parts — which is exactly why the quiz's correct answer ties the split to demand ("increase its instances based on demand", Quiz 3 Q1). L3's tables give you the vocabulary of the pans: an embedded system cares about performance and safety, a web app about performance, scalability and security (L3 slide 13) — and the seesaw reminds you that adding security checks also adds latency, so the architect must say *which* side they are choosing to load.

{% call example("Two requirements that cannot both win — memorable vs secure passwords") %}
"It should be easy for the user to remember the username and password" collides head-on with "the password should be secure": the security rules forbid dictionary terms and consecutive letters and demand a number beside a symbol — exactly the properties that make a password hard to remember. "There's no way you can satisfy all of them, so you need to reach a compromise" (L3 recording, ~[86:00]). The lecturer's aside: surfacing such conflicting requirements is precisely one of the things LLMs do well (L3 recording, ~[87:00]).
{% endcall %}

**Why trade-offs exist — two different pressures the slide keeps separate.** Project constraints (resource limits, few skilled engineers, budgets and time, technical limitations) force you to *prioritize* which attributes to fund — the slide's own conclusion (its "⇒" marker): this is a planning and resource-allocation problem. Attribute conflicts are the other pressure: improving one attribute can genuinely degrade another, which is what the slide's table records. The deck works from a sample prioritization table for an airport check-in kiosk (Figure 14-1 on L3 slide 23, offline with the slide PDFs): rows are attributes, each carries a priority **Score** (Security 7, Integrity 6, Usability 5 … Verifiability 1, Robustness 1), and the cell symbols give the direction of influence — a "plus" (drawn `^` in the figure) means improving the row attribute improves the column attribute; a "minus" (drawn `<`) means improving the row attribute degrades the column one (Source: L3 slide 23).

**The conflicts are directional, and Quiz 1 tests two of them.** Improving interoperability by allowing open data exchange and API access can expose the system to more vulnerabilities, weakening security; improving reliability by introducing redundant checks, backups, and recovery routines makes the system slower and more resource-hungry, degrading efficiency (Quiz 1 Q7, model answer; Source: L3 slide 23).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-03.md#def-reliability" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-03.md#def-interoperability" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-03.md#def-efficiency" trim />
</box>

{% call example("L3 slide 24 — the same four NFRs, two very different systems") %}
The healthcare examples pair two scenarios that both list performance, scalability, usability, and deployability as NFRs, yet weight them differently: an A&E (accident & emergency) bedside clinical decision support system that helps with patient triage — deciding which patients need treatment first — versus a national health-record platform for citizens' health data — both list the same four NFRs (performance, scalability, usability, deployability), and the slide's point is that the same list serves both because the weighting differs with the context: the bedside tool lives or dies on instant response ("thinking doesn't take time, talking takes time — no talking, only thinking: the patient is dying, you want to diagnose soon"), the national platform on serving huge populations dependably — so scalability leads there. %%The full slide (L3, offline) shows the two lists verbatim.%% The lesson: the attribute list is generic; the prioritization is what makes it a requirement (Source: L3 slide 24; quotes from L3 recording, ~[88:00]).
{% endcall %}

**Trade-off analysis needs a common language and structure.** Use quality models and frameworks that provide a common language and structure for describing, measuring, and comparing quality attributes — e.g., pair-wise prioritization; feasibility takes priority (Source: L3 slide 23).

**MoSCoW is the other framework the lecture named.** Where pair-wise forces an order by head-to-head comparison, MoSCoW sorts requirements into four labeled classes — including an explicit *will not have*, which makes the de-scoping visible to everyone (L3 recording, ~[87:00]).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-03.md#def-moscow-prioritization" trim />
</box>

**For FoC, pairwise prioritization identifies the nice-to-haves.** The deck asks: "You can use pair-wise prioritization to identify the Nice-to-haves in FoC" — comparing requirements two at a time to force an order, which is exactly what sprint planning needs (Source: L3 slide 25).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-03.md#def-pairwise-prioritization" trim />
</box>

<box type="warning" seamless>

**Pitfall / trade-off:** Feasibility takes priority — a required-but-infeasible attribute combination is a plan to fail. Tutorial 2 Task 1.1 has you prioritize and draft an execution plan precisely so these conflicts surface before development (Source: L3 slide 23; Tutorial 2 Task 1.1).
</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** (From Quiz 1 Q7.) Improving interoperability by allowing open data exchange and API access can expose the system to more vulnerabilities, weakening ___; improving ___ by introducing redundant checks, backups and recovery routines can make the system slower and consume more resources.

<panel type="seamless" minimized header="%%Answer%%">

Security; reliability (Quiz 1 Q7, model answer).

</panel>

**Q2.** FoC's lockout rule (disable after 3 failed attempts) trades which attribute against which? Name a mitigation the requirements already contain.

<panel type="seamless" minimized header="%%Answer%%">

Security (protect accounts against unauthorized access) is bought at a usability cost (legitimate students locked out). The mitigation is already in the requirements: the profile "can be enabled again by clicking a verification link sent to the university email" — self-service recovery shortens the usability penalty (Source: L4-AlternativeExamplesForProductBacklog, user service N2.2.1–N2.2.2).

</panel>

**Q3.** In one sentence each: what does pair-wise prioritization ask, and what does MoSCoW decide?

<panel type="seamless" minimized header="%%Answer%%">

Pair-wise asks, for every pair, "if we could fund only one of these two, which one?" — then tallies the wins (1 point per favored comparison, 0.5 per indifference, 0 per loss). MoSCoW assigns each requirement a class — must, should, could, or will not have — making the exclusions explicit rather than merely ranked (L3 slides 23, 25; L3 recording, ~[87:00]–~[89:00]).

</panel>

</panel>

</panel>

<span id="W3-c7"></span>


<panel type="seamless" expanded>
  <span slot="header" class="card-title"><markdown>### W3.7 Validating, documenting and managing requirements ★★</markdown></span>


**Requirements are managed artifacts: they are verified for quality, recorded in documents, traced to work items, and revised as the product learns.**

**Validation and verification ask different questions.** Validation: whether you have written the *right* requirements — do they trace back to business objectives? Verification: whether you have written the requirements *right* — do they have the desirable properties: completeness, correctness, feasibility, prioritization, unambiguity? Methods: informal — a peer desk-check (one colleague reviews the work at their own desk), a pass-around (copies circulate to several reviewers in turn), or a walkthrough (the author steps a group through the requirements) — and formal (inspection: a defined, role-assigned process run from a checklist) (Source: L3 slide 28).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-03.md#def-requirement-verification" trim />
</box>

**The unambiguity property fails quietly — the lecture's cautionary tale.** "A user can log in with username or OAuth" looks acceptable, yet when the lecturer asked what had actually been implemented, one developer answered "our system uses username and password" and another said "GitHub login" — and because none of them had written the code themselves (AI had), the ambiguity was never forced into the open (L3 recording, ~[95:00]). A requirement each reader can interpret differently is not one requirement but two.

**Requirement documents come in textual and visual forms.** Textual: vision and scope document, use case document, software requirements specification (SRS), product backlog. Visual: structured analysis models — a data flow diagram (how data moves through the system's processes), an entity-relationship diagram (the entities in stored data and how they relate), a state-transition diagram (the states a thing moves through and the events that move it), and a dialog map (a state-transition diagram drawn over the user-interface dialogs, showing which screens can follow which %%— dimmed: Wiegers & Beatty, *Software Requirements*%%) — and object-oriented analysis models (e.g., object-oriented domain models — conceptual models of the problem-domain's things, their properties, and relations; for FoC: students, errands, wallets, vendors. Week 8 develops this idea as domain-driven design) (Source: L3 slide 29).

**A template keeps service requirements complete.** The deck's microservice template asks three questions of every service: what can the system/service do (functionality), how well should the service perform (NFRs), and what data does the service deal with — customizable (e.g., add more NFRs) (Source: L3 slides 30–31).

{% call example("The template applied to FoC's credit service") %}
**What it can do:**

- Load bonus credits after university email verification
- Accept reward changes while an errand waits for a courier
- Charge the difference when the reward increases
- Transfer charged credits to the courier on delivery confirmation
- Refund held credits when an errand is removed, abandoned, or missed

**How well it performs:** exactly-once wallet events — every wallet-changing message carries a replay tag, duplicates are acknowledged without updating balances.

**What data:** wallet balances, replay tags (stored in Redis), credit ledger entries — the ledger being the running record of every credit movement (loaded, charged, transferred, refunded)

(Source: L4-AlternativeExamplesForProductBacklog, credit service 5.1–5.5, NFR6; template from L3 slide 30)
{% endcall %}

**Requirements management is a loop, not a phase.**

1. Collect initial requirements from stakeholders
2. Analyze
3. Define and record
4. Prioritize
5. Agree on and approve
6. Trace requirements to work items
7. Query stakeholders after implementation on needed changes
8. Utilize test management to verify and validate
9. Assess the impact of changes
10. Revise
11. Document changes

Tools range from spreadsheets to GitHub, Jira, and dedicated requirements-management platforms — JAMA and IBM's RequisitePro %%— dimmed: products named on L3 slide 32%% (Source: L3 slide 32).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-03.md#def-requirements-management" trim />
</box>

**Requirements are not set in stone — "those days are gone."** The management loop exists because requirements change. The lecture's realistic caveat: under deadline heat, teams skip the writing-down steps and just implement — tolerable under student constraints, but the full discipline is what industry certification and government contracts demand (L3 recording, ~[94:00]).

**AI now assists requirements engineering — with the same caveat as Week 2.** Uses:

- Elicitation — persona specification (acting as a domain expert or user — the lecture's mechanics: "you say this is the persona, this is the use case; now you act like someone, I ask you questions, you answer") and contextual information (questions relevant to the product context)
- Analysis — requirement refinement (identify sub-tasks/sub-features) and automated templating and tagging (the lecture's version: specify a grammar or rough structure, and the LLM produces requirements in the right format)
- Automated tagging and categorization by type and priority (better traceability, e.g., automated tracing of tests to requirements)
- Natural language processing — identify ambiguity, conflicting requirements; fill missing requirements; fix inconsistencies
- Predictive analytics — which requirements are likely to be implemented successfully (helping identify and prioritize)

The lecture's closing advice on all of these uses: *use but verify*. LLMs are effective at conflict and completeness checking — "quite effective actually" — but outputs are non-deterministic: the same question may not get the same answer the second time, and growing robustness has not removed that possibility, so "don't simply trust it like a black box" (L3 recording, ~[95:00]; Source: L3 slides 33–34; Tutorial 2 Task 2.2 rehearses the elicitation use).

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** Your reviewer marks FoC's "The system should display the suppliers with name and category visible when the user is logged in" as "clear". Which verification property does the refined child requirement "The system should display the supplier details, such as descriptions, opening hours, etc., when the user selects a supplier" add?

<panel type="seamless" minimized header="%%Answer%%">

Completeness (it says what details, and when) and testability — the observable result is explicit, so a test can settle whether it is met (Source: Tutorial 2 appendix F2.1.1; L3 slide 28).

</panel>

**Q2.** Tutorial 2 Task 2.2 has you elicit ClassPulse requirements from an LLM by probing with personas and "what if" scenarios. Which AI-in-RE use does this rehearse, and what is the deck's caveat?

<panel type="seamless" minimized header="%%Answer%%">

Elicitation — persona specification (the deck: the LLM acts "as a domain expert or user"; for ClassPulse, an instructor persona) and contextual information (questions relevant to the product context). Caveat: don't simply trust the black box — outputs are non-deterministic and the chain of thought is not explainable (Source: L3 slides 33–34; Tutorial 2 Task 2.2).

</panel>

</panel>

<box type="info" seamless>

**Section summary**

* **Requirements development loops through elicitation, analysis, specification, and validation** (W3.1).
* **FRs say what the system does; NFRs say how well — and NFRs must be measurable to be verifiable** (W3.2).
* **The product backlog organizes requirements into traced, prioritized, sprint-planned rows** (W3.3).
* **Quality attributes split external (user-felt) from internal (design-perceived), and five attributes carry most of the weight** (W3.4–W3.5).
* **Attributes trade off against each other; feasibility takes priority** (W3.6).
* **Requirements are validated, documented, traced, and managed — increasingly with AI assistance, never with blind trust** (W3.7).

</box>

</panel>

## Connections

* Requirements development, FR/NFR, usage/product-centric ↔ L3 slides 3–9 ↔ Tutorial 1 Q1 (characterize an application) ↔ Quiz 1 Q5, Q9.
* Product backlog and refinement ↔ L3 slides 6–8, 26 ↔ L1 slide 24 (PeerPrep, W1.3) ↔ Tutorial 2 Task 1.1 (the errand platform's own backlog) ↔ Scrum's sprint planning (W1.3).
* Quality attributes ↔ L3 slides 10–22 ↔ W1.4–W1.5 (deployment mechanisms and strategies as attribute decisions) ↔ W12 (scalability deep dive).
* Trade-offs ↔ L3 slides 23–25 ↔ Quiz 1 Q7 ↔ the prioritization step of Tutorial 2 Task 1.1.
* Validation, documentation, management, AI in RE ↔ L3 slides 28–34 ↔ W2.2 (AI across the SDLC) ↔ Tutorial 2 Task 2.2 (LLM-assisted elicitation for ClassPulse).

## Further reading

All cited on the slides: the IEEE Standard Glossary definition of requirements; Wiegers & Beatty, *Software Requirements* (source of the validation/verification and quality-of-requirements lists); Chris Richardson's microservice requirement template (microservices.io); IBM's requirements-management overview; Ronanki et al. and Arora et al. on generative AI in requirements engineering.

## Summary

**Key takeaways**

* **Requirements are conditions or capabilities — developed in a loop, not gathered once.** (→ outcome 1)
* **FRs specify behavior; NFRs specify how well, and only measurable NFRs can be verified.** (→ outcome 2)
* **A product backlog turns requirements into a traced, prioritized, sprint-planned plan.** (→ outcome 3)
* **Quality attributes are named, measurable properties — external ones are user-felt, internal ones are design-perceived.** (→ outcome 4)
* **Security, performance, scalability, deployability, and usability each carry named concerns, measures, and design consequences.** (→ outcome 4)
* **Attributes trade off; prioritization under constraints is the engineering act.** (→ outcome 5)
* **Requirements are validated, documented, traced, and managed — increasingly with AI assistance, never with blind trust.** (→ outcome 1)

**Key terms**

| Term | One-line definition | Unit |
|---|---|---|
| Requirement | A condition or capability needed by a user or that must be met by a system — or its documented representation | [W3.1](#W3-c1) |
| Elicitation | Discovering requirements — interview, workshop, document analysis, prototyping | [W3.1](#W3-c1) |
| Requirements analysis | Analyze, decompose, derive, negotiate; identify gaps | [W3.1](#W3-c1) |
| Specification | Writing and illustrating requirements for comprehension, review, and use | [W3.1](#W3-c1) |
| Requirements validation | Confirming the correct set of requirements that enables developers to build a solution | [W3.1](#W3-c1) |
| Event-response table | Elicitation source listing external stimuli against the system's responses | [W3.1](#W3-c1) |
| Functional requirement | Specifies something the system should do | [W3.2](#W3-c2) |
| Non-functional requirement | A constraint on how well the system works, not directly tied to functionality | [W3.2](#W3-c2) |
| Product backlog | The ordered list of requirements with type, id, description, priority, and planned sprint | [W3.3](#W3-c3) |
| Usage-centric requirement | States the capability from the user's point of view ("As a user, I can…") | [W3.3](#W3-c3) |
| Product-centric requirement | States what the system will do, refined into testable system statements | [W3.3](#W3-c3) |
| Requirement refinement | Decomposing a requirement at least two levels, from capability to testable rule | [W3.3](#W3-c3) |
| SRS | Traditional document that only records what is to be done — not a sequencing tool like the backlog | [W3.3](#W3-c3) |
| Requirement traceability | Type, id, description, priority, sprint — traced to use-case, design, code, and test references | [W3.3](#W3-c3) |
| Quality attribute | A property (performance, security, usability…) whose combination defines software quality | [W3.4](#W3-c4) |
| External quality attribute | Observed while the software executes; shapes the user's perception of quality | [W3.4](#W3-c4) |
| Internal quality attribute | Not directly observed in execution; perceived by developers, impacts external attributes | [W3.4](#W3-c4) |
| Safety | Not causing harm to life or property — bug-free is not the same as safe | [W3.4](#W3-c4) |
| Security | Resisting unauthorized use while serving legitimate users — confidentiality, integrity, authentication, authorization, auditing | [W3.5](#W3-c5) |
| Confidentiality | Protecting data against unauthorized disclosure or access | [W3.5](#W3-c5) |
| Integrity | Protecting data against unauthorized modification | [W3.5](#W3-c5) |
| Authentication | Establishing who the user is | [W3.5](#W3-c5) |
| Authorization | Deciding what the user is allowed to do | [W3.5](#W3-c5) |
| Auditing | Recording actions so misuse can be detected or investigated | [W3.5](#W3-c5) |
| Performance | Responsiveness of the system; drives architecture, hardware, and network choices | [W3.5](#W3-c5) |
| Caching | Storing frequently accessed data closer to the user — high-speed, transient (Redis, ElastiCache) | [W3.5](#W3-c5) |
| Scalability | Handling growth in work by adding resources while response stays stable (deep-dived in Week 12) | [W3.5](#W3-c5) |
| Vertical scaling | Adding capability to existing machines — easier to maintain, single point of failure | [W3.5](#W3-c5) |
| Horizontal scaling | Adding machines (nodes) — resilient and fault-tolerant, more cost and complexity | [W3.5](#W3-c5) |
| Deployability | Ease and speed of getting software to production — deployment frequency, change failure rate, MTTR | [W3.5](#W3-c5) |
| Usability | Effort to prepare input, operate, and decipher output; ease of learning and of use | [W3.5](#W3-c5) |
| Requirement trade-off | Improving one quality attribute degrades another | [W3.6](#W3-c6) |
| Reliability | Keeping working correctly; redundancy buys it at efficiency's expense | [W3.6](#W3-c6) |
| Interoperability | Working with other systems; open exchange exposes more attack surface | [W3.6](#W3-c6) |
| Efficiency | How well the system uses resources — what reliability's redundancy taxes | [W3.6](#W3-c6) |
| Pair-wise prioritization | Comparing requirements two at a time to force an order; feasibility takes priority | [W3.6](#W3-c6) |
| MoSCoW prioritization | Sorting requirements into must / should / could / will not have — exclusions made explicit | [W3.6](#W3-c6) |
| Requirements verification | Written the requirements right? Completeness, correctness, feasibility, prioritization, unambiguity | [W3.7](#W3-c7) |
| Requirements management | The collect → analyze → record → prioritize → trace → revise loop, tool-supported | [W3.7](#W3-c7) |

%%Next: Week 4 moves up a level of abstraction — architecture: once you know *what* to build and *how well*, architecture decides the system's overall structure that delivers it.%%

</div>
