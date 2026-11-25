# Class-day quick start (instructor, 5 minutes)

**What is ready:** Day 1 (Python I) and Day 2 (Python II), each with independent modules, slide decks, runnable AI-themed terminal demos, and exercises.

## 1. Open the repo in a NEW Claude Code session
Open the `python-course` folder, then start a **new session** in it. Skills load only at session start.

## 2. Say
> **set up the class**

Wait for **READY**. It checks Python 3.10+, verifies all Day 1 and Day 2 demos and sample data files, and runs `scripts/smoke.sh`.

## 3. Open your slides
- **Day 1:** [course/slides/day1-python-i-slides.md](course/slides/day1-python-i-slides.md)
- **Day 2:** [course/slides/day2-python-ii-slides.md](course/slides/day2-python-ii-slides.md)

The agent tells you which slide number to show for every beat.

## 4. Start teaching a day
Say either:
> **teach day 1**

or:
> **teach day 2**

The agent asks whether your screen is shared, then walks through the day **one beat at a time**.

| You say | What happens |
|---|---|
| `next` / `back` | move beats |
| `repeat` | re-run the demo |
| `skip` | skip, logged |
| `answer` | reveal the answer to the question just asked |
| `more` | another question or example |
| `status` | progress and time |
| `take over` | you run the demo, agent waits |
| `jump 1.4` / `jump 2.3` | go to a beat |
| `end` | wrap up with exercise and done-check |

## Start commands by day
| Day | Start with |
|---|---|
| Day 1 – Python I | `scripts/setup.sh --day1` |
| Day 2 – Python II | `scripts/setup.sh --day2` |
| Full check (both days) | `scripts/setup.sh` |

## 5. Candidates
Send them the [Student Guide](student-guide.md). Before class they say **"set up my environment"**. After class they can say **"quiz me"** or **"help with the exercise"** (skill `practice-python`).

## 6. After class
`.class/progress.md` records completed/skipped beats, confusing topics, and notes for both days. Run `scripts/setup.sh --reset` to clean up generated File I/O outputs.

