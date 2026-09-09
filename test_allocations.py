from copy import copy
from datetime import datetime, timedelta, timezone

from main import Batch, OrderLine

tomorrow: datetime = datetime.now(tz=timezone.utc) + timedelta(days=1)


def make_batch_order_line():
    return Batch(100, "abc123", "Book Case", 20, tomorrow), OrderLine(123, "abc123", 5)


def test_can_allocate_if_skus_match():
    batch, order_line = make_batch_order_line()
    batch.allocate(order_line)
    expected_result = Batch(100, "abc123", "Book Case", 15, tomorrow, {123})

    assert batch != Batch(100, "abc123", "Book Case", 20, tomorrow, {123})
    assert batch != Batch(100, "abc123", "Book Case", 20, tomorrow)
    assert batch == expected_result


def test_cannot_allocate_if_skus_mismatch():
    batch, order_line = make_batch_order_line()
    order_line.qty = 2
    order_line.sku = "def456"
    batch.allocate(order_line)
    expected_result = Batch(100, "abc123", "Book Case", 20, tomorrow)

    assert batch != Batch(100, "abc123", "Book Case", 18, tomorrow, {123})
    assert batch != Batch(100, "abc123", "Book Case", 20, tomorrow, {123})
    assert batch == expected_result


def test_cannot_allocate_if_batch_qty_insufficient():
    batch, order_line = make_batch_order_line()
    batch.qty = 4
    batch.allocate(order_line)
    expected_result = Batch(100, "abc123", "Book Case", 4, tomorrow)
    assert batch != Batch(100, "abc123", "Book Case", -1, tomorrow, {123})
    assert batch != Batch(100, "abc123", "Book Case", 4, tomorrow, {123})
    assert batch == expected_result


def test_cannot_allocate_if_order_already_allocated():
    batch, order_line_1 = make_batch_order_line()
    batch.allocate(order_line_1)
    expected_result = Batch(100, "abc123", "Book Case", 15, tomorrow, {123})
    assert batch == expected_result
    batch.allocate(order_line_1)
    assert batch == expected_result


def test_can_deallocate_on_matching_order_ref():
    batch, order_line = make_batch_order_line()
    expected_result = copy(batch)
    batch.allocate(order_line)
    batch.deallocate(order_line)
    assert batch == expected_result
    assert batch != Batch(100, "abc123", "Book Case", 15, tomorrow, {123})


def test_cannot_deallocate_on_mismatching_order_ref():
    batch, order_line = make_batch_order_line()
    batch.allocate(order_line)
    expected_result = copy(batch)
    order_line.ref = 124
    batch.deallocate(order_line)
    assert batch == expected_result
    assert batch != Batch(100, "abc123", "Book Case", 20, tomorrow)
