from unittest import TestCase
import pandas as pd 
import os

class TestImageInfo(TestCase):
    @classmethod
    def setUpClass(cls):
        from image_info import ImageInfo
       
        cls.testInfo = ImageInfo("street.jpg")
        cls.testInfo.csvInfo("street.csv")
    @classmethod
    def tearDownClass(cls):
        if os.path.exists("street.csv"):
            os.remove("street.csv")
    def test_class_boxes(self):
        self.assertEqual(self.testInfo.classBoxes("car"), [0, 8])
        self.assertEqual(self.testInfo.classBoxes("horse"), [])

    def test_box_info(self):
        x_center, y_center, confidence = self.testInfo.boxInfo(0)
        self.assertAlmostEqual(x_center, 0.6620, places=4)
        self.assertAlmostEqual(y_center, 0.4287, places=4)
        self.assertAlmostEqual(confidence, 0.9276, places=4)
    def test_csv_info(self):
        self.assertTrue(os.path.exists("street.csv"))
        df = pd.read_csv("street.csv")
        self.assertIn("class", df.columns)
        self.assertIn("confidence", df.columns)
        self.assertIn("normalized width", df.columns)
        self.assertIn("normalized height", df.columns)  
        self.assertEqual((10,4), df.shape)
    def test_bags_belong_persons(self):
        actual = self.testInfo.bagsPersons(0.5)  
        self.assertEqual(2, len(actual))
        self.assertEqual(4, actual[7][0])
        self.assertEqual(4, actual[9][0])
        self.assertIsNotNone(actual[7][1])
        self.assertIsNotNone(actual[9][1])
    def test_bags_no_belong_persons(self):
        actual = self.testInfo.bagsPersons(0.05)  
        self.assertEqual(2, len(actual))
        self.assertIsNone(actual[7])
        self.assertIsNone(actual[9])    