# Copyright 2018 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest

from rclpy.parameter import Parameter


class TestNode(unittest.TestCase):

    def test_create_boolean_parameter(self):
        p = Parameter('myparam', True)
        self.assertEqual(p.name, 'myparam')
        self.assertEqual(p.value, True)

    def test_create_bytes_parameter(self):
        p = Parameter('myparam', b'pvalue')
        self.assertEqual(p.name, 'myparam')
        self.assertEqual(p.value, b'pvalue')

    def test_create_float_parameter(self):
        p = Parameter('myparam', 2.41)
        self.assertEqual(p.name, 'myparam')
        self.assertEqual(p.value, 2.41)

    def test_create_integer_parameter(self):
        p = Parameter('myparam', 42)
        self.assertEqual(p.name, 'myparam')
        self.assertEqual(p.value, 42)

    def test_create_string_parameter(self):
        p = Parameter('myparam', 'pvalue')
        self.assertEqual(p.name, 'myparam')
        self.assertEqual(p.value, 'pvalue')

    @unittest.skip('not yet implemented')
    def test_create_boolean_array_parameter(self):
        p = Parameter('myparam', [True, False, True])
        self.assertEqual(p.value, [True, False, True])

    @unittest.skip('not yet implemented')
    def test_create_float_array_parameter(self):
        p = Parameter('myparam', [2.41, 6.28])
        self.assertEqual(p.value, [2.41, 6.28])

    @unittest.skip('not yet implemented')
    def test_create_integer_array_parameter(self):
        p = Parameter('myparam', [1, 2, 3])
        self.assertEqual(p.value, [1, 2, 3])

    @unittest.skip('not yet implemented')
    def test_create_string_array_parameter(self):
        p = Parameter('myparam', ['hello', 'world'])
        self.assertEqual(p.value, ['hello', 'world'])

    def test_prevent_illegal_value_type(self):
        with self.assertRaises(ValueError):
            Parameter('illegaltype', ())
