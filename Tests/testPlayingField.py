from unittest import TestCase
import playingField
import Common.variables as variables


class TestPlayingField(TestCase):
    def test_incorrect_get_empty_cells(self):
        field = playingField.PlayingField()
        expected_output = variables.DEFAULT_FIELD_SIZE ** 2
        field.change_cell_type(1, "Circle")
        self.assertNotEqual(expected_output, len(field.get_empty_cells()))

    def test_correct_get_empty_cells(self):
        field = playingField.PlayingField()
        expected_output = variables.DEFAULT_FIELD_SIZE ** 2
        expected_output_2 = expected_output - 1
        self.assertEqual(expected_output, len(field.get_empty_cells()))
        field.change_cell_type(1, "Circle")
        self.assertEqual(expected_output_2, len(field.get_empty_cells()))

    def test_incorrect_get_number_of_cells(self):
        field = playingField.PlayingField()
        expected_output = 0
        self.assertNotEqual(expected_output, field.get_number_of_cells())

    def test_correct_get_number_of_cells(self):
        field = playingField.PlayingField()
        expected_output = variables.DEFAULT_FIELD_SIZE ** 2
        self.assertEqual(expected_output, field.get_number_of_cells())

    def test_incorrect_get_cell_by_id(self):
        incorrect_input_1 = -1
        incorrect_input_2 = "Not a number"
        field = playingField.PlayingField()
        expected_output = None
        self.assertEqual(expected_output, field.get_cell_by_id(incorrect_input_1))
        self.assertRaises(ValueError, lambda: field.get_cell_by_id(incorrect_input_2))

    def test_correct_get_cell_by_id(self):
        correct_input = 1
        field = playingField.PlayingField()
        self.assertEqual(correct_input, field.get_cell_by_id(correct_input).cell_id)

    def test_incorrect_get_cell_by_x_y(self):
        incorrect_inputx = incorrect_inputy = 1
        x = y = -1
        x_1 = y_1 = "Not a number"
        field = playingField.PlayingField()
        expected_value = 2
        expected_value_2 = None
        self.assertNotEqual(expected_value, field.get_cell_by_x_y(incorrect_inputx, incorrect_inputy).x)
        self.assertNotEqual(expected_value, field.get_cell_by_x_y(incorrect_inputx, incorrect_inputy).y)
        self.assertEqual(expected_value_2, field.get_cell_by_x_y(x, y))
        self.assertRaises(ValueError, lambda: field.get_cell_by_x_y(x_1, y_1))

    def test_correct_get_cell_by_x_y(self):
        correct_inputx = correct_inputy = 1
        field = playingField.PlayingField()
        self.assertEqual(correct_inputx, field.get_cell_by_x_y(correct_inputx, correct_inputy).x)
        self.assertEqual(correct_inputy, field.get_cell_by_x_y(correct_inputx, correct_inputy).y)

    def test_incorrect_clicked_cell(self):
        wrong_inputx = "Not a number"
        wrong_inputy = -1
        expected_output = None
        self.assertRaises(ValueError, lambda: playingField.PlayingField().get_clicked_cell(wrong_inputx, wrong_inputy))
        self.assertEqual(expected_output, playingField.PlayingField().get_clicked_cell(wrong_inputy, wrong_inputy))

    def test_correct_clicked_cell(self):
        correct_input_x = correct_input_y = 1
        expected_output = True
        cell = playingField.PlayingField().get_clicked_cell(correct_input_x, correct_input_y)
        self.assertEqual(expected_output, cell.is_click_inside(correct_input_x, correct_input_y))

    def test_incorrect_input(self):
        incorrect_input = "Not a number"
        expected_output = False
        self.assertEqual(expected_output, playingField.PlayingField._correct_input(incorrect_input))

    def test_correct_input(self):
        correct_input = variables.Iam.Cross.value
        expected_output = True
        self.assertEqual(expected_output, playingField.PlayingField._correct_input(correct_input))

    def test_incorrect_change_cell_type(self):
        field = playingField.PlayingField()
        input_id_1 = "Wrong input"
        input_cell_1 = "Circle"
        input_id_2 = 1
        input_cell_2 = "Not a shape"
        expected_output_1 = False
        expected_output_2 = variables.CellStatus.Cross
        expected_output_3 = variables.CellStatus.Empty
        self.assertRaises(ValueError, lambda: field.change_cell_type(input_id_1, input_cell_1))
        self.assertEqual(expected_output_1, field.change_cell_type(input_id_2, input_cell_2))
        self.assertNotEqual(expected_output_2, field.change_cell_type(input_id_2, input_cell_1).status)
        self.assertNotEqual(expected_output_3, field.change_cell_type(input_id_2, input_cell_1).status)

    def test_correct_change_cell_type(self):
        field = playingField.PlayingField()
        input_id = 1
        input_cell = "Circle"
        expected_output = variables.CellStatus.Circle
        self.assertEqual(expected_output, field.change_cell_type(input_id, input_cell).status)

    def test_incorrect_init(self):
        incorrect_input = "Not a number"
        self.assertRaises(ValueError, lambda: playingField.PlayingField().initialize_field(incorrect_input))

    def test_correct_init(self):
        expected_value_after_initialization = {}  # if it would be different it is ok
        self.assertNotEqual(expected_value_after_initialization, playingField.PlayingField().field_cells)


if __name__ == '__main__':
    import unittest
    unittest.main()
