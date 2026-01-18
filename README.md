# Deep Research – Multi‑Agent AI Research System

An **asynchronous, multi‑agent research pipeline** that takes a natural‑language query, plans web searches, executes them concurrently, synthesizes a long‑form research report, **critiques and improves it iteratively**, and finally emails the result — all with real‑time progress streaming via a Gradio UI.

This project demonstrates **agent orchestration, async concurrency, structured outputs, and self‑correcting AI workflows**.

---

## 🚀 Key Features

* **Planner Agent** – Breaks a query into structured web searches
* **Concurrent Search Agents** – Executes searches in parallel (asyncio)
* **Writer Agent** – Produces a detailed markdown research report
* **Critic Agent** – Reviews the report, finds gaps, suggests follow‑up research
* **Iterative Refinement Loop** – Improves report quality automatically
* **Email Agent** – Sends the final report via SendGrid
* **Streaming UI** – Live progress updates using Gradio
* **Traceability** – Built‑in execution tracing

---

## 🧠 System Architecture

```text
User Query
   ↓
Planner Agent
   ↓
Search Agents (parallel)
   ↓
Writer Agent (initial report)
   ↓
Critic Agent
   ↓
Follow‑up Searches (optional)
   ↓
Writer Agent (refined report)
   ↓
Email Agent
```



---

## 📁 Project Structure

```text
.
├── deep_research.py        # Gradio UI (entry point)
├── research_manager.py    # Orchestrates the full workflow
├── planner_agent.py       # Plans search queries
├── search_agent.py        # Performs web searches
├── writer_agent.py        # Synthesizes research reports
├── critic_agent.py        # Reviews & improves reports
├── email_agent.py         # Sends report via email
├── .env                   # API keys & configuration
└── README.md
```

---

## 🛠️ Installation & Setup

### 1️⃣ Create virtual environment

```bash
python -m venv venv
source venv/bin/activate   # macOS / Linux
venv\Scripts\activate      # Windows
```

### 2️⃣ Install dependencies

```bash
pip install openai-agents gradio python-dotenv sendgrid pydantic
```

---

## 🔐 Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
SENDGRID_API_KEY=SG.xxxxxxxxxxxxxxxxx
```
---

## ▶️ Running the Application

```bash
python deep_research.py
```

You should see:

```text
Running on local URL: http://127.0.0.1:7860
```

Open the link, enter a research query, and click **Run**.

---

## 🧪 Example Query

```
Impact of large language models in healthcare
```

The system will:

* Plan searches
* Run them concurrently
* Write an initial report
* Critique and refine it
* Send the final report via email

---

## 💡 Design Highlights

* **Async‑first architecture** – optimized for I/O‑bound workloads
* **Agent specialization** – each agent has a single responsibility
* **Structured outputs (Pydantic)** – reliable agent communication
* **Iterative reasoning loop** – higher‑quality research results
* **Production‑oriented** – retries, tracing, fault isolation

---

---

## 📄 License

MIT License
