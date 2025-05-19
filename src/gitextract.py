import os
import git
import pandas as pd

def extract_file_versions(repo_path: str, file_path: str, output_folder: str) -> pd.DataFrame:
    repo = git.Repo(repo_path)
    file_basename = os.path.basename(file_path)
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # check if file exists in the repository
    if not os.path.exists(os.path.join(repo.working_tree_dir, file_path)):
        raise FileNotFoundError(f"file {file_path} not found in repository {repo_path}")
    else:
        print(f"file {file_path} found in repository {repo_path}")

    commit_data = []

    for commit in repo.iter_commits(paths=file_path):
        commit_id = commit.hexsha[:8]  # Kürzere Commit-ID
        commit_date = commit.committed_datetime.strftime('%Y-%m-%d')
        commit_time = commit.committed_datetime.strftime('%H:%M:%S')
        
        output_file = os.path.join(output_folder, f"{file_basename}_{commit_id}.py")
        
        with open(output_file, "w", encoding="utf-8") as f:
            blob = commit.tree / file_path.replace(os.sep, '/')
            # get the text length of the file
            length = len(blob.data_stream.read().decode("utf-8"))   
            f.write(blob.data_stream.read().decode("utf-8"))
        
        print(f"Snapshot saved: {output_file}")
        
        commit_data.append({
            'commit_id': commit_id,
            'date': commit_date,
            'time': commit_time,
            'file_length': length,
        })

    df = pd.DataFrame(commit_data)
    return df
def analyze_commit_metadata(repo_path: str, file_path: str):
    repo = git.Repo(repo_path)
    commit_data = []
    
    for commit in repo.iter_commits(paths=file_path):
        commit_data.append({
            "date": commit.committed_datetime.date(),
            "day_of_week": commit.committed_datetime.strftime("%A"),
            "time": commit.committed_datetime.time(),
            "user": commit.committer.name,
            "commit_message": commit.message.strip(),
            "commit_id": commit.hexsha[:8],
            "commit_length": len(commit.message.strip())
        })

    df_commits = pd.DataFrame(commit_data)
    return df_commits
# Beispielaufruf
repo_path = r"./"
file_path = r"src/pipelineResearch.py"  # Relativ zum Repository-Root
output_folder = "./data"

df = extract_file_versions(repo_path, file_path, output_folder)
df.to_csv(os.path.join(output_folder, "commit_data.csv"), index=False)
df_commits = analyze_commit_metadata(repo_path, file_path)
df_commits.to_csv(os.path.join(output_folder, "commit_metadata.csv"), index=False)
