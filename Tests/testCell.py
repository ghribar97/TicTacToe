import cell
from unittest import TestCase
from Common.variables import CellStatus


class TestCell(TestCase):
    def test_incorrect_cell_status_change(self):
        input_empty_cell = CellStatus.Empty
        input_cross_cell = CellStatus.Cross
        input_circle_cell = CellStatus.Circle
        c = cell.Cell(0, 0, 0, 0, 0, 0, 0)
        self.assertNotEqual(c.change_cell_type(input_empty_cell), input_circle_cell)
        self.assertNotEqual(c.change_cell_type(input_empty_cell), input_cross_cell)
        self.assertNotEqual(c.change_cell_type(input_circle_cell), input_empty_cell)
        self.assertNotEqual(c.change_cell_type(input_circle_cell), input_cross_cell)
        self.assertNotEqual(c.change_cell_type(input_cross_cell), input_circle_cell)
        self.assertNotEqual(c.change_cell_type(input_cross_cell), input_empty_cell)

    def test_correct_cell_status_change(self):
        input_empty_cell = CellStatus.Empty
        input_cross_cell = CellStatus.Cross
        input_circle_cell = CellStatus.Circle
        c = cell.Cell(0, 0, 0, 0, 0, 0, 0)
        self.assertEqual(c.change_cell_type(input_empty_cell), c.status)
        self.assertEqual(c.change_cell_type(input_circle_cell), c.status)
        self.assertEqual(c.change_cell_type(input_cross_cell), c.status)

    def test_incorrect_click_inside(self):
        input_x = 1
        input_y = 1
        x1 = y1 = cell_id = x = y = 2
        x2 = y2 = 2
        c = cell.Cell(x1, y1, x2, y2, cell_id, x, y)
        expected_output = False
        self.assertEqual(expected_output, c.is_click_inside(input_x, input_y))

    def test_correct_click_inside(self):
        input_x = 1
        input_y = 1
        x1 = y1 = cell_id = x = y = 0
        x2 = y2 = 2
        c = cell.Cell(x1, y1, x2, y2, cell_id, x, y)
        expected_output = True
        self.assertEqual(expected_output, c.is_click_inside(input_x, input_y))

    def test_incorrect_init(self):
        x1 = x2 = y1 = y2 = cell_id = x = y = "Wrong input"
        self.assertRaises(ValueError, lambda: cell.Cell(x1, y1, x2, y2, cell_id, x, y))

    def test_correct_init(self):
        x1 = x2 = y1 = y2 = cell_id = x = y = 1
        c = cell.Cell(x1, y1, x2, y2, cell_id, x, y)
        expected_output = 1
        self.assertEqual(expected_output, c.x1)
        self.assertEqual(expected_output, c.y1)
        self.assertEqual(expected_output, c.x2)
        self.assertEqual(expected_output, c.y2)
        self.assertEqual(expected_output, c.cell_id)
        self.assertEqual(expected_output, c.x)
        self.assertEqual(expected_output, c.y)


if __name__ == '__main__':
    import unittest
    unittest.main()
