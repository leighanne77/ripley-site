# Terms used

Vocabulary running across the Ripley site, the EGON pages, and the USACE decks.
Grouped by where it comes from, because the audiences differ: a district engineer
knows section 2 cold and may not care about section 6; an investor is the reverse.

Entries marked **[verify]** are ones to confirm before saying out loud to USACE.

---

## 1 · EGON product vocabulary

| Term | Means |
|---|---|
| **Decision support** | The system produces options and evidence; a human decides. Load-bearing distinction for USACE — "decision support, not decision making." |
| **Download-only** | EGON exports a payload. It has no interface into the customer's models and writes nothing back. |
| **Deterministic core** | The only component allowed to author a figure. Language models draft and discover; the core writes. The trust path contains no LLM. |
| **Validation gate / fails closed** | A figure without a source and a reproducible calculation cannot render at all. Structural property, not a policy. |
| **Click-to-source** | Every exported figure carries its citation, formula, model reference and sensitivity. |
| **Data contracts** | Enforced agreements on shape and origin of incoming data; sources are named before anything is computed. |
| **Escrowed refresh** | Automated data pull with a time-date stamp; staleness gated red/green with no human in the loop. |
| **Rejection log** | The record of what was screened out and why — "what we did NOT use." Doubles as the anti-opposition asset in public review. |
| **Measure catalogue** | The full set of candidate resilience measures for a site — gray, nature-based and hybrid. |
| **Both horizons** | Reporting the near-term hold *and* the long-term service life, not one or the other. |
| **Referee, not advocate** | EGON prices exposure and lets return choose the lever; it does not favour nature-based or gray. |

## 2 · USACE process and documents

| Term | Means |
|---|---|
| **PDT** | Project Delivery Team — the district team carrying a study. |
| **ATR** | Agency Technical Review — independent USACE review of a study product. |
| **FCSA** | Feasibility Cost Sharing Agreement — the instrument that starts a feasibility study clock. |
| **ADM** | Agency Decision Milestone — the decision point in a feasibility study. |
| **Vertical team** | District → division → HQ review chain. A common source of schedule slip. |
| **Section 404** | Clean Water Act permit for discharge of dredged or fill material into waters of the US. |
| **404(b)(1) / LEDPA** | The guidelines requiring the Least Environmentally Damaging Practicable Alternative. Testing a full array — nature-based included — is what this test asks for. |
| **NEPA** | National Environmental Policy Act — the environmental review statute. |
| **NWP 3 / NWP 27** | Nationwide Permits. 3 covers maintenance of previously authorised structures; 27 covers aquatic-ecosystem restoration and beneficial-use sediment. |
| **Class 5 estimate** | Widest-band conceptual cost estimate (AACE classification). USACE Class-5 cost engine = estimates built to USACE methods. |
| **CWCCIS** | Civil Works Construction Cost Index System — the escalation index, so cross-year figures are escalated rather than summed raw. |
| **EAD** | Expected Annual Damage — annualised expected loss. |
| **BCR** | Benefit-Cost Ratio. **Currently OPEN for EGON** — localisation and benefit transfer unresolved. Do not claim. |
| **MVN** | USACE New Orleans District (Mississippi Valley Division). Avondale's district. |
| **NAD / Baltimore District** | North Atlantic Division; Baltimore Harbor's district. |
| **MD-0011** | Project ID for the Baltimore Harbor Navigation Project. **[verify]** what the number indexes. |

## 3 · Hazard and coastal engineering

| Term | Means |
|---|---|
| **Stage-frequency** | The relationship between river stage and exceedance probability at a reach. Distinct from coastal sea level far upriver. |
| **RSL** | Relative sea level — eustatic rise plus local land motion. The Chesapeake runs well above the national average because subsidence compounds it. |
| **Subsidence** | Land sinking. Modifies every elevation rather than standing as a loss of its own. |
| **Shoaling** | Sediment accumulating in a channel. On a navigation project it is a scheduled operating cost, not a tail event. |
| **Back-door pathway** | Surge reaching an asset from behind rather than off the open water — the Barataria route in behind the West Bank at Avondale. |
| **Batture** | Louisiana term for the land between the river's low-water edge and the levee. |
| **Depth-damage curve** | Function mapping inundation depth to damage. Coastal industrial assets need one carrying wave and erosion; **no published USACE curve covers that case**. |
| **Design basis** | The condition an asset was built to withstand. The deck's core argument is that the loss window has moved inside the service-life window. |

## 4 · Models and data sources

