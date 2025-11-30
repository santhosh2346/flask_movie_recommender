import os
import pytest
from app.recommender import Recommender
from app.preprocessing import build_and_save, PROCESSED

@pytest.fixture(scope="module")
def recommender():
    if not os.path.exists(PROCESSED) or not os.listdir(PROCESSED):
        build_and_save()
    return Recommender(artifacts_path=PROCESSED)

def test_recommend_by_title(recommender):
    res = recommender.recommend_by_title("The Matrix", n=3)
    assert isinstance(res, list)
    assert len(res) <= 3
    if len(res) > 0:
        assert 'title' in res[0]
