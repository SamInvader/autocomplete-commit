import subprocess
import argparse
import random

# Fun endings
FLAVORS = ["🚀 Let's go!", "🔥 Ship it!", "🛠️ Refactor done.", "✅ Clean commit."]


def get_changed_files():
    """Get changed files from git status."""
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True,
        text=True,
        shell=True
    )
    lines = result.stdout.splitlines()
    return [line for line in lines if line]


def get_diff_details(filename):
    """Return added/removed lines for a file."""
    result = subprocess.run(
        ["git", "diff", "--unified=0", filename],
        capture_output=True,
        text=True,
        shell=True
    )
    lines = result.stdout.splitlines()
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

    action_map = {
        "A": "Created",
        "M": "Modified",
        "D": "Deleted",
        "R": "Renamed",
        "C": "Copied",
        "??": "Created new",
    }

    # Short summary
    if short:
        counts = {}
        for change in changes:
            parts = change.strip().split(maxsplit=1)
            status = parts[0]
            action = action_map.get(status, "Changed")
            counts[action] = counts.get(action, 0) + 1
        summary = ", ".join(f"{n} {a}" for a, n in counts.items())
        msg = f"Summary: {summary}"
        if with_flavor:
            msg += " " + random.choice(FLAVORS)
        return msg

    messages = []
    for change in changes:
        parts = change.strip().split(maxsplit=1)
        status = parts[0]
        filename = parts[1] if len(parts) > 1 else "unknown"
        action = action_map.get(status, "Changed")

        if verbose:
            msg = f"{action} file {filename}"
        else:
            msg = f"{action} file(s)"
        messages.append(msg)

        if show_lines and status in ("M", "A"):
            diff_lines = get_diff_details(filename)
            if diff_lines:
                messages.append(f"Changes in {filename}:")
                messages.extend(diff_lines)

    final_msg = "\n".join(messages)
    if with_flavor:
        final_msg += "\n" + random.choice(FLAVORS)

    return final_msg


def main():
    parser = argparse.ArgumentParser(
        description="Generate human-friendly git commit messages.",
        usage="""cli.py [options]

Options:
  --verbose      Show detailed file list
  --show-lines   Show exact added/removed lines
  --flavor       Add a fun ending to the commit message
  --short        Show a 1-line summary of changes
  --stage        Stage all changes before generating the message
  --commit       Stage and commit with the generated message
  -h, --help     Show this help message and exit
"""
    )
    parser.add_argument("--verbose", action="store_true", help="Show detailed file list.")
    parser.add_argument("--show-lines", action="store_true", help="Show exact added/removed lines.")
    parser.add_argument("--flavor", action="store_true", help="Add a fun ending to the commit message.")
    parser.add_argument("--short", action="store_true", help="Show a 1-line summary of changes.")
    parser.add_argument("--stage", action="store_true", help="Stage all changes before generating the message.")
    parser.add_argument("--commit", action="store_true", help="Stage and commit with the generated message.")

    args = parser.parse_args()

    if args.commit or args.stage:
        subprocess.run(["git", "add", "."], check=True, shell=True)

    msg = generate_message(
        verbose=args.verbose,
        with_flavor=args.flavor,
        show_lines=args.show_lines,
        short=args.short
    )

    if args.commit:
        subprocess.run(["git", "commit", "-m", msg], check=True, shell=True)
        print("✅ Changes committed!")
    else:
        print(msg)


if __name__ == "__main__":
    main()
