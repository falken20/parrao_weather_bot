import unittest
from unittest.mock import Mock, patch

import main_db
from models import Location


class TestCreateDefaultLocation(unittest.TestCase):

    @patch("main_db.db.session.commit")
    @patch("main_db.db.session.add")
    @patch("main_db.db.session.get", return_value=None)
    def test_creates_location_when_missing(self, get, add, commit):
        main_db.create_default_location()

        get.assert_called_once_with(Location, 1)
        added_location = add.call_args.args[0]
        self.assertEqual(added_location.id_location, 1)
        self.assertEqual(added_location.desc_location, "Cercedilla")
        commit.assert_called_once_with()

    @patch("main_db.db.session.commit")
    @patch("main_db.db.session.add")
    @patch("main_db.db.session.get")
    def test_does_not_duplicate_existing_location(self, get, add, commit):
        get.return_value = Mock(desc_location="Cercedilla")

        main_db.create_default_location()

        get.assert_called_once_with(Location, 1)
        add.assert_not_called()
        commit.assert_not_called()
