# Module 4 — JSON and Data Contracts (detailed TOC, draft v1)

Moves from the end of the deck (slides 105–117) to right after the browser modules.
Status: **Have** · **Thin** · **Add**

## 4.1 What is JSON
- Lightweight, text-based, language independent; from JavaScript Object Notation
- Uses: APIs, config files, data exchange
Slides 106, 107 · **Have** (slide 107 says "SOAP", looks like a copy error, fix)

## 4.2 JSON syntax and types
- Objects, arrays, strings, numbers, booleans, null
- Rules: double quotes only, no trailing commas, no comments
- Nesting: employee with department object and skills array
Slides 108, 111 · **Have**

## 4.3 JSON vs XML
- Example in both, size comparison, readability
- When XML still wins: validation, XSLT, mixed content, namespaces
Slides 109, 110, 114, 116 · **Have** (trim the quote slide)

## 4.4 Why JSON for web APIs
- Native to JavaScript, smaller, easy to parse
- `JSON.parse` / `JSON.stringify`, never `eval`
Slides 112, 113 · **Have**

## 4.5 Working with JSON in practice
- Python: `json` module, `dict` ↔ JSON
- JavaScript: `fetch(...).then(r => r.json())`
- `jq` on the command line
- Common errors: invalid JSON, dates as strings, big numbers, encoding
**Add**

## 4.6 Data contracts and JSON Schema
- What a contract is; why client and server must agree
- JSON Schema: `type`, `properties`, `required`, `enum`, `format`, `minimum`
- Validating an employee payload
Slide 115 · **Thin**

## 4.7 From schema to code: Pydantic and OpenAPI
- FastAPI model → validation → auto-generated OpenAPI/JSON Schema
- Swagger UI shows the same contract
- Demo: change the model, watch `/docs` change
**Add**

## 4.8 Related formats (awareness)
- YAML, CSV, Protocol Buffers, MessagePack, JSON Lines
**Add** (Stretch)

## Labs
1. Write an employee JSON by hand; break it five ways and read the errors
2. Convert the same employee to XML and compare size
3. Write a JSON Schema and validate valid and invalid payloads
4. Open `/docs` and map each field to the Pydantic model
5. Candidate exercise: add a `skills` array and a `manager` object

## Candidate question bank (sample)
- JSON vs XML: two reasons to prefer each?
- Why is `eval` unsafe for parsing JSON?
- What does `required` do in a schema?

## Slide work
- **Fix:** slide 107 copy error; reorder to follow this TOC; HR examples in 108–109
- **Add:** 4.5, 4.7 (about 5 slides)
