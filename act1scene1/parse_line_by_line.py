import re
from pathlib import Path

MD_PATH = Path(__file__).parent / "line-by-line.md"

SPEAKERS = {
    "ANTONIO", "SALARINO", "SOLANIO", "BASSANIO", "LORENZO", "GRATIANO"
}

SECTION_ORDER = [
    "Antonio's Melancholy",
    "Salarino's Theory",
    "Solanio's View",
    "Antonio Rejects Their Assumption",
    "Humorous Exchange",
    "Arrival of Antonio's Friends",
    "Gratiano's Advice About Life",
    "The World as a Stage",
    "Gratiano's Speech on False Wisdom",
    "Comic Relief",
    "Bassanio's Assessment of Gratiano",
    "Transition to the Main Plot",
    "Bassanio's Financial Problems",
    "Antonio's Extraordinary Friendship",
    "The Arrow Analogy",
    "Antonio's Unconditional Support",
    "Introduction of Portia",
    "Mythological Imagery",
    "Bassanio's Hope",
    "Antonio's Final Promise",
]

SECTION_STARTS = [
    "in sooth i know not why i am so sad",
    "your mind is tossing on the ocean",
    "believe me sir had i such venture forth",
    "believe me no i thank my fortune for it",
    "why then you are in love",
    "here comes bassanio your most noble kinsman",
    "you look not well signior antonio",
    "i hold the world but as the world gratiano",
    "let me play the fool",
    "well we will leave you then till dinner time",
    "is that anything now",
    "well tell me now what lady is the same",
    "tis not unknown to you antonio",
    "i pray you good bassanio let me know it",
    "in my school days when i had lost one shaft",
    "you know me well and herein spend but time",
    "in belmont is a lady richly left",
    "for the four winds blow in from every coast",
    "o my antonio had i but the means",
    "thou knowst that all my fortunes are at sea",
]


def norm(text):
    text = text.strip().lower()
    for ch in "''`´‘’":
        text = text.replace(ch, "")
    text = text.replace(""", "").replace(""", "")
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def is_gloss(line):
    s = line.strip()
    return s.startswith("(") and "=" in s


def is_stage_bold(text):
    return text.startswith("Enter ") or text.endswith(" exit.")


def section_index_for(text):
    n = norm(text)
    for i, start in enumerate(SECTION_STARTS):
        if n.startswith(start):
            return i
    return None


def parse_md_lines():
    raw_lines = MD_PATH.read_text(encoding="utf-8").splitlines()
    entries = []
    speaker = None
    i = 0

    while i < len(raw_lines):
        line = raw_lines[i].strip()
        i += 1
        if not line or line.startswith("###") or line.startswith("→") or line == "---":
            continue

        if line.startswith("*") and line.endswith("*") and not line.startswith("**"):
            entries.append({
                "speaker": "STAGE",
                "text": line.strip("*").strip(),
                "translation": line.strip("*").strip(),
            })
            continue

        bold_parts = re.findall(r"\*\*([^*]+)\*\*", line)
        if bold_parts:
            remainder = re.sub(r"\*\*[^*]+\*\*", "", line).strip().strip('"')
            for part in bold_parts:
                part = part.strip()
                if part.upper() in SPEAKERS:
                    speaker = part.upper()
                    continue
                if is_stage_bold(part):
                    entries.append({
                        "speaker": "STAGE",
                        "text": part,
                        "translation": "Antonio, Salarino, and Solanio enter.",
                    })
                    continue

                translation = remainder if remainder and not is_gloss(remainder) else None
                if not translation:
                    while i < len(raw_lines):
                        nxt = raw_lines[i].strip()
                        if not nxt:
                            i += 1
                            continue
                        if nxt.startswith("**") or nxt == "---":
                            break
                        i += 1
                        if is_gloss(nxt):
                            continue
                        translation = nxt.strip('"')
                        break
                entries.append({
                    "speaker": speaker or "STAGE",
                    "text": part,
                    "translation": translation or part,
                })
            continue

        if speaker and not is_gloss(line):
            entries.append({
                "speaker": speaker,
                "text": line,
                "translation": line,
            })

    return entries


def group_into_sections(entries):
    sections = []
    current = None
    next_section = 0

    for entry in entries:
        idx = section_index_for(entry["text"])
        if idx is not None:
            if idx == 0 and entry["speaker"] == "STAGE":
                if current is None:
                    current = {"title": SECTION_ORDER[0], "lines": []}
                current["lines"].append(entry)
                next_section = max(next_section, 1)
                continue
            if idx >= next_section:
                if current and current["lines"]:
                    sections.append(current)
                current = {"title": SECTION_ORDER[idx], "lines": []}
                next_section = idx + 1
        if current is None:
            current = {"title": SECTION_ORDER[0], "lines": []}
        current["lines"].append(entry)

    if current and current["lines"]:
        sections.append(current)

    merged = []
    for sec in sections:
        if merged and merged[-1]["title"] == sec["title"]:
            merged[-1]["lines"].extend(sec["lines"])
        else:
            merged.append(sec)
    return merged


def load_sections():
    return group_into_sections(parse_md_lines())


if __name__ == "__main__":
    sections = load_sections()
    total = sum(len(s["lines"]) for s in sections)
    print(f"Sections: {len(sections)}")
    print(f"Lines: {total}")
    for sec in sections:
        print(f"{sec['title']}: {len(sec['lines'])}")