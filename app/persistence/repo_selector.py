"""
RepoSelector module to select and initialize the appropriate repository type.
"""

from app.persistence.repository import InMemoryRepository, InFileRepository, SQLAlchemyRepository


class RepoSelector:
    """
    Selector class to choose and initialize the appropriate repository
    based on configuration.

    Attributes:
        repo_type (str): The type of repository to use ('in_memory',
        'in_file', or 'in_DB').
        file_name (str): The file name for in-file storage,
        defaulting to 'data.json'.
    """

    def __init__(self, repo_type="in_memory", file_name="data.json"):
        """
        Initialize the RepoSelector with a specified repository type
        and optional file name.

        Args:
            repo_type (str): The repository type to use.
            Defaults to 'in_memory'.
            file_name (str): The file name for in-file storage.
            Defaults to 'data.json'.
        """
        self.repo_type = repo_type
        self.file_name = file_name

    def select_repo(self, model=None):
        """
        Select and return the appropriate repository instance,
        based on repo_type.

        Args:
            model (db.Model, optional): SQLAlchemy model,
            required for SQLAlchemyRepository.

        Returns:
            Repository: An instance of the selected repository.

        Raises:
            ValueError: If the repository type is unknown
            or model is not provided for SQLAlchemyRepository.
        """
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
