import pytest
from photo_print_order import extra_print_charge, order_valid, dispatch_status


# ---------- extra_print_charge ----------

def test_unknown_print_size_raises():
    with pytest.raises(ValueError, match="unknown print size"):
        extra_print_charge("A4", 10, "matte", False)

def test_negative_copies_raises():
    with pytest.raises(ValueError, match="invalid copies"):
        extra_print_charge("4x6", -1, "matte", False)

def test_within_included_prints():
    assert extra_print_charge("4x6", 15, "matte", False) == 0

def test_member_bonus_matte():
    # 4x6 member: 20 + 5 included, 5 extra at matte rate 4
    assert extra_print_charge("4x6", 30, "matte", True) == 20

def test_glossy_rate():
    # 5x7: 15 included, 5 extra at non-matte rate 7
    assert extra_print_charge("5x7", 20, "glossy", False) == 35

def test_bulk_canvas_surcharge():
    # 8x10: 10 included, 60 extra at rate 7 + 2 + 5 = 14
    assert extra_print_charge("8x10", 70, "canvas", False) == 840


# ---------- order_valid ----------

def test_rush_order_valid():
    assert order_valid(10, 40, True) is True

def test_large_file_invalid():
    assert order_valid(30, 10, False) is False

def test_order_valid():
    assert order_valid(10, 100, False) is True


# ---------- dispatch_status ----------

def test_framed_on_time():
    assert dispatch_status(30, True, False) == "on_time"

def test_unframed_tight():
    assert dispatch_status(8, False, False) == "tight"

def test_international_missed():
    assert dispatch_status(10, False, True) == "missed"
