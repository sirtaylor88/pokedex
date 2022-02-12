from unittest.mock import patch

from django.core.management import call_command
from django.db.utils import OperationalError


def test_wait_for_db_ready() -> None:
    """Test waiting for db when db is available"""
    with patch("django.db.utils.ConnectionHandler.__getitem__") as gi:
        gi.return_value = True
        call_command("wait_for_db")
        assert gi.call_count == 1


@patch("time.sleep", return_value=True)
def test_wait_for_db(ts):
    """Test waiting for db when db is not available"""
    with patch("django.db.utils.ConnectionHandler.__getitem__") as gi:
        # Simulate 5 failed connections before the connection is established
        gi.side_effect = [OperationalError] * 5 + [True]
        call_command("wait_for_db")
        assert gi.call_count == 6
