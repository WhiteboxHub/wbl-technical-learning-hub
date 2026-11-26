---
name: setup-sdlc-class
description: Setup and health-check skill for the Software Design, Architecture, SDLC & Agile (Jira) course. Use when starting class ("set up the class", "verify setup", "check prerequisites") to verify module files, documentation, and AI skills.
---

# Class Setup & Verification Skill

Use this skill when preparing for class delivery. It verifies that all teaching assets, curriculum documentation, and course resources are present and structurally sound.

## Checks Performed
1. **Course Modules Complete**:
   - `course/modules/01-software-architecture-and-design.md`
   - `course/modules/02-sdlc-models-and-alm.md`
   - `course/modules/03-agile-and-scrum-framework.md`
   - `course/modules/04-jira-in-practice.md`
   - `course/modules/05-capstone-system-design-to-jira.md`
2. **AI Skills Verified**:
   - `teach-sdlc-class` (Instructor Co-Pilot)
   - `learn-sdlc` (Self-Paced Candidate Tutor)
   - `practice-sdlc` (Candidate Practice Coach & Interview Simulator)
   - `setup-sdlc-class` (Instructor Setup Validator)
   - `setup-candidate` (Candidate Onboarding & Laptop Preparation)
3. **Core Documentation Ready**:
   - `README.md`, `instructor-steps.md`, `docs/course-toc.md`, `docs/instructor-guide.md`, `docs/student-guide.md`, `docs/class-day-quickstart.md`.
5. **No Code / Zero-Local-Server Delivery Confirmed**:
   - Confirm the session uses **no** practical code examples, programming exercises, or local databases—only conceptual architecture walkthroughs, the *Building a House* story anchor, and live Atlassian Jira Cloud steps.

## How to Run
In chat, type:
```text
set up the class
```
The skill directly checks that all 5 curriculum modules, 5 AI skills, and documentation files are present.
When verified, it outputs **READY TO TEACH** and prompts:
`Type "teach module 1" to begin.`
