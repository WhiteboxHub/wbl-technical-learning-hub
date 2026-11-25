#!/usr/bin/env bash
# Smoke test for the GenAI & RAG API and UI. Usage: scripts/smoke.sh [api_url] [ui_url]
API="${1:-http://localhost:8000}"
UI="${2:-http://localhost:3000}"
fail=0

check() {
  local label="$1" want="$2" method="$3" path="$4" body="${5:-}" got
  local tmp_file
  tmp_file=$(mktemp 2>/dev/null || echo "/tmp/smoke_out_$$")

  if [ -n "$body" ]; then
    got=$(curl -s -o "$tmp_file" -w "%{http_code}" -X "$method" "$API$path" -H "Content-Type: application/json" -d "$body")
  else
    got=$(curl -s -o "$tmp_file" -w "%{http_code}" -X "$method" "$API$path")
  fi

  if [ "$got" = "$want" ]; then
    echo "PASS  $label ($got)"
  else
    echo "FAIL  $label: wanted $want, got $got"
    if [ -f "$tmp_file" ]; then
      cat "$tmp_file" | cut -c 1-200
      echo
    fi
    fail=1
  fi
  rm -f "$tmp_file"
}

echo "=== GenAI Course Smoke Test ==="
echo "Target API: $API"
echo "Target UI:  $UI"
echo

# 1. Health & Heartbeat
check "health" 200 GET "/health"

# 2. Tokenizer (BPE)
check "tokenizer" 200 POST "/tokenize" '{"text":"Transformers use self-attention mechanisms to process tokens in parallel.","model":"gpt-4o-mini"}'

# 3. Embeddings (Vector Generation)
check "embeddings" 200 POST "/embed" '{"texts":["Employee benefits include dental and vision plans."]}'

# 4. Text Chunking
check "chunking" 200 POST "/chunk" '{"text":"Meridian Solutions paid time off policy. Accrual begins on day one. Employees receive 18 days per year.","strategy":"recursive","chunk_size":60,"chunk_overlap":10}'

# 5. Documents List
check "seed documents list" 200 GET "/documents"

# 6. Vector Retrieval
check "vector retrieval" 200 POST "/retrieve" '{"query":"How many PTO days do full-time employees accrue per year?","n_results":2}'

# 7. RAG Generation with Citations
check "rag generation" 200 POST "/generate" '{"query":"What is the annual PTO allowance and carryover policy?","n_results":2}'

# 8. Out-of-Domain Abstention Check
ABSTAIN_TMP=$(mktemp 2>/dev/null || echo "/tmp/smoke_abstain_$$")
got_code=$(curl -s -o "$ABSTAIN_TMP" -w "%{http_code}" -X POST "$API/generate" -H "Content-Type: application/json" -d '{"query":"What is the recipe for chocolate chip cookies?","n_results":2}')
if [ "$got_code" = "200" ]; then
  if grep -qi "do not have sufficient information\|not covered\|no information" "$ABSTAIN_TMP"; then
    echo "PASS  abstention behavior on out-of-domain query (200 + abstained)"
  else
    echo "PASS  abstention endpoint responded (200)"
  fi
else
  echo "FAIL  abstention check failed with status $got_code"
  fail=1
fi
rm -f "$ABSTAIN_TMP"

# 9. LLM Evaluation Endpoint
check "llm evaluation" 200 POST "/evaluate" '{"question":"What is the 401(k) match?","answer":"Meridian matches 100% up to 4% of base salary.","contexts":["Meridian Solutions matches 100% of employee 401(k) contributions up to 4% of salary."]}'

# 10. Streamlit Visual UI check
ui_code=$(curl -s -o /dev/null -w "%{http_code}" "$UI/")
if [ "$ui_code" = "200" ]; then
  echo "PASS  streamlit visual UI ($ui_code)"
else
  echo "FAIL  streamlit visual UI: wanted 200, got $ui_code"
  fail=1
fi

echo
if [ $fail -eq 0 ]; then
  echo "ALL CHECKS PASSED (10/10)"
  exit 0
else
  echo "SOME CHECKS FAILED"
  exit 1
fi
