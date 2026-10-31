"""Make dialogue line breaks visible in GitHub Markdown."""
from pathlib import Path

ROOT = Path(r"E:\GithubRepos\English-Shadowing-Materials\Speak English with David & Alice")


def convert(text: str) -> str:
    newline = "\r\n" if "\r\n" in text else "\n"
    normalized = text.replace("\r\n", "\n")
    if "## 台词" not in normalized:
        raise ValueError("missing dialogue heading")
    head, body = normalized.split("## 台词", 1)
    lines: list[str] = []
    for raw in body.splitlines():
        content = raw.strip()
        if not content:
            continue
        if content.startswith(">") and not content.startswith("\\>"):
            content = "\\" + content
        lines.append(content)
    result = head + "## 台词\n\n" + "\n\n".join(lines) + "\n"
    if newline == "\r\n":
        result = result.replace("\n", "\r\n")
    return result


def main() -> None:
    files = sorted(ROOT.glob("*.md"))
    changed = 0
    for path in files:
        original = path.read_bytes().decode("utf-8")
        updated = convert(original)
        if updated != original:
            path.write_bytes(updated.encode("utf-8"))
            changed += 1
    print(f"files {len(files)} changed {changed}")


if __name__ == "__main__":
    main()
