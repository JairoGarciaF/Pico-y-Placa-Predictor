import re
from datetime import datetime

class Vehicle:
    def __init__(self, license_plate: str):
        self.license_plate = license_plate

    def get_last_digit(self):
        # Gets the last digit of the plate
        return int(self.license_plate[-1])

class DateTime:
    def __init__(self, date_str: str, time_str: str):
        # Date format 'YYYY-MM-DD' and hour format 'HH:MM'
        self.date = datetime.strptime(date_str, "%Y-%m-%d")
        self.time = datetime.strptime(time_str, "%H:%M").time()


class PicoYPlacaPredictor:
    def __init__(self):
        self.restricted_days = {
            1: "Monday",
            2: "Monday",
            3: "Tuesday",
            4: "Tuesday",
            5: "Wednesday",
            6: "Wednesday",
            7: "Thursday",
            8: "Thursday",
            9: "Friday",
            0: "Friday"
        }

    def validate_license_plate(self, plate):
        # Validates the first letter of the plate with 3 letters and 3-4 numbers
        # Regular expression for the first letter of the plate
        pattern = r"^[A-Z]{3}-\d{3,4}$"
        if re.match(pattern, plate):
            valid_provinces = "AUECHXOGIRLWMPYJKSTZVNBQ"  # Valid letters of the provinces
            return plate[0] in valid_provinces
        return False

    def validate_date(self, date_str):
        try:
            datetime.strptime(date_str, "%d-%m-%Y")
            return True
        except ValueError:
            return False

    def validate_time(self, time_str):
        try:
            datetime.strptime(time_str, "%H:%M")
            return True
        except ValueError:
            return False

    def is_restricted(self, license_plate, date_str, time_str):
        # Validation of the plate, date and hour
        if not self.validate_license_plate(license_plate):
            return "Invalid license plate format. Please enter a valid one (e.g., ABC-1234)."

        if not self.validate_date(date_str):
            return "Invalid date format. Please enter a valid date (DD-MM-YYYY)."

        if not self.validate_time(time_str):
            return "Invalid time format. Please enter a valid time (HH:MM)."

        last_digit = int(license_plate[-1])
        date_obj = datetime.strptime(date_str, "%d-%m-%Y")
        time_obj = datetime.strptime(time_str, "%H:%M").time()

        restricted_day = self.restricted_days[last_digit]
        restricted_morning = time_obj >= datetime.strptime("07:00", "%H:%M").time() and time_obj <= datetime.strptime(
            "09:30", "%H:%M").time()
        restricted_evening = time_obj >= datetime.strptime("16:00", "%H:%M").time() and time_obj <= datetime.strptime(
            "19:30", "%H:%M").time()

        if date_obj.strftime("%A") == restricted_day and (restricted_morning or restricted_evening):
            return "This car CANNOT be on the road during this time."

        return "This car CAN be on the road during this time."


def get_user_input():
    predictor = PicoYPlacaPredictor()

    # Input of the plate
    while True:
        plate = input("Enter the license plate (e.g., ABC-1234): ").strip().upper()
        if predictor.validate_license_plate(plate):
            break
        print("Invalid license plate. Please use the format ABC-1234 with valid letters and numbers.")

    # Input of the date
    while True:
        date_str = input("Enter the date (DD-MM-YYYY): ").strip()
        if predictor.validate_date(date_str):
            break
        print("Invalid date. Please use the format DD-MM-YYYY.")

    # Input of the hour
    while True:
        time_str = input("Enter the time (HH:MM): ").strip()
        if predictor.validate_time(time_str):
            break
        print("Invalid time. Please use the format HH:MM.")

    # Validate if the car can be on the road
    result = predictor.is_restricted(plate, date_str, time_str)
    print(result)


if __name__ == "__main__":
    get_user_input()

