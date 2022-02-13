import os
import tempfile
from unittest.mock import patch

import pytest
from core.models import PokedexCreature
from django.conf import settings
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


@pytest.mark.django_db
def test_import_pokemon_csv(capsys) -> None:
    """Test import pokemon csv file in app directory"""

    call_command("import_csv")
    assert PokedexCreature.objects.count() == 800

    expected = "Nb of creatures imported to the database: 800.\n"
    assert expected == capsys.readouterr().out


@pytest.mark.django_db
def test_import_other_csv_file(capsys) -> None:
    """Test import another CSV file"""

    call_command(
        "import_csv", os.path.join(settings.BASE_DIR, "core/tests/test.csv")
    )
    assert PokedexCreature.objects.count() == 4

    expected = "Nb of creatures imported to the database: 4.\n"
    assert expected == capsys.readouterr().out


@pytest.mark.django_db
def test_import_invalid_csv_file(capsys) -> None:
    """Test import invalid CSV file"""

    with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
        call_command("import_csv", ntf.name)
        expected = "This is not a CSV file.\n"
        assert expected == capsys.readouterr().err
