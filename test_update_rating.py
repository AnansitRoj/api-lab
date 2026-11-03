import pytest


# Boundaries of stars for an update: 1 and 5 are saved, 0 and 6 are refused.
@pytest.mark.parametrize("stars, expected", [(0, 400), (1, 200), (5, 200), (6, 400)])
def test_update_stars_boundaries(api, auth, rating, stars, expected):
    path = f"/api/ratings/{rating['id']}"
    res = api.put(path, json={"stars": stars}, headers=auth)
    assert res.status_code == expected
    saved = api.get(path, headers=auth).json()
    if expected == 200:
        assert saved["stars"] == stars
    else:
        assert saved["stars"] == rating["stars"]