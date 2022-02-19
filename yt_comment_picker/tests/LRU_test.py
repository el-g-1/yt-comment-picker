from yt_comment_picker.LRU import LRUCache


def test_lru_put_and_get():
    c = LRUCache(100)
    c.put(6, 10)
    assert c.get(6) == 10


def test_lru_removed_first_added():
    c = LRUCache(2)
    c.put(6, 10)
    c.put(3, 42)
    c.put(100, -5)
    assert c.get(6) is None


def test_lru_removed_oldest():
    c = LRUCache(2)
    c.put(6, 10)
    c.put(3, 42)
    assert c.get(6) == 10
    c.put(100, -5)
    assert c.get(3) is None
    assert c.get(100) == -5
    assert c.get(6) == 10
