from unittest import TestCase
import playingField
import Common.variables as variables
from endValidator import EndValidator


class TestEndValidator(TestCase):
    def test_correct_check_for_the_end(self):
        field = playingField.PlayingField()
        field.initialize_field(3)
        c1 = field.get_cell_by_id(0)
        expected_output = None
        self.assertEqual(expected_output, EndValidator.check_for_the_end(field, c1))

        def _fill_line(line):
            field.change_cell_type(0 + line * 3, "Cross")
            field.change_cell_type(1 + line * 3, "Cross")
            field.change_cell_type(2 + line * 3, "Cross")

        _fill_line(0), _fill_line(1), _fill_line(2)  # fill the entire grid
        self.assertEqual(3, len(EndValidator.check_for_the_end(field, field.get_cell_by_id(0))))
        self.assertEqual(3, len(EndValidator.check_for_the_end(field, field.get_cell_by_id(0))))
        self.assertEqual(3, len(EndValidator.check_for_the_end(field, field.get_cell_by_id(0))))
        self.assertEqual(3, len(EndValidator.check_for_the_end(field, field.get_cell_by_id(2))))

    def test_incorrect_win(self):
        incorrect_input_1 = "One"
        incorrect_input_2 = 0
        incorrect_input_3 = {1: "One", 2: "Two", 3: "Three"}
        correct_columns = 3
        self.assertRaises(ValueError, lambda: EndValidator._win(incorrect_input_1, correct_columns))
        self.assertRaises(ValueError, lambda: EndValidator._win(incorrect_input_2, correct_columns))
        self.assertRaises(ValueError, lambda: EndValidator._win(incorrect_input_3, correct_columns))
        self.assertRaises(ValueError, lambda: EndValidator._win(incorrect_input_3, incorrect_input_1))

    def test_correct_win(self):
        field = playingField.PlayingField()
        field.initialize_field(3)
        c1 = field.change_cell_type(0, "Cross")
        c2 = field.change_cell_type(1, "Cross")
        c3 = field.change_cell_type(2, "Cross")
        correct_columns = 3
        correct_input_1 = []
        correct_input_2 = [c1]
        correct_input_3 = [c1, c2]
        correct_input_4 = [c1, c2, c3]
        expected_output_true = True
        expected_output_false = False
        self.assertEqual(expected_output_false, EndValidator._win(correct_input_1, correct_columns))
        self.assertEqual(expected_output_false, EndValidator._win(correct_input_2, correct_columns))
        self.assertEqual(expected_output_false, EndValidator._win(correct_input_3, correct_columns))
        self.assertEqual(expected_output_true, EndValidator._win(correct_input_4, correct_columns))

    def test_incorrect_check_column(self):
        field = playingField.PlayingField()
        field.initialize_field(3)
        incorrect_input_1 = "Not a number"
        self.assertRaises(ValueError, lambda: EndValidator._check_column(field, incorrect_input_1, 1))
        self.assertRaises(ValueError, lambda: EndValidator._check_column(field, 1, incorrect_input_1))

        def _fill_column_wrong(column):
            c1 = field.change_cell_type(column, "Cross")
            c2 = field.change_cell_type(column + 3, "Circle")
            c3 = field.change_cell_type(column + 6, "Cross")
            return [c1, c2, c3]

        self.assertNotEqual(_fill_column_wrong(0), EndValidator._check_column(field, 3, 0))
        self.assertNotEqual(_fill_column_wrong(1), EndValidator._check_column(field, 3, 1))
        self.assertNotEqual(_fill_column_wrong(2), EndValidator._check_column(field, 3, 2))

    def test_correct_check_column(self):
        field = playingField.PlayingField()
        field.initialize_field(3)
        expected_output = []
        result_1 = EndValidator._check_column(field, 3, 0)
        result_2 = EndValidator._check_column(field, 3, 1)
        result_3 = EndValidator._check_column(field, 3, 2)
        self.assertEqual(expected_output, result_1)
        self.assertEqual(expected_output, result_2)
        self.assertEqual(expected_output, result_3)

        def _fill_column(column):
            c1 = field.change_cell_type(column, "Cross")
            c2 = field.change_cell_type(column + 3, "Cross")
            c3 = field.change_cell_type(column + 6, "Cross")
            return [c1, c2, c3]

        self.assertEqual(_fill_column(0), EndValidator._check_column(field, 3, 0))
        self.assertEqual(_fill_column(1), EndValidator._check_column(field, 3, 1))
        self.assertEqual(_fill_column(2), EndValidator._check_column(field, 3, 2))

    def test_incorrect_check_line(self):
        field = playingField.PlayingField()
        field.initialize_field(3)
        incorrect_input_1 = "Not a number"
        self.assertRaises(ValueError, lambda: EndValidator._check_line(field, incorrect_input_1, 1))
        self.assertRaises(ValueError, lambda: EndValidator._check_line(field, 1, incorrect_input_1))

        def _fill_line_wrong(line):
            c1 = field.change_cell_type(0 + line * 3, "Cross")
            c2 = field.change_cell_type(1 + line * 3, "Circle")
            c3 = field.change_cell_type(2 + line * 3, "Cross")
            return [c1, c2, c3]

        self.assertNotEqual(_fill_line_wrong(0), EndValidator._check_line(field, 3, 0))
        self.assertNotEqual(_fill_line_wrong(1), EndValidator._check_line(field, 3, 1))
        self.assertNotEqual(_fill_line_wrong(2), EndValidator._check_line(field, 3, 2))

    def test_correct_check_line(self):
        field = playingField.PlayingField()
        field.initialize_field(3)
        expected_output = []
        result_1 = EndValidator._check_line(field, 3, 0)
        result_2 = EndValidator._check_line(field, 3, 1)
        result_3 = EndValidator._check_line(field, 3, 2)
        self.assertEqual(expected_output, result_1)
        self.assertEqual(expected_output, result_2)
        self.assertEqual(expected_output, result_3)

        def _fill_line(line):
            c1 = field.change_cell_type(0 + line * 3, "Cross")
            c2 = field.change_cell_type(1 + line * 3, "Cross")
            c3 = field.change_cell_type(2 + line * 3, "Cross")
            return [c1, c2, c3]

        self.assertEqual(_fill_line(0), EndValidator._check_line(field, 3, 0))
        self.assertEqual(_fill_line(1), EndValidator._check_line(field, 3, 1))
        self.assertEqual(_fill_line(2), EndValidator._check_line(field, 3, 2))

    def test_incorrect_check_increasing_diagonal(self):
        field = playingField.PlayingField()
        incorrect_input = "Not a number"
        expected_output = variables.DEFAULT_FIELD_SIZE
        result = EndValidator._check_decreasing_diagonal(field, variables.DEFAULT_FIELD_SIZE)
        self.assertNotEqual(expected_output, len(result))
        self.assertRaises(ValueError, lambda: EndValidator._check_increasing_diagonal(field, incorrect_input))
        field.initialize_field(3)
        field.change_cell_type(2, "Cross")
        field.change_cell_type(4, "Cross")
        field.change_cell_type(6, "Circle")
        expected_output = []
        self.assertEqual(expected_output, EndValidator._check_increasing_diagonal(field, variables.DEFAULT_FIELD_SIZE))

    def test_correct_check_increasing_diagonal(self):
        field = playingField.PlayingField()
        expected_output = []
        self.assertEqual(expected_output, EndValidator._check_increasing_diagonal(field, variables.DEFAULT_FIELD_SIZE))
        field.initialize_field(3)
        c1 = field.change_cell_type(2, "Cross")
        c2 = field.change_cell_type(4, "Cross")
        c3 = field.change_cell_type(6, "Cross")
        expected_output = [c1, c2, c3]
        self.assertEqual(expected_output, EndValidator._check_increasing_diagonal(field, 3))

    def test_incorrect_check_decreasing_diagonal(self):
        field = playingField.PlayingField()
        incorrect_input = "Not a number"
        expected_output = variables.DEFAULT_FIELD_SIZE
        result = EndValidator._check_decreasing_diagonal(field, variables.DEFAULT_FIELD_SIZE)
        self.assertNotEqual(expected_output, len(result))
        self.assertRaises(ValueError, lambda: EndValidator._check_decreasing_diagonal(field, incorrect_input))
        field.initialize_field(3)
        field.change_cell_type(0, "Cross")
        field.change_cell_type(4, "Cross")
        field.change_cell_type(8, "Circle")
        expected_output = []
        self.assertEqual(expected_output, EndValidator._check_decreasing_diagonal(field, variables.DEFAULT_FIELD_SIZE))

    def test_correct_check_decreasing_diagonal(self):
        field = playingField.PlayingField()
        expected_output = []
        self.assertEqual(expected_output, EndValidator._check_decreasing_diagonal(field, variables.DEFAULT_FIELD_SIZE))
        field.initialize_field(3)
        c1 = field.change_cell_type(0, "Cross")
        c2 = field.change_cell_type(4, "Cross")
        c3 = field.change_cell_type(8, "Cross")
        expected_output = [c1, c2, c3]
        self.assertEqual(expected_output, EndValidator._check_decreasing_diagonal(field, 3))


if __name__ == '__main__':
    import unittest
    unittest.main()
