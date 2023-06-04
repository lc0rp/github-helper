import pytest
from criteria.state import StateCriteria
from criteria.category import CategoryCriteria
from criteria.sort import SortCriteria
from criteria.direction import DirectionCriteria
from criteria.since import SinceCriteria
from criteria.before import BeforeCriteria
from criteria.limit import LimitCriteria

def test_state_criteria():
    state_criteria = StateCriteria.parse("state:open")
    assert state_criteria.state == "open"

    state_criteria = StateCriteria.parse("state:closed")
    assert state_criteria.state == "closed"

    state_criteria = StateCriteria.parse("state:all")
    assert state_criteria.state == "all"

    with pytest.raises(ValueError):
        StateCriteria.parse("state:invalid")

def test_category_criteria():
    category_criteria = CategoryCriteria.parse("category:question")
    assert category_criteria.category == "question"

    category_criteria = CategoryCriteria.parse("category:general")
    assert category_criteria.category == "general"

    with pytest.raises(ValueError):
        CategoryCriteria.parse("category:invalid")

def test_sort_criteria():
    sort_criteria = SortCriteria.parse("sort:created")
    assert sort_criteria.sort == "created"

    sort_criteria = SortCriteria.parse("sort:updated")
    assert sort_criteria.sort == "updated"

    with pytest.raises(ValueError):
        SortCriteria.parse("sort:invalid")

def test_direction_criteria():
    direction_criteria = DirectionCriteria.parse("direction:asc")
    assert direction_criteria.direction == "asc"

    direction_criteria = DirectionCriteria.parse("direction:desc")
    assert direction_criteria.direction == "desc"

    with pytest.raises(ValueError):
        DirectionCriteria.parse("direction:invalid")

def test_since_criteria():
    since_criteria = SinceCriteria.parse("since:2021-01-01T00:00:00Z")
    assert since_criteria.since == "2021-01-01T00:00:00Z"

    with pytest.raises(ValueError):
        SinceCriteria.parse("since:invalid")

def test_before_criteria():
    before_criteria = BeforeCriteria.parse("before:2021-01-31T23:59:59Z")
    assert before_criteria.before == "2021-01-31T23:59:59Z"

    with pytest.raises(ValueError):
        BeforeCriteria.parse("before:invalid")

def test_limit_criteria():
    limit_criteria = LimitCriteria.parse("limit:100")
    assert limit_criteria.limit == 100

    limit_criteria = LimitCriteria.parse("limit:1000")
    assert limit_criteria.limit == 1000

    with pytest.raises(ValueError):
        LimitCriteria.parse("limit:invalid")