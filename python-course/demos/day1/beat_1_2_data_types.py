"""Day 1, Beat 1.2: Python Data Types (str, int, float, bool, NoneType)."""

prompt_text = "Explain Python in one sentence"  # str
max_tokens = 150                               # int
temperature = 0.7                              # float
stream_response = True                         # bool
api_error = None                               # NoneType

print("=== Beat 1.2: Python Data Types ===")
print(f"prompt_text     = {prompt_text!r} -> {type(prompt_text)}")
print(f"max_tokens      = {max_tokens} -> {type(max_tokens)}")
print(f"temperature     = {temperature} -> {type(temperature)}")
print(f"stream_response = {stream_response} -> {type(stream_response)}")
print(f"api_error       = {api_error} -> {type(api_error)}")

