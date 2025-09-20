import subprocess
import argparse
import random

# Emojis for change types
EMOJIS = {
    "A": "✨",   # Added
    "M": "🔧",   # Modified
    "D": "🗑️",  # Deleted
    "R": "🔄",  # Renamed
    "C": "📑",  # Copied
    "AM": "📦", # Added + Modified
    "??": "🆕", # Untracked new file
}

# File categories
CATEGORIES = {
    "code": [".py", ".js", ".java", ".cpp", ".ts"],
    "frontend": [".html", ".css", ".scss"],
    "docs": [".md", ".txt", ".rst"],
    "config": [".json", ".yaml", ".yml", ".env", ".ini"],
}

# Fun endings
FLAVORS = ["🚀 Let's go!", "🔥 Ship it!", "🛠️ Refactor done.", "✅ Clean commit."]


def get_changed_files():
    """Get changed files from git status."""
    result = subprocess.run(["git", "status", "--porcelain"],
                            capture_output=True, text=True)
    lines = result.stdout.strip().split("\n")
    return [line for line in lines if line]


def detect_category(filename):
    """Detect category of file by extension."""
    for category, exts in CATEGORIES.items():
        if any(filename.endswith(ext) for ext in exts):
            return category
    return "other"


def get_diff_details(filename):
    """Return added/removed lines for a file."""
    result = subprocess.run(["git", "diff", "--unified=0", filename],
                            capture_output=True, text=True)
    lines = result.stdout.split("\n")

    changes = []
    for line in lines:
        if line.startswith("+") and not line.startswith("+++"):
            changes.append("  + " + line[1:])
        elif line.startswith("-") and not line.startswith("---"):
            changes.append("  - " + line[1:])
    return changes


def generate_message(verbose=False, with_flavor=False, show_lines=False, short=False):
    changes = get_changed_files()
    if not changes:
        return "✅ No changes to commit"

    # Short overrides everything else
    if short:
        counts = {}
        for change in changes:
            _, filename = change[:2].strip(), change[3:]
            cat = detect_category(filename)
            counts[cat] = counts.get(cat, 0) + 1

        parts = [f"{n} {c} file{'s' if n > 1 else ''}" for c, n in counts.items()]
        msg = "Summary: " + ", ".join(parts)
        if with_flavor:
            msg += " " + random.choice(FLAVORS)
        return msg

    messages = []
    for change in changes:
        status, filename = change[:2].strip(), change[3:]
        emoji = EMOJIS.get(status, "📦")
        cat = detect_category(filename)

        action_map = {
            "A": "Created",
            "M": "Modified",
            "D": "Deleted",
            "R": "Renamed",
            "C": "Copied",
            "AM": "Added & Modified",
            "??": "Created new",
        }
        action = action_map.get(status, "Changed")

        if verbose:
            msg = f"{emoji} {action} {cat} file {filename}"
        else:
            msg = f"{emoji} {action} {cat} file(s)"

        messages.append(msg)

        if show_lines:
            diff_lines = get_diff_details(filename)
            if diff_lines:
                messages.append(f"Changes in {filename}:")
                messages.extend(diff_lines)

    final_msg = "\n".join(messages)
    if with_flavor:
        final_msg += "\n" + random.choice(FLAVORS)

    return final_msg


def main():
    parser = argparse.ArgumentParser(description="Generate human-friendly git commit messages.")
    parser.add_argument("--verbose", action="store_true", help="Show detailed file list.")
    parser.add_argument("--show-lines", action="store_true", help="Show exact added/removed lines.")
    parser.add_argument("--flavor", action="store_true", help="Add a fun ending to the commit message.")
    parser.add_argument("--short", action="store_true", help="Show a 1-line summary of changes.")
    parser.add_argument("--stage", action="store_true", help="Stage all changes before generating the message.")
    parser.add_argument("--commit", action="store_true", help="Stage and commit with the generated message.")

    args = parser.parse_args()

    if args.commit or args.stage:
        subprocess.run(["git", "add", "."], check=True)

    msg = generate_message(verbose=args.verbose, with_flavor=args.flavor,
                           show_lines=args.show_lines, short=args.short)

    if args.commit:
        subprocess.run(["git", "commit", "-m", msg], check=True)
        print("✅ Changes committed!")
    else:
        print(msg)


if __name__ == "__main__":
    main()