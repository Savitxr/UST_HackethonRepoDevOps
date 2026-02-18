from collections import Counter
from pathlib import Path
import re


WORD_RE = re.compile(r'\b[^\W\d_]+\b')  # excludes numbers/underscores
STOP_WORDS = {
    "the", "a", "an", "and", "or", "to", "as",
    "of", "in", "on", "for", "by", "with", "at",
    "info", "warn", "warning", "error", "debug", "trace", "fatal",
    "http", "https", "get", "post", "put", "delete", "request", "response",
}

def tokenize(line: str):
    return (t.lower() for t in WORD_RE.findall(line.lower()))

def main():
    log_path = Path("Anomolizer") / "Windows_2k.log"
    out_path = Path("flagged_lines.txt")

    counter = Counter()

    # count global token frequencies
    with log_path.open("r", encoding="utf-8", errors="replace") as f:
        for line in f:
            for token in tokenize(line):
                if token not in STOP_WORDS:
                    counter[token] += 1

    total_tokens = sum(counter.values())
    if total_tokens == 0:
        print("No tokens found (after stopword filtering). Adjust regex/stopwords.")
        return

    threshold = total_tokens * 0.01 
    rare_words = {w for w, c in counter.items() if c < threshold}

    print(f"[stats] total_tokens={total_tokens} unique_tokens={len(counter)} rare_words={len(rare_words)}")

    # flag lines that contain any rare word
    flagged = 0
    with log_path.open("r", encoding="utf-8", errors="replace") as f, out_path.open("w", encoding="utf-8") as out:
        for i, line in enumerate(f, start=1):
            tokens = list(tokenize(line))
            if any(t in rare_words for t in tokens):
                out.write(f"[line {i}] {line}")
                flagged += 1
    print(counter.most_common(10))  
    print(f"[done] flagged_lines={flagged}, written to: {out_path}")

if __name__ == "__main__":
    main()