#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.plugins.action import ActionBase
from jsonschema import Draft7Validator
from jsonschema.exceptions import ValidationError


class ActionModule(ActionBase):

    TRANSFERS_FILES = False
    _VALID_ARGS = frozenset((
        'schema', 'instance', 'fatal'
    ))

    def run(self, tmp=None, task_vars=None):
        del tmp  # tmp no longer has any effect

        self._supports_check_mode = True

        result = super(ActionModule, self).run(task_vars=task_vars)
        result["changed"] = False
        result["validated"] = False

        schema = self._task.args.get("schema")
        instance = self._task.args.get("instance")
        fatal = self._task.args.get("fatal", False)

        # input validation
        if schema is None:
            result["failed"] = True
            result["msg"] = "missing required argument: schema"
            return result
        if instance is None:
            result["failed"] = True
            result["msg"] = "missing required argument: instance"
            return result

        try:
            Draft7Validator(schema).validate(instance)
            result["validated"] = True
            return result
        except ValidationError as e:
            result["msg"] = '{0}: {1}'.format(e.path, e.message)
            if fatal:
                result["failed"] = True
            return result
        except Exception as e:
            result["msg"] = e
            if fatal:
                result["failed"] = True
            return result
