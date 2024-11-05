# repo_selector.py
from app.persistence.repository import InMemoryRepository, InFileRepository, SQLAlchemyRepository

class RepoSelector:
    def __init__(self, repo_type="in_memory", file_name="data.json"):
        self.repo_type = repo_type
        self.file_name = file_name

    def select_repo(self, model=None):
        if self.repo_type == "in_file":
            return InFileRepository(self.file_name)
        elif self.repo_type == "in_memory":
            return InMemoryRepository()
        elif self.repo_type == "in_DB":
            if model is None:
                raise ValueError("Model is required for SQLAlchemyRepository")
            return SQLAlchemyRepository(model)
        else:
            raise ValueError(f"Unknown repository type: {self.repo_type}")