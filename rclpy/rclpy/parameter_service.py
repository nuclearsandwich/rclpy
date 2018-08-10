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

from rcl_interfaces.srv import DescribeParameters, GetParameters, GetParameterTypes
from rcl_interfaces.srv import ListParameters, SetParameters, SetParametersAtomically
from rclpy.parameter import Parameter


class ParameterService:

    def __init__(self, node):
        self._node = node
        nodename = node.get_name()

        describe_parameters_service_name = '/'.join((nodename, 'describe_parameters'))
        node.create_service(
            DescribeParameters, describe_parameters_service_name,
            self._describe_parameters_callback
        )
        get_parameters_service_name = '/'.join((nodename, 'get_parameters'))
        node.create_service(
            GetParameters, get_parameters_service_name, self._get_parameters_callback
        )
        get_parameter_types_service_name = '/'.join((nodename, 'get_parameter_types'))
        node.create_service(
            GetParameterTypes, get_parameter_types_service_name,
            self._get_parameter_types_callback
        )
        list_parameters_service_name = '/'.join((nodename, 'list_parameters'))
        node.create_service(
            ListParameters, list_parameters_service_name, self._list_parameters_callback
        )
        set_parameters_service_name = '/'.join((nodename, 'set_parameters'))
        node.create_service(
            SetParameters, set_parameters_service_name, self._set_parameters_callback
        )
        set_parameters_atomically_service_name = '/'.join((nodename, 'set_parameters_atomically'))
        node.create_service(
            SetParametersAtomically, set_parameters_atomically_service_name,
            self._set_parameters_atomically_callback
        )

    def _describe_parameters_callback(self, request, response):
        for name in request.names:
            p = self._node.get_parameter(name)
            response.descriptors.append(p.get_descriptor())
        return response

    def _get_parameters_callback(self, request, response):
        for name in request.names:
            p = self._node.get_parameter(name)
            response.values.append(p.get_parameter_value())
        return response

    def _get_parameter_types_callback(self, request, response):
        for name in request.names:
            response.types.append(self._node.get_parameter(name).get_parameter_type())
        return response

    def _list_parameters_callback(self, request, response):
        names_with_prefixes = []
        for name in self._node._parameters.keys():
            if '.' in name:
                names_with_prefixes.append(name)
                continue
            elif request.prefixes:
                continue
            else:
                response.result.names.append(name)
        if 1 == request.depth:
            return response

        if not 0 == request.depth:
            # A depth of zero indicates infinite depth
            names_with_prefixes = filter(
                lambda name: name.count('.') + 1 <= request.depth, names_with_prefixes
            )
        for name in names_with_prefixes:
            if request.prefixes:
                for prefix in request.prefixes:
                    prefix_with_trailing_dot = '%s.' % (prefix)
                    if name.startswith(prefix_with_trailing_dot):
                        response.result.names.append(name)
                        full_prefix = '.'.join(name.split('.')[0:-1])
                        if full_prefix not in response.result.prefixes:
                            response.result.prefixes.append(full_prefix)
                        if prefix not in response.result.prefixes:
                            response.result.prefixes.append(prefix)
            else:
                prefix = '.'.join(name.split('.')[0:-1])
                if prefix not in response.result.prefixes:
                    response.result.prefixes.append(prefix)
                response.result.names.append(name)

        return response

    def _set_parameters_callback(self, request, response):
        for p in request.parameters:
            param = Parameter.from_rcl_interface_parameter(p)
            response.results.append(self._node.set_parameters_atomically([param]))
        return response

    def _set_parameters_atomically_callback(self, request, response):
        response.results = self._node.set_parameters_atomically([
            Parameter.from_rcl_interface_parameter(p) for p in request.parameters])
        return response
