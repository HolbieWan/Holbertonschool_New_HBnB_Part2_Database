from app.persistence.repo_selector import RepoSelector
from app.models.review import Review

class ReviewFacade():

    def __init__(self, selected_repo):
        self.review_repo = selected_repo

    # <------------------------------------------------------------------------>

    def create_review(self, review_data):
        print(f"Creating review with data: {review_data}")

        review = Review(
            text = review_data["text"],
            rating = review_data["rating"],
            place_id = review_data["place_id"],
            place_name=review_data["place_name"],
            user_id = review_data["user_id"],
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
        
    #   <------------------------------------------------------------------------>

    def get_all_reviews(self):
        reviews = self.review_repo.get_all()
        return [review.to_dict() for review in reviews]

    #   <------------------------------------------------------------------------>

    def get_review(self, review_id):
        review = self.review_repo.get(review_id)
        if review:
            return review.to_dict() 
        else:
            raise ValueError(f"Review: {review_id} does not exist !")
        
    #   <------------------------------------------------------------------------>

    def update_review(self, review_id, new_data):
        review = self.review_repo.get(review_id)
        if review:
            self.review_repo.update(review_id, new_data)
            return review.to_dict()
        else:
            raise ValueError(f"Review: {review_id} not found")
            
    #   <------------------------------------------------------------------------>

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if review:
            print(f"Review: {review} has been deleted")
            self.review_repo.delete(review_id)
        else:
            raise ValueError(f"Review: {review_id} not found !")
        
    #   <------------------------------------------------------------------------>
