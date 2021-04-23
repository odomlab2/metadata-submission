import unittest
import pandas as pd
import numpy as np
import pytest

from scripts.yaml2xlsx import load_template_yaml

class TemplateTests(unittest.TestCase):

    def test_loadYAML(self):
        df = load_template_yaml(yaml_file = "../template.yaml")
        self.assertIsInstance(df, pd.DataFrame)

    @pytest.mark.xfail# (raises=AssertionError)
    def test_equal_colname_list(self):
        """Do the fieldnames in the YAML match those in the previos spreadsheet. """
        yaml_based_df = load_template_yaml(yaml_file = "../template.yaml")
        orig_spreadsheet = pd.read_excel("../sequencing_spreadsheet.template.xlsx", sheet_name="Examples")

        diff = set(orig_spreadsheet.columns).difference(set(yaml_based_df.columns))
        print(diff)
        self.assertIsNone(diff)


    def test_example_match_regex(self):
        """Do the examples work with the regular expression?"""
        import re
        df = load_template_yaml(yaml_file = "../template.yaml")

        def _get_regex(col):
            if col.name == "info":
                return None # skip info row

            regex_pattern = col["regex"]
            example =  col["example"]

            # catch exceptions
            if pd.isnull(regex_pattern):
                return None
            if pd.isnull(example):
                return None

            print(f"{regex_pattern} : ", end="")
            if type(example) == list:
                print(",".join(example), end=" -- ")
                match_list  = [re.match(regex_pattern, str(elem))for elem in example]
                regex_match = all(match_list)
            else:
                print(example, end=" -- ")
                regex_match = re.match(regex_pattern, str(example))
            if regex_match:
                print("✓")
                return True
            else:
                print("❌")
                return False


        r = df.apply(lambda x: _get_regex(x), result_type="reduce")
        list_of_matches = all([e for e in r.to_list() if not e == None])
        self.assertTrue(list_of_matches)


if __name__ == '__main__':
    unittest.main()
