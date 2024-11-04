from app.persistence.repository import InMemoryRepository, InFileRepository

class RepoSelector:
    def __init__(self, repo_type="in_memory", file_name="data.json"):
        self.repo_type = repo_type
        self.file_name = file_name

    def select_repo(self):
        if self.repo_type == "in_file":
            return InFileRepository(self.file_name)
        elif self.repo_type == "in_memory":
            return InMemoryRepository()
        else:
            raise ValueError(f"Unknown repository type: {self.repo_type}")