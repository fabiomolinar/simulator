import unittest
from simulator.models.base import BaseModel
from simulator.models.rc import RC

class TestBaseModel(unittest.TestCase):
    def setUp(self):
        class Asd(BaseModel):
            def __init__(self, asd, qwe):
                self.asd = asd
                self.qwe = qwe
                self.a_list = [1,2,3]

            def reset(self):
                self.asd = "asd"
                self.qwe = "qwe"

        self.asd = Asd("asd", "qwe")

    def test_attributes_update(self):
        self.assertEqual(self.asd.asd, "asd")
        self.assertEqual(self.asd.qwe, "qwe")
        asd = "new asd"
        qwe = "new qwe"
        self.asd.update_attributes(**{"asd": asd, "qwe": qwe})
        self.assertEqual(self.asd.asd, asd)
        self.assertEqual(self.asd.qwe, qwe)

    def test_attribute_list_update(self):
        self.asd.update_attributes(**{"a_list": 4})
        self.assertListEqual(self.asd.a_list, [1,2,3,4])


