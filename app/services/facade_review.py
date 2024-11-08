"""
ReviewFacade provides high-level operations for creating, retrieving,
updating, and deleting reviews. This service layer interacts with the
review repository.
"""

from app.models.review import Review


class ReviewFacade():
    """
    Service class for managing review operations, including creation,
    retrieval, updating, and deletion of reviews.
    """

    def __init__(self, selected_repo):
        """
        Initializes the ReviewFacade with a repository.

        Args:
            selected_repo: The repository instance
            to manage review persistence.
        """
        self.review_repo = selected_repo

    # <---------------------------------------------------------------------->

    def create_review(self, review_data):
        """
        Creates a new review.

        Args:
            review_data (dict): Dictionary containing review information,
                                including 'text', 'rating', 'place_id',
                                'place_name', 'user_id',
                                and 'user_first_name'.

        Returns:
            dict: The created review in dictionary form.

        Raises:
            ValueError: If a review with the same ID exists
            or validation fails.
        """
        print(f"Creating review with data: {review_data}")

        review = Review(
            text=review_data["text"],
            rating=review_data["rating"],
            place_id=review_data["place_id"],
            place_name=review_data["place_name"],
            user_id=review_data["user_id"],
            user_first_name=review_data["user_first_name"]
        )

        existing_review = self.review_repo.get_by_attribute("id", review.id)

        if existing_review:
            print(f"review: {review.id} already exists. Please create a new review")
            raise ValueError(f"Review: {review.id}' already exists. Please create a new review.")

        if review.is_valid():
            print(f"Review: {review.id} passed validation.")
            self.review_repo.add(review)
            return review.to_dict()
        
        else:
            print(f"review: {review.id} failed validation.")
            raise ValueError("Invalid review data.")

    #   <-------------------------------------------------------------------->

    def get_all_reviews(self):
        """
        Retrieves all reviews.

        Returns:
            list: A list of all reviews in dictionary form.
        """
        reviews = self.review_repo.get_all()

        return [review.to_dict() for review in reviews]

    #   <-------------------------------------------------------------------->

    def get_review(self, review_id):
        """
        Retrieves a review by ID.

        Args:
            review_id (str): The unique identifier of the review.

        Returns:
            dict: The review data in dictionary form.

        Raises:
            ValueError: If the review is not found.
        """
        review = self.review_repo.get(review_id)

        if review:
            return review.to_dict()
        
        else:
            raise ValueError(f"Review: {review_id} does not exist !")

    #   <-------------------------------------------------------------------->

    def update_review(self, review_id, new_data):
        """
        Updates a review's data.

        Args:
            review_id (str): The unique identifier of the review to update.
            new_data (dict): Dictionary with the updated review information.

        Returns:
            dict: The updated review data in dictionary form.

        Raises:
            ValueError: If the review is not found.
        """
        review = self.review_repo.get(review_id)

        if not review:
            raise ValueError(f"Review with id {review_id} not found")

        new_review = Review(
            text=new_data["text"],
            rating=new_data["rating"],
            place_id=review.place_id,
            place_name=review.place_name,
            user_id=review.user_id,
            user_first_name=review.user_first_name
        )

        if not new_review.is_valid():
            raise ValueError("Review validation failed. Please check the email and other attributes.")

        if review:
            self.review_repo.update(review_id, new_data)

            return review.to_dict()
        else:
            raise ValueError(f"Review: {review_id} not found")


    #   <-------------------------------------------------------------------->

    def delete_review(self, review_id):
        """
        Deletes a review by ID.

        Args:
            review_id (str): The unique identifier of the review to delete.

        Raises:
            ValueError: If the review is not found.
        """
        review = self.review_repo.get(review_id)

        if review:
            print(f"Review: {review} has been deleted")
            self.review_repo.delete(review_id)
            
        else:
            raise ValueError(f"Review: {review_id} not found !")

    #   <-------------------------------------------------------------------->
