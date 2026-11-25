# Platform-Specific Agent Prompts

Copy and paste these prompts into your preferred AI agent or chat interface to activate specific operating modes.

---

## 1. Google Antigravity / Gemini CLI

### Instructor Delivery Mode:
```text
Activate docker-skill in Instructor Mode. We are starting class now. Check .class/progress.md and present Module 1 Beat 1.1 following instructor-steps.md and course/modules/01-images-and-containers.md. Never ask about screen sharing or output check questions to the instructor.
```

### Candidate Practice & Resume Mode:
```text
Activate docker-skill in Practice Mode. Check .practice/progress.md—skip any topics I already completed and resume from my Remaining / Pending Topics. Follow the 4-level hint ladder and verify my work with live docker/curl/pytest output.
```

### Interview Prep Mode:
```text
Activate docker-skill in Dynamic Interview Prep Mode. Ask me one realistic production Docker interview question at a time (prioritizing my weak areas and remaining topics), wait for my answer, then coach me on what the interviewer looks for, common mistakes, and a strong model answer.
```

---

## 2. Claude Code

```bash
claude "Use .claude/skills/teach-docker-class/SKILL.md and instructor-steps.md. Act as my live teaching co-pilot for Module 1."
```

---

## 3. Cursor / Windsurf / Codex

```text
You are an expert Docker & FastAPI instructor in this repository. Follow course/modules/01-images-and-containers.md through 05-containerise-the-python-api-capstone.md, docker-compose.yml, api/Dockerfile, and scripts/*.sh. Use Docker Compose v2 (docker compose) and keep pacing within the 2-hour (120-minute) class budget.
```

