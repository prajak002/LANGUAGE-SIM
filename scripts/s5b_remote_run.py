"""Run the frozen S5 prompts with a larger open-weight model on a machine with a GPU (e.g. a free Kaggle or Colab notebook).

    pip install -q transformers accelerate bitsandbytes
    python s5b_remote_run.py prompts.jsonl answers.jsonl [MODEL_ID]

Default model: Qwen/Qwen2.5-14B-Instruct (open weights, Apache 2.0), loaded in 4-bit. Greedy decoding, at most
8 new tokens, the prompt text unchanged. Writes one line per prompt in the format that
`scripts/llm_dissociation.py ... score` reads. Resumable. Copy answers.jsonl back to data/llm_s5b/.
"""
import json, os, sys

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

SRC, DST = sys.argv[1], sys.argv[2]
MODEL = sys.argv[3] if len(sys.argv) > 3 else "Qwen/Qwen2.5-14B-Instruct"
torch.manual_seed(20261011)
tok = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForCausalLM.from_pretrained(MODEL, device_map="auto",
                                             quantization_config=BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype=torch.float16))
done = set()
if os.path.exists(DST):
    done = {(d["lang"], d["title"], d["route"], d["condition"]) for d in map(json.loads, open(DST, encoding="utf-8"))}
with open(DST, "a", encoding="utf-8") as out:
    for i, d in enumerate(map(json.loads, open(SRC, encoding="utf-8")), 1):
        if (d["lang"], d["title"], d["route"], d["condition"]) in done:
            continue
        ids = tok.apply_chat_template([{"role": "user", "content": d["prompt"]}], add_generation_prompt=True, return_tensors="pt").to(model.device)
        with torch.no_grad():
            gen = model.generate(ids, max_new_tokens=8, do_sample=False)
        raw = tok.decode(gen[0, ids.shape[1]:], skip_special_tokens=True)
        out.write(json.dumps({k: d[k] for k in ("lang", "title", "route", "subset", "condition", "A_is")} | {"raw": raw, "model": MODEL}, ensure_ascii=False) + "\n")
        if i % 100 == 0:
            out.flush()
            print(i, flush=True)
print("done")
