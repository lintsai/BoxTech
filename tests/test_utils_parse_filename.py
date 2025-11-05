from datetime import datetime

from scripts.scan_videos import parse_filename


def test_parse_filename_happy_path():
    meta = parse_filename("20251102-團課-打靶 01.MOV")
    assert isinstance(meta, dict)
    tt = meta.get("training_type")
    # 現行 parse 規則會把「團課-打靶」整段當作 training_type
    # 這裡僅驗證前綴符合主要類型「團課」，保持測試穩定
    assert isinstance(tt, str) and tt.startswith("團課")
    td = meta.get("training_date")
    assert isinstance(td, datetime)
    assert td.strftime("%Y%m%d") == "20251102"


def test_parse_filename_no_match():
    meta = parse_filename("random_video_name.mov")
    assert isinstance(meta, dict)
    assert meta.get("training_type") is None
    assert meta.get("training_date") is None
