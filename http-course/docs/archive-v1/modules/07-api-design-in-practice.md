# Module 7 — API Design in Practice (detailed TOC, draft v1)

All new. Builds on Module 6.

## 7.1 Pagination
- Offset/limit vs page/size vs cursor-based
- Response shape: `items`, `total`, `next`; `Link` header
- Trade-offs (deep offsets are slow, cursors are stable)
- `GET /employees?limit=10&offset=20`

## 7.2 Filtering, sorting, searching
- `?department=eng&title=manager`
- `?sort=-hire_date`
- `?q=smith`, field selection (`?fields=name,email`)
- Query-param validation and limits

## 7.3 Consistent error format
- Why one shape everywhere
- RFC 7807 Problem Details: `type`, `title`, `status`, `detail`, `instance`
- Validation errors with field-level detail (FastAPI 422)
- Never leak stack traces

## 7.4 API documentation with OpenAPI
- OpenAPI spec, Swagger UI, ReDoc
- FastAPI generates `/docs` and `/openapi.json`
- Examples, descriptions, tags
- Spec-first vs code-first

## 7.5 Idempotency and safe retries
- Why networks retry
- `Idempotency-Key` header for POST
- Demo: double-submit creates one employee

## 7.6 Long-running work
- `202 Accepted`, status endpoint, polling
- Example: bulk import of employees

## 7.7 Concurrency control
- Lost updates; `ETag` + `If-Match`; 412 Precondition Failed; 409 Conflict
- Demo: two HR users edit one employee

## 7.8 Webhooks (intro)
- Server-to-server push: "employee.created" event
- Signatures, retries (idempotent receivers)

## 7.9 Bulk and file operations
- Bulk create/update patterns
- File upload: multipart, size limits, content-type checks (employee photo)

## 7.10 Style summary
- Checklist: naming, status codes, errors, pagination, versioning, docs

## Labs
1. Add pagination and sorting to `/employees`
2. Return RFC 7807 errors for 404 and 422
3. Explore and extend `/docs`
4. Reproduce a lost update, then fix it with ETag
5. Candidate exercise: add search and filter to `/departments/{id}/employees`

## Candidate question bank (sample)
- Offset vs cursor pagination?
- Why a standard error format?
- How does `If-Match` prevent lost updates?

## Slide work
- **Add:** about 14 slides (new module)
- Appendix pointers: GraphQL/gRPC, async APIs
