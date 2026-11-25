# Universal Master Prompts for System Design

These master prompts are **100% platform-neutral** and engineered to run identically across all modern LLMs and agent platforms:
- **Claude** (Claude Code, Claude Projects, Claude Web)
- **Antigravity** (Google DeepMind Agentic IDE & CLI)
- **ChatGPT** (OpenAI Custom GPTs, Projects, or standard chats)
- **Gemini** (Google AI Studio System Prompts, Gemini Gems, Vertex AI)
- **Grok** (xAI Grok System Prompt / Assistant)
- **Codex / Local Models** (Cursor, Windsurf, Ollama, vLLM)

---

## The Four-Agent Architecture

In accordance with the Whitebox Learning pedagogy, the 4 student-facing agents have strictly separated responsibilities:

| Agent Prompt | Its One Job | When to Use It |
|---|---|---|
| [tutor-agent.md](file:///c:/Users/AI%20ML%20PC%20Ajmeer/Desktop/Course%20Restructure/wbl-technical-learning-hub/System%20Design/prompts/tutor-agent.md) | Explain concepts using *The Growing City* story until understood | After class, when a concept is unclear |
| [practice-agent.md](file:///c:/Users/AI%20ML%20PC%20Ajmeer/Desktop/Course%20Restructure/wbl-technical-learning-hub/System%20Design/prompts/practice-agent.md) | Turn topics into hands-on tasks & real-world job scenarios | After tutor, for assignments and design drills |
| [coding-review-agent.md](file:///c:/Users/AI%20ML%20PC%20Ajmeer/Desktop/Course%20Restructure/wbl-technical-learning-hub/System%20Design/prompts/coding-review-agent.md) | Review system architecture and code using the Hint Ladder | Reviewing 1-page designs and API code |
| [quiz-assessment-agent.md](file:///c:/Users/AI%20ML%20PC%20Ajmeer/Desktop/Course%20Restructure/wbl-technical-learning-hub/System%20Design/prompts/quiz-assessment-agent.md) | Fair examination, finding weak areas, and generating Daily Report | End of day, last, every day |
| [instructor-copilot.md](file:///c:/Users/AI%20ML%20PC%20Ajmeer/Desktop/Course%20Restructure/wbl-technical-learning-hub/System%20Design/prompts/instructor-copilot.md) | Classroom co-pilot managing beats, demos, and hidden answer keys | For the instructor during live teaching |

---

## How to Set Up On Any Platform

### 1. ChatGPT (Custom GPT or Project)
1. Create a Project or Custom GPT named `WBL - System Design Tutor` (repeat for Practice, Review, Quiz).
2. Paste the exact text from the corresponding prompt file into the **Instructions** field.
3. Attach `docs/student-guide.md` and your `candidate-state.md` to Project Files / Knowledge.

### 2. Google Gemini / Gemini Gems / Antigravity
1. Create a new Gem or Antigravity workspace rule.
2. Paste the prompt text into the **Instructions / System Prompt** field.
3. Set model to Gemini 1.5 Pro or Flash.

### 3. Claude / Claude Code
- Claude Code automatically discovers `.claude/skills/`.
- For Claude Projects on web: Create 4 projects and paste the master prompt into each Project's custom instructions.

### 4. Grok / Generic LLM Chat Fallback
1. Open a new chat.
2. Message 1: Paste the full master prompt, and add: *"Confirm you understand your role in one sentence, then wait for my Candidate State."*
3. Message 2: Paste your `candidate-state.md`.
4. Message 3: Send the agent's starter line.
