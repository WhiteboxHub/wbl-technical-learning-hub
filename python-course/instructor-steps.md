# Instructor steps: how to start and take the class

Course: **Python I & Python II (AI Engineering Edition)**, taught with an AI co-pilot (Claude Code) and runnable Python terminal demos.
Project folder: `python-course/`. More detail: `docs/instructor-guide.md` and `docs/class-day-quickstart.md`.

## Before class

1. **Open the right folder.** In Claude Code, open `python-course/` and start a **new session**. Skills load only at session start.
2. **Verify Python 3.10+** is available on your machine (`python3 --version`).
3. **Open your slides** for the day you are teaching:
   - Day 1: `course/slides/day1-python-i-slides.md`
   - Day 2: `course/slides/day2-python-ii-slides.md`

## Starting the class

1. Say **"set up the class"**. It checks Python 3, verifies course files and exercises, runs the smoke test on Day 1 and Day 2 demos, and ends with **READY**.
2. Choose which day to teach independently:
   - Say **"teach day 1"** (or **"teach module 1"**) → Python I: The Labelled Pantry
   - Say **"teach day 2"** (or **"teach module 2"**) → Python II: The Kitchen's Containers
3. The agent checks the day's demo files, shows the objectives and beat count, and checks `.class/progress.md` if you are resuming an unfinished day.
4. It asks whether your screen is shared. If yes, answers stay hidden until you ask for them.

## Start commands by day

| Day | Title | Start with |
|---|---|---|
| **Day 1** | Python I (The Labelled Pantry) | `scripts/setup.sh --day1` (or `scripts/setup.sh`) |
| **Day 2** | Python II (The Kitchen's Containers) | `scripts/setup.sh --day2` (or `scripts/setup.sh`) |

To clean up temporary files created by Day 2 File I/O demos: `scripts/setup.sh --reset`.

## During class

The agent works one beat at a time: it tells you which slide to show, gives the talking points and simple definition, runs or hands over the terminal demo, and asks the student interaction question. You present and talk to the room.

| You say | What happens |
|---|---|
| `next` / `back` | move between beats |
| `repeat` | re-run the terminal demo |
| `skip` | skip this beat and log it |
| `answer` | reveal the answer to the question just asked |
| `more` | another question or example |
| `status` | progress and time |
| `take over` | you run the demo yourself; the agent waits |
| `jump 1.3` / `jump 2.2` | go directly to a beat |
| `end` | wrap up the day |

- **Beat 1.3 (Input & Type Casting):** takes keyboard input interactively, or accepts piped demo values when run by the agent.
- **Beat 2.4 (File Handling):** reads `demos/day2/data/model_config.json` and `demos/day2/data/prompt_docs.txt` and writes a log file.

## At the end of each day

1. Say `end`. The agent recaps what was covered, hands over the practical exercise (`exercises/day1_exercise.py` or `exercises/day2_exercise.py`), runs the done-check, and offers to clean up demo output files (`scripts/setup.sh --reset`).
2. It writes a post-class note to `.class/progress.md`: skipped beats, confusing topics, and teaching notes.

## If something goes wrong

| Problem | Do this |
|---|---|
| Python not found | Install Python 3.10+ from python.org, then say "set up the class" again |
| Demo output changed after edits | Say "reset the data" (runs `scripts/setup.sh --reset`) |
| Skill not found | You are in an old session; open `python-course/` in a new session |
| Input script appears stuck | Beat 1.3 is waiting for you to type an answer in the terminal and press Enter |

## Candidates

Send them `docs/student-guide.md`. Before class they say **"set up my environment"**; afterwards they say **"quiz me"** or **"help with the exercise"**.

