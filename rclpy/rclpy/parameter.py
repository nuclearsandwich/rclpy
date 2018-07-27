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

PARAMETER_TYPES = (bool, bytes, float, int, str)


class Parameter:

    def __init__(self, name, value):
        self._name = name
        if isinstance(value, list):
            raise NotImplementedError('List parameter types WIP')

        value_type = type(value)
        if value_type not in PARAMETER_TYPES:
            raise ValueError('Parameter type %s is not supported' % value_type)

        self._type = value_type
        self._value = value

    @property
    def value(self):
        return self._value

    @property
    def value_type(self):
        return self._value_type

    @property
    def name(self):
        return self._name
