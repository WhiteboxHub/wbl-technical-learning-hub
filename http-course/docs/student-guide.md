# Student Guide

HTTP, Web Services, REST APIs, Auth/SSO and Microservices. You will learn by sending real requests to a small HR system running on your own laptop.

## 1. What you will learn
| # | Module | You will be able to… |
|---|---|---|
| 1 | HTTP foundations | read and write raw HTTP, pick methods and status codes, use `curl` and DevTools |
| 2 | Websites, browser and storage | explain what happens when you open a URL; cookies, storage, CORS |
| 3 | JSON and REST APIs | design and call a REST API with CRUD, pagination, errors, docs |
| 4 | Authentication and tokens | use API keys, bearer tokens and JWT; roles and permissions |
| 5 | SSO and web security | explain OAuth/OIDC and single sign-on; spot XSS, CSRF, injection |
| 6 | API gateway and scaling | rate limiting, caching, versioning |
| 7 | Microservices | split a system into services; resilience and communication |
| 8 | Capstone | trace one request through the whole system |

The example throughout is an **HR system**: employees, departments, managers.

## 2. Get your laptop ready (before class)
You need:
- **Docker Desktop** (installed and running): https://www.docker.com/products/docker-desktop/
- **Claude Code** (desktop app or CLI), to run the setup helper
- A terminal with `curl` (macOS and Linux have it; on Windows use WSL2 or Git Bash)
- A modern browser (Chrome, Edge or Firefox)
- Optional: Postman

Then:
1. Get the `http-course` folder from your instructor and open it in Claude Code (start a **new session** after opening it).
2. Say **"set up my environment"**. The helper checks Docker, starts the HR system and tests it. When it prints **READY** you are done.
3. Make your first request:
   ```bash
   curl -i http://localhost:8000/v2/employees/1
   ```
   You should see `HTTP/1.1 200 OK`, some headers, then JSON for **Priya Raman, Head of HR**.
4. Open http://localhost:8000/docs in your browser to see the interactive API page (Swagger), and http://localhost:3000 for the HR Directory web page (used from Module 2).

**Stuck?** Tell the helper what you see. Common causes: Docker Desktop isn't running, or something else already uses port 8000 or 5432.

## 3. During class
- Your instructor presents; follow along on your own machine and try the commands.
- Keep the HR system running (`docker compose` containers stay up after setup).
- You can break things. To go back to the starting data: `scripts/setup.sh --reset`. To stop everything: `scripts/setup.sh --stop`.

## 4. The HR system at a glance
Base URL: `http://localhost:8000`

| Method | Path | What it does |
|---|---|---|
| GET | `/health` | is it running |
| GET, POST | `/v2/departments` | list, create |
| GET, PUT, DELETE | `/v2/departments/{id}` | read, replace, delete (409 if employees remain) |
| GET | `/v2/departments/{id}/employees` | employees of one department |
| GET, POST | `/v2/employees` | list (`?limit=&offset=&department_id=&q=&sort=`), create |
| GET, PUT, PATCH, DELETE | `/v2/employees/{id}` | read, replace, update some fields, delete |

Seed data: 4 departments, 20 employees.

## 5. Module 1 cheat sheet

**An HTTP request**
```
GET /v2/employees/1 HTTP/1.1      ← request line: method, path, version
Host: localhost                   ← headers
                                  ← blank line
                                  ← body (none for GET)
```
**An HTTP response**
```
HTTP/1.1 200 OK                   ← status line
content-type: application/json    ← headers
                                  ← blank line
{"name":"Priya Raman", ...}       ← body
```

**Methods**
| Method | Use | Safe | Idempotent |
|---|---|---|---|
| GET | read | yes | yes |
| POST | create | no | no |
| PUT | replace whole resource | no | yes |
| PATCH | change some fields | no | usually not guaranteed |
| DELETE | remove | no | yes |
| HEAD | headers only | yes | yes |
| OPTIONS | what is allowed | yes | yes |

*Safe* = doesn't change anything. *Idempotent* = repeating gives the same end state.

**Status codes you will use**
| Code | Meaning |
|---|---|
| 200 / 201 / 204 | OK / Created / No Content |
| 301, 302, 307, 308 | redirects (307/308 keep the method) |
| 304 | Not Modified (your cached copy is fine) |
| 400 / 422 | bad request / failed validation |
| 401 | not logged in (who are you?) |
| 403 | logged in but not allowed |
| 404 / 405 | not found / method not allowed |
| 409 | conflict (duplicate, or still in use) |
| 429 | too many requests |
| 500 / 502 / 503 / 504 | server error / bad gateway / unavailable / gateway timeout |

4xx = the client's fault. 5xx = the server's fault.

**URL anatomy**
`http://localhost:8000/v2/employees?department_id=2&limit=3#top`
scheme `http` · host `localhost` · port `8000` · path `/v2/employees` · query `department_id=2&limit=3` · fragment `#top` (never sent to the server). Spaces and special characters are percent-encoded (`space` → `%20`).

**curl you will use**
```bash
curl http://localhost:8000/v2/employees/1                 # GET
curl -i  URL                                              # show response headers too
curl -v  URL                                              # show request and response
curl -X DELETE URL                                        # choose the method
curl -X POST URL -H 'Content-Type: application/json' -d '{"name":"..."}'   # send JSON
curl -L  URL                                              # follow redirects
curl -s -o /dev/null -w "%{http_code}\n" URL              # just the status code
```

## 6. Exercise: Module 1 (about 15 minutes)
Write five `curl` commands against the HR API, and show the status code of each:
1. List employees of department 2.
2. Fetch one employee.
3. Create an employee.
4. Update its title.
5. Delete it.

Stretch: make each of **404, 405, 409 and 422** happen on purpose.

*Check yourself:* can you (1) point at the parts of a raw request, (2) choose the method and status code for create, read, replace, update and delete, (3) explain *stateless* and *idempotent*, (4) name five headers, (5) describe a 304 round trip?

## 7. Troubleshooting
| Problem | What to do |
|---|---|
| "Docker not running" | Open Docker Desktop and wait until it says running |
| "Port 8000/5432 in use" | Another program is using it. Ask the helper; don't stop it without checking |
| `curl: (7) Failed to connect` | The stack isn't running. Run `scripts/setup.sh` |
| Data looks wrong after experiments | `scripts/setup.sh --reset` |
| Windows: script won't run | Use WSL2 or Git Bash |
| Helper command not found | Open the repo in a **new** session |

## 8. Practice after class
In Claude Code, inside the course folder, say:
- **"quiz me"**: one question at a time, with feedback
- **"help with the exercise"**: hints first, answers last; it checks your work against the running API
- **"check my progress on module 1"**: walks the self-check

## 9. Later modules
Modules 4–8 (auth and tokens, SSO and security, gateway, microservices, capstone) use extra parts of the stack. Your instructor starts them in class; to follow along, run the command the instructor gives you. If something stops working afterwards, `scripts/fix.sh` returns to the normal setup.