| Term | Means |
|---|---|
| **HEC-RAS** | USACE river hydraulics model. A nature-based alternative in RAS is a terrain edit plus a Manning's *n* polygon — and RAS has no wave-attenuation-over-marsh/reef capability. |
| **HEC-FDA** | USACE flood damage reduction analysis model. |
| **ADCIRC / CSTORM** | Storm surge and wave modelling. |
| **Manning's *n*** | Channel roughness coefficient — how nature-based measures get represented in RAS. |
| **NACCS** | North Atlantic Coast Comprehensive Study (USACE, Jan 2015). 306 pages; 14 building prototypes across inundation, wave and erosion; states plainly that content-to-structure value ratios are not available. |
| **EGM** | USACE Economic Guidance Memoranda. Checked for a NACCS successor — none issued after 2015. |
| **Hazus** | FEMA loss estimation model. Rejected as a substitute on surge-and-wave assets: no wave or erosion mechanism. |
| **LOCA2 / STAR-ESDM** | Statistical downscaling for temperature and precipitation, bias-corrected to the observed record. Supports claims about trend, magnitude and tails — not a year-by-year lineup. |
| **SLOSH** | NOAA hurricane surge model. |
| **Atlas 14** | NOAA precipitation frequency atlas. |
| **NSI** | National Structure Inventory — structure-level exposure data. |
| **NNBF** | Natural and Nature-Based Features. USACE's own International Guidelines (2021) state benefit quantification is immature — which is why gray wins by default. |

## 5 · Resilience measures

| Term | Means |
|---|---|
| **Gray** | Hard engineered infrastructure — floodwalls, revetment, closure structures. |
| **NbS** | Nature-based solutions — marsh, reef, shoreline, buffer. |
| **Hybrid** | Combined gray and nature-based. |
| **Beneficial use** | Placing dredged material to build land rather than disposing of it. On a navigation project the sediment the mission already produces becomes the feedstock. |
| **Poplar Island** | USACE Baltimore District's beneficial-use island restoration — the local precedent for the Baltimore case. |
| **Living shoreline** | Vegetated/structured bank treatment replacing bulkhead-and-revetment cycles. |
| **Marsh creation cell** | Constructed marsh, typically from beneficial-use sediment. |
| **Ridge and berm** | Constructed land-bridge features for surge attenuation. |
| **HSDRRS** | Hurricane and Storm Damage Risk Reduction System — the New Orleans area system. |
| **MR&T** | Mississippi River and Tributaries project. |
| **Without-project counterfactual** | What happens if nothing is done — the comparison every benefit claim is measured against. Reactive repair typically runs 2–4× planned. |

## 6 · AI and architecture

| Term | Means |
|---|---|
| **Multi-agent** | Specialised agents dividing the work, coordinating over a protocol. |
| **A2A** | Google's Agent-to-Agent protocol for inter-agent communication. |
| **ADK** | Google's Agent Development Kit — wraps native Python functions as tools. |
| **MCP** | Model Context Protocol — standard for exposing tools and data to a model. |
| **RAG** | Retrieval-augmented generation. |
| **GraphRAG / graph-grounded verification** | Routing generative output through a graph to validate logic and suppress unsupported relationships. Applied to *outputs*, not retrieval. |
| **Compound AI System** | Multiple models and components composed into one system rather than a single model call. |
| **Bounded agent loop** | An agent loop with a hard execution ceiling. |
| **HITL** | Human-in-the-loop. |
| **Recursive CTE** | SQL common table expression that references itself — how the relationship graph was traversed in PostgreSQL before Neo4j. |

## 7 · Governance and compliance

| Term | Means |
|---|---|
| **NIST AI RMF** | NIST's AI Risk Management Framework. |
| **SR 11-7** | US supervisory guidance on model risk management. The reference standard for "can this model be trusted in a regulated setting." |
| **TEE** | Trusted Execution Environment — confidential compute. Basis for "district grants a read → enclave → knowledge out, no data retained." |
| **RBAC** | Role-based access control. |
| **PII governance** | Three-tier privacy — visible / redacted / hidden — enforced at the query layer. |
| **XAI** | Explainable AI. |
| **Provenance / lineage** | Where a figure came from and every transformation applied to it. |

## 8 · Banned copy — do not use

From `CLAUDE.md`, enforced on every build:

- **Pythia** — never, anywhere.
- **"Exit Value Enhancer" / "exit-value enhancer"** — banned. Still present in the v19 deck's appendix divider; remove there too. Wrong register for a federal audience regardless.
- **"Global DIN"**, `din-` asset paths, EVE tokens — not on the external surface.
- **"Resilient Intelligence"** — dropped, stays dropped.
- **X / The Moonshot Factory** — not in the biography. "Google" alone is fine.

## 9 · Claims discipline

Phrases that must stay accurate, because they are the product:

- **"No figure enters a payload unsourced."** Say it as a structural property.
- **Do not say** "only verified, highest-quality data for every number." The decks disprove it — Mobile shows a gap that could not be closed, Design says the benefit side is OPEN, Permitting is PENDING POC. The guarantee is that *you know the quality of every figure*, not that every figure is good.
- **PENDING POC** — Permitting is not built. Never present it as shipped.
- **Percentages stay blank** until filled from the customer's own baseline.
- **Illustrative figures** on the public EGON pages are labelled as such and must stay labelled until replaced with sourced numbers.
