from unittest import TestCase
import Common.functions as functions


class TestFunctions(TestCase):
    def test_incorrect_remove_key(self):
        input_1 = {1: "One", 2: "Two"}
        key_1 = 1
        input_2 = [1, 2, 3]
        key_2 = 3
        input_3 = "This is not a dictionary"
        self.assertNotEqual(input_1, functions.remove_key(input_1, key_1))
        self.assertRaises(ValueError, lambda: functions.remove_key(input_2, key_2))
        self.assertRaises(ValueError, lambda: functions.remove_key(input_1, key_2))
        self.assertRaises(ValueError, lambda: functions.remove_key(input_3, key_1))

    def test_correct_remove_key(self):
        valid_input_1 = {1: "One", 2: "Two", 3: "Three"}
        valid_input_1_key = 1
        valid_input_2 = {"One": 1, "Two": 2}
        valid_input_2_key = "One"
        valid_input_3 = {1.1: "One.One"}
        valid_input_3_key = 1.1
        expected_output_1 = {2: "Two", 3: "Three"}
        expected_output_2 = {"Two": 2}
        expected_output_3 = {}
        self.assertEqual(expected_output_1, functions.remove_key(valid_input_1, valid_input_1_key))
        self.assertEqual(expected_output_2, functions.remove_key(valid_input_2, valid_input_2_key))
        self.assertEqual(expected_output_3, functions.remove_key(valid_input_3, valid_input_3_key))

    def test_incorrect_numbers(self):
        invalid_input_1 = "Almost"
        invalid_input_2 = ["this is so wrong."]
        invalid_input_3 = {0: "And also this."}
        invalid_input_4 = None
        invalid_input_5 = [1, "a", "b", "c", "d"]
        self.assertRaises(ValueError, lambda: functions.are_numbers(invalid_input_1))
        self.assertRaises(ValueError, lambda: functions.are_numbers(invalid_input_2))
        self.assertRaises(ValueError, lambda: functions.are_numbers(invalid_input_3))
        self.assertRaises(ValueError, lambda: functions.are_numbers(invalid_input_4))
        self.assertRaises(ValueError, lambda: functions.are_numbers(invalid_input_5))

    def test_correct_numbers(self):
        valid_input_1 = [1, 2, 3]
        valid_input_2 = [1.0, 2.0, 3.0]
        valid_input_3 = [1, 2.0, 3]
        valid_input_4 = []
        expected_output = True
        self.assertEqual(expected_output, functions.are_numbers(valid_input_1))
        self.assertEqual(expected_output, functions.are_numbers(valid_input_2))
        self.assertEqual(expected_output, functions.are_numbers(valid_input_3))
        self.assertEqual(expected_output, functions.are_numbers(valid_input_4))

    def test_correct_number(self):
        valid_input_1 = 1
        valid_input_2 = 1.0
        expected_output = True
        self.assertEqual(expected_output, functions.is_number(valid_input_1))
        self.assertEqual(expected_output, functions.is_number(valid_input_2))

    def test_incorrect_number(self):
        invalid_input_1 = "Almost"
        invalid_input_2 = ["this is so wrong."]
        invalid_input_3 = {0: "And also this."}
        invalid_input_4 = None
        self.assertRaises(ValueError, lambda: functions.is_number(invalid_input_1))
        self.assertRaises(ValueError, lambda: functions.is_number(invalid_input_2))
        self.assertRaises(ValueError, lambda: functions.is_number(invalid_input_3))
        self.assertRaises(ValueError, lambda: functions.is_number(invalid_input_4))

    def test_incorrect_float(self):
        invalid_input_1 = 0
        invalid_input_2 = ["this is so wrong."]
        invalid_input_3 = {0: "And also this."}
        invalid_input_4 = None
        invalid_input_5 = "Almost"
        expected_output = False
        self.assertEqual(expected_output, functions.is_float(invalid_input_1))
        self.assertEqual(expected_output, functions.is_float(invalid_input_2))
        self.assertEqual(expected_output, functions.is_float(invalid_input_3))
        self.assertEqual(expected_output, functions.is_float(invalid_input_4))
        self.assertEqual(expected_output, functions.is_float(invalid_input_5))

    def test_correct_float(self):
        valid_input = 1.0
        expected_output = True
        self.assertEqual(expected_output, functions.is_float(valid_input))

    def test_incorrect_int(self):
        invalid_input_1 = "Zero"
        invalid_input_2 = ["this is so wrong."]
        invalid_input_3 = {0: "And also this."}
        invalid_input_4 = None
        invalid_input_5 = 1.0
        expected_output = False
        self.assertEqual(expected_output, functions.is_int(invalid_input_1))
        self.assertEqual(expected_output, functions.is_int(invalid_input_2))
        self.assertEqual(expected_output, functions.is_int(invalid_input_3))
        self.assertEqual(expected_output, functions.is_int(invalid_input_4))
        self.assertEqual(expected_output, functions.is_int(invalid_input_5))

    def test_correct_int(self):
        valid_input = 0
        expected_output = True
        self.assertEqual(expected_output, functions.is_int(valid_input))

    def test_correct_string(self):
        valid_input = "This is the correct input."
        expected_output = True
        self.assertEqual(expected_output, functions.is_string(valid_input))

    def test_incorrect_string(self):
        invalid_input_1 = 1
        invalid_input_2 = ["this is so wrong."]
        invalid_input_3 = {0: "And also this."}
        invalid_input_4 = None
        invalid_input_5 = 1.0
        expected_output = False
        self.assertEqual(expected_output, functions.is_string(invalid_input_1))
        self.assertEqual(expected_output, functions.is_string(invalid_input_2))
        self.assertEqual(expected_output, functions.is_string(invalid_input_3))
        self.assertEqual(expected_output, functions.is_string(invalid_input_4))
        self.assertEqual(expected_output, functions.is_string(invalid_input_5))


if __name__ == '__main__':
    import unittest
    unittest.main()
