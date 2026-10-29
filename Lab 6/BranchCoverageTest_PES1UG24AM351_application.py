import pytest
from photo_print_order import extra_print_charge, order_valid, dispatch_status


# ---------- extra_print_charge ----------

def test_unknown_print_size_raises():
    with pytest.raises(ValueError, match="unknown print size"):
        extra_print_charge("A4", 10, "matte", False)

def test_negative_copies_raises():
    with pytest.raises(ValueError, match="invalid copies"):
        extra_print_charge("4x6", -1, "matte", False)

def test_zero_copies_no_charge():
    assert extra_print_charge("4x6", 0, "matte", False) == 0

def test_within_included_prints():
    assert extra_print_charge("4x6", 15, "matte", False) == 0

def test_exactly_included_prints_no_charge():
    assert extra_print_charge("5x7", 15, "glossy", False) == 0

def test_member_bonus_covers_extra_prints():
    # 4x6 member gets 25 included, so 25 copies cost nothing
    assert extra_print_charge("4x6", 25, "matte", True) == 0

def test_member_bonus_matte():
    # 4x6 member: 25 included, 5 extra at matte rate 4
    assert extra_print_charge("4x6", 30, "matte", True) == 20

def test_member_8x10_gets_no_bonus():
    # 8x10 member: still only 10 included, 5 extra at matte rate 4
    assert extra_print_charge("8x10", 15, "matte", True) == 20

def test_glossy_rate():
    # 5x7: 15 included, 5 extra at non-matte rate 7
    assert extra_print_charge("5x7", 20, "glossy", False) == 35

def test_exactly_50_extra_no_bulk_surcharge():
    # 4x6: 20 included, 50 extra at rate 7, no bulk surcharge
    assert extra_print_charge("4x6", 70, "glossy", False) == 350

def test_bulk_matte_surcharge():
    # 4x6: 60 extra at rate 4 + 2 = 6
    assert extra_print_charge("4x6", 80, "matte", False) == 360

def test_bulk_glossy_surcharge_no_canvas():
    # 5x7: 51 extra at rate 7 + 2 = 9
    assert extra_print_charge("5x7", 66, "glossy", False) == 459

def test_bulk_canvas_surcharge():
    # 8x10: 60 extra at rate 7 + 2 + 5 = 14
    assert extra_print_charge("8x10", 70, "canvas", False) == 840

def test_canvas_without_bulk_uses_base_rate():
    # 8x10: 5 extra, canvas only adds surcharge above 50 extra
    assert extra_print_charge("8x10", 15, "canvas", False) == 35


# ---------- order_valid ----------

def test_rush_order_valid():
    assert order_valid(10, 40, True) is True

def test_rush_order_at_limit():
    assert order_valid(10, 50, True) is True

def test_rush_order_too_many_copies():
    assert order_valid(10, 51, True) is False

def test_rush_order_ignores_file_size():
    assert order_valid(100, 10, True) is True

def test_large_file_invalid():
    assert order_valid(30, 10, False) is False

def test_file_size_at_limit():
    assert order_valid(25, 10, False) is True

def test_order_valid():
    assert order_valid(10, 100, False) is True

def test_copies_at_limit():
    assert order_valid(10, 500, False) is True

def test_too_many_copies():
    assert order_valid(10, 501, False) is False


# ---------- dispatch_status ----------

def test_framed_on_time():
    assert dispatch_status(30, True, False) == "on_time"

def test_framed_tight():
    # cutoff 24, tight window 18-23
    assert dispatch_status(20, True, False) == "tight"

def test_framed_missed():
    assert dispatch_status(17, True, False) == "missed"

def test_unframed_on_time_at_cutoff():
    assert dispatch_status(12, False, False) == "on_time"

def test_unframed_tight():
    assert dispatch_status(8, False, False) == "tight"

def test_unframed_tight_at_lower_bound():
    assert dispatch_status(6, False, False) == "tight"

def test_unframed_missed():
    assert dispatch_status(5, False, False) == "missed"

def test_international_on_time():
    # cutoff 12 + 24 = 36
    assert dispatch_status(36, False, True) == "on_time"

def test_international_tight():
    assert dispatch_status(32, False, True) == "tight"

def test_international_missed():
    assert dispatch_status(10, False, True) == "missed"

def test_framed_international_on_time():
    # cutoff 24 + 24 = 48
    assert dispatch_status(48, True, True) == "on_time"

def test_framed_international_tight():
    assert dispatch_status(45, True, True) == "tight"
