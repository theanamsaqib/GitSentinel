from app.extractor.git_extractor import extract_commits

if __name__ == "__main__":
    repo = "https://github.com/google/gson"

    commits = extract_commits(repo, max_commits=500)

    authors = set()

    for c in commits:
        authors.add(c["author"])

    print("Unique authors:", authors)
    print(f"\nTotal commits extracted: {len(commits)}\n")

    for c in commits[:3]:
        print("Commit:", c["hash"])
        print("Author:", c["author"])
        print("Files changed:", len(c["files"]))
        print("-" * 40)

        author_count = {}

    for c in commits:
        author = c["author"]
        author_count[author] = author_count.get(author, 0) + 1

    print("\nCommits per author:")
    for author, count in author_count.items():
        print(author, "→", count)

        # skewed distribution: a few authors with many commits, many authors with few commits