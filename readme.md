# Hanum Agentic AI (Prototype)

A self-driven experimental project to build an intelligent, memory-enabled, and dynamically interacting autonomous AI Agent. Built from scratch using the modern LangChain and LangGraph ecosystem, powered by the Gemma 4 (31B) Cloud model as its core logic engine.

**Project Status:** Work in Progress.. This repository serves as an experimental journal for AI architecture, memory management, and Agentic Workflow exploration.

## Key Features & Current Experiments

### Cognitive Brain (Gemma 4 Cloud via LangChain)

Integrates the `gemma-4:31b-cloud` model as the core engine driving agent logic.

### Dual-Layer Persistence (LangGraph Memory)

Implements advanced memory concepts adhering to standard LangGraph documentation:

* **Short-Term Memory (Checkpointer):** Uses `InMemorySaver` to track conversation state within a single thread (chat session). The AI can recall previous context within the active session.
* **Long-Term Memory (Store):** Uses `InMemoryStore` to permanently store user preferences (e.g., hobbies, favorite coffee, etc.) accessible across threads (new sessions).

### Future Experiments (Roadmap)

Designed to evolve beyond a standard chatbot into an autonomous Multi-Agent ecosystem (Self-Learning & Self-Improving). Below is the technical development blueprint:

#### PHASE 1: Memory Automation & Autonomous Cognition (Self-Learning)

* **Automated Reflection Node:** Implements an evaluation node at the end of conversations. Gemma 4 will independently analyze chat transcripts, extract key facts or user corrections, and execute `store.put()` without manual code intervention.
* **Memory Pruning & Consolidation:** Builds a system capable of filtering long-term memory. The agent can remove invalidated information (e.g., if the user changes their coffee preference) or consolidate granular facts into a unified profile to optimize storage.
* **Semantic Memory Search:** Integrates Embedding models into `InMemoryStore`/`PostgresStore` so Hanum can retrieve long-term memories based on contextual/semantic similarity rather than basic keyword matching.

#### PHASE 2: Expanding the Arsenal (Agentic Tools Integration)

* **Cybersecurity & OSINT Suite:** Equips the agent with custom Python tools to automate technical tasks such as vulnerability scanning, Sherlock/Shodan API integration, and secure local HTTP header analysis.
* **HRD Toolkit & Psychometrics Parser:** Develops specialized tools supporting the Industrial-Organizational Psychology sub-agent, including:
* **Resume/CV Parser:** Uses Python libraries (such as `PyPDF2`/`python-docx`) to automatically extract candidate data.
* **Sentiment & Text Analytics Dashboard:** Maps employee emotions and stress levels based on internal surveys or psychometric questionnaires (e.g., Likert scale).
* **Job-Desc Matcher:** Uses text similarity algorithms (Cosine Similarity) to match candidate qualifications against company job requirements.


* **Local Database Integration:** Migrates from In-Memory storage to a robust persistent database for production readiness, utilizing `PostgresSaver` (Short-term) and `PostgresStore` (Long-term).

#### PHASE 3: Multi-Agent Architecture (Multiple Agents, One Ecosystem)

Hanum will be split into specialized sub-agents controlled by a central Primary Agent (Supervisor/Orchestrator):

* **Hanum Orchestrator (The Boss):** The main agent responsible for receiving user input, parsing intent, and delegating tasks to appropriate sub-agents via Conditional Edges in LangGraph.
* **SecOps Agent (The Pentester):** A specialized sub-agent focused exclusively on cybersecurity instructions, code analysis, and vulnerability research.
* **Hanum HRD & Psychometrics Agent (The Evaluator):** A specialized sub-agent for Industrial and Organizational (I/O) Psychology. Responsible for defining Key Performance Indicators (KPIs/OKRs), conducting workplace culture sentiment analysis from employee surveys, designing Behavioral Event Interview (BEI) scenarios, and performing initial CV screening (Resume Parsing) based on job-psychological fit.

#### PHASE 4: Self-Evaluation & Reinforcement (Self-Improving)

* **Self-Correction Loops:** If a sub-agent produces an error or malformed output, the agent catches the error message, re-evaluates it, fixes its own code, and re-executes automatically (Auto-debugging loop).
* **LangSmith Golden Dataset Evaluation:** Curates a test suite (Dataset) in LangSmith to automatically evaluate the logical performance of the entire agent network upon every architecture update.
