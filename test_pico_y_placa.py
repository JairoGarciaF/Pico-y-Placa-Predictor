import unittest
from pico_y_placa import PicoYPlacaPredictor


class TestPicoYPlacaPredictor(unittest.TestCase):

    def setUp(self):
        self.predictor = PicoYPlacaPredictor()

    # Test valid plates
    def test_validate_license_plate_valid(self):
        self.assertTrue(self.predictor.validate_license_plate("ABC-1234"))
        self.assertTrue(self.predictor.validate_license_plate("PQR-987"))

    # Test invalid plates
    def test_validate_license_plate_invalid(self):
        self.assertFalse(self.predictor.validate_license_plate("DYZ-123"))  # invalid letters
        self.assertFalse(self.predictor.validate_license_plate("ABC1234"))  # no middle hyphen
        self.assertFalse(self.predictor.validate_license_plate("ABCD-1234"))  # more than 3 letters
        self.assertFalse(self.predictor.validate_license_plate("ABC-12"))  # less than 3 numbers
        self.assertFalse(self.predictor.validate_license_plate("123-4567"))  # no letters

    # Test valid date
    def test_validate_date_valid(self):
        self.assertTrue(self.predictor.validate_date("14-09-2024"))

    # Test invalid date
    def test_validate_date_invalid(self):
        self.assertFalse(self.predictor.validate_date("2024-09-14"))  # invalid format
        self.assertFalse(self.predictor.validate_date("2024/09/14"))  # invalid format
        self.assertFalse(self.predictor.validate_date("2024-13-01"))  # invalid month

    # Test valid hour
    def test_validate_time_valid(self):
        self.assertTrue(self.predictor.validate_time("7:11"))
        self.assertTrue(self.predictor.validate_time("08:00"))
        self.assertTrue(self.predictor.validate_time("16:30"))

    # Test invalid hour
    def test_validate_time_invalid(self):
        self.assertFalse(self.predictor.validate_time("16:70"))  # invalid minutes
        self.assertFalse(self.predictor.validate_time("25:00"))  # invalid hour

    # Test restricted vehicles
    def test_is_restricted_true(self):
        # Digit 4, restricted day: Tuesday
        self.assertEqual(self.predictor.is_restricted("ABC-1234", "17-09-2024", "07:30"),
                         "This car CANNOT be on the road during this time.")
        # Digit 6, restricted day: Wednesday
        self.assertEqual(self.predictor.is_restricted("PQR-9876", "18-09-2024", "17:00"),
                         "This car CANNOT be on the road during this time.")

    # Test allowed vehicles (day and hour)
    def test_is_restricted_false(self):
        # Digit 4, allowed on Wednesday
        self.assertEqual(self.predictor.is_restricted("ABC-1234", "18-09-2024", "08:30"),
                         "This car CAN be on the road during this time.")
        # Digit 5, restricted on Wednesday, but outside rush hour
        self.assertEqual(self.predictor.is_restricted("PQR-1235", "18-09-2024", "15:00"),
                         "This car CAN be on the road during this time.")

    # Test error messages
    def test_invalid_plate_message(self):
        result = self.predictor.is_restricted("123-4567", "14-09-2024", "08:00")
        self.assertEqual(result, "Invalid license plate format. Please enter a valid one (e.g., ABC-1234).")

    def test_invalid_date_message(self):
        result = self.predictor.is_restricted("ABC-1234", "2024-09-14", "08:00")
        self.assertEqual(result, "Invalid date format. Please enter a valid date (DD-MM-YYYY).")

    def test_invalid_time_message(self):
        result = self.predictor.is_restricted("ABC-1234", "14-09-2024", "O7:00")
        self.assertEqual(result, "Invalid time format. Please enter a valid time (HH:MM).")


if __name__ == "__main__":
    unittest.main()