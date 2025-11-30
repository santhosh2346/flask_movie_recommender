import os
import pytest
from app.recommender import Recommender
from app.preprocessing import build_and_save, PROCESSED

@pytest.fixture(scope="module")
def recommender():
    if not os.path.exists(PROCESSED) or not os.listdir(PROCESSED):
        build_and_save()
    return Recommender(artifacts_path=PROCESSED)

def test_recommend_by_plot(recommender):
    plot = "A hacker discovers a dark simulated reality controlled by machines."
    res = recommender.recommend_by_plot(plot, n=4)
    assert isinstance(res, list)
    assert len(res) <= 4
