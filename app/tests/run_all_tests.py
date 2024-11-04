import unittest

from app.tests.tests_models.test_user_model import TestUserModel
from app.tests.tests_models.test_place_model import TestPlaceModel
from app.tests.tests_models.test_amenity_model import TestAmenityModel
from app.tests.tests_models.test_review_model import TestReviewModel

from app.tests.tests_facades.test_user_facade import TestUserFacade
from app.tests.tests_facades.test_place_facade import TestPlaceFacade
from app.tests.tests_facades.test_amenity_facade import TestAmenityFacade
from app.tests.tests_facades.test_review_facade import TestReviewFacade
from app.tests.tests_facades.test_relations_manager_facade import TestFacadeRelationManager

from app.tests.tests_endpoints.base_test import BaseTestCase
from app.tests.tests_endpoints.test_user_endpoints import TestUserEndpoints
from app.tests.tests_endpoints.test_place_endpoints import TestPlaceEndpoints
from app.tests.tests_endpoints.test_amenity_endpoints import TestAmenityEndpoints
from app.tests.tests_endpoints.test_review_endpoints import TestReviewEndpoints


if __name__ == '__main__':
    unittest.main()