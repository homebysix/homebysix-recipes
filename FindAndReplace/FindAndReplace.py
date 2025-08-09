#
# Copyright 2016-2020 Elliot Jordan
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

import os

from autopkglib import Processor, remove_recipe_extension  # noqa: F401

__all__ = ["FindAndReplace"]


class FindAndReplace(Processor):
    """This processor does one thing only: It searches the input variable you
    specify and replaces instances of the "find" string with the "replace"
    string."""

    input_variables = {
        "input_string": {
            "required": True,
            "description": "The string you want to perform find/replace on.",
        },
        "find": {
            "required": True,
            "description": "This string, if found, will be replaced with the "
            '"replace" string.',
        },
        "replace": {
            "required": True,
            "description": 'The string that you want to replace the "find" '
            "string with.",
        },
    }
    output_variables = {
        "output_string": {
            "description": "The result of find/replace on the input string."
        },
        "deprecation_summary_result": {
            "description": "Description of deprecation results."
        },
    }
    description = __doc__

    def main(self):
        """Main process."""

        input_string = self.env["input_string"]
        find = self.env["find"]
        replace = self.env["replace"]
        self.output(f'Replacing "{find}" with "{replace}" in "{input_string}".')
        self.env["output_string"] = self.env["input_string"].replace(find, replace)

        # Deprecation method lifted from DeprecationWarning processor
        warning_message = self.env.get(
            "warning_message",
            "### Please use the new FindAndReplace core processor in AutoPkg 2.7.6 instead of this shared processor. ###",
        )
        self.output(warning_message)
        recipe_name = os.path.basename(self.env["RECIPE_PATH"])
        recipe_name = remove_recipe_extension(recipe_name)
        self.env["deprecation_summary_result"] = {
            "summary_text": "The following recipes have deprecation warnings:",
            "report_fields": ["name", "warning"],
            "data": {"name": recipe_name, "warning": warning_message},
        }


if __name__ == "__main__":
    PROCESSOR = FindAndReplace()
    PROCESSOR.execute_shell()
