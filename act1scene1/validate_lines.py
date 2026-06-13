from parse_line_by_line import load_sections, parse_md_lines, norm

sections = load_sections()
generated = [line for sec in sections for line in sec["lines"]]
parsed = parse_md_lines()

print(f"Parsed MD entries: {len(parsed)}")
print(f"Generated page lines: {len(generated)}")

# Lines in parsed md that are not gloss and should appear on page
expected = [e for e in parsed if not (e["text"].strip().startswith("(") and "=" in e["text"])]
expected_norms = {norm(e["text"]) for e in expected}
generated_norms = {norm(e["text"]) for e in generated}

missing = [e for e in expected if norm(e["text"]) not in generated_norms]
extra = [e for e in generated if norm(e["text"]) not in expected_norms]

print(f"Missing on page: {len(missing)}")
for e in missing[:20]:
    print(f"  - [{e['speaker']}] {e['text'][:90]}")
if len(missing) > 20:
    print(f"  ... and {len(missing) - 20} more")

print(f"Extra on page: {len(extra)}")
for e in extra[:10]:
    print(f"  + [{e['speaker']}] {e['text'][:90]}")