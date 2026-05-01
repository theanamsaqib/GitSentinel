from pydriller import Repository

def extract_commits(repo_url, max_commits=20):
    data = []

    for i, commit in enumerate(Repository(repo_url).traverse_commits()):
        if i >= max_commits:
            break

        commit_data = {
            "hash": commit.hash,
            "author": commit.author.name,
            "date": str(commit.committer_date),
            "files": []
        }

        for mod in commit.modified_files:
            commit_data["files"].append({
                "filename": mod.filename,
                "added": mod.added_lines,
                "deleted": mod.deleted_lines
            })

        data.append(commit_data)

    return data