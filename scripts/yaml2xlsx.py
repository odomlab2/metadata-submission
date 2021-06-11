#!/usr/bin/python3

import pandas as pd
import openpyxl
import ruamel.yaml as yaml
from styleframe import StyleFrame, Styler, utils
import itertools

from scripts.yaml2html import write_html

def load_template_yaml(yaml_file="template.yaml"):
    """Read template YAML and return as Pandas DataFrame"""
    with open(yaml_file) as fin:
        template = yaml.safe_load(fin)

    row_names = set(list(itertools.chain.from_iterable([list(d.keys()) for d in template.values()])))

    row_names = row_names.add("fieldname")

    df = pd.DataFrame(template)#
    df.insert(0, "info", df.index)
    print(df.head())
    return df

def order_df(df):
    def _get_order(df):
        t = df.transpose()
        t.used_for = t.used_for.apply(lambda x: x.split(","))
        t2 = t.explode("used_for")
        ilse = t2[t2["used_for"] == "ILSe"].index.to_list()
        guide = t2[t2["used_for"] == "GUIDE"].index.to_list()
        odomlab = t2[t2["used_for"] == "Odomlab"].index.to_list()
        odomlab_no_duplicates = list(set(odomlab) - set(ilse) - set(guide))
        odomlab_manual = [
            'SPECIES',
            'STRAIN',
            'INDIVIDUAL',
            'TISSUE',
            'GENOTYPE',
            'TREATMENT',
            'WAY_OF_DEATH',
            'DATE_OF_BIRTH',
            'DATE_OF_DEATH',
            'TISSUE_PREP_METHOD',
            'CELL_INPUT[TOTAL_ALIVE CELLS]',
            'NA_PREP_METHOD',
            'BARCODETYPE',
            'BARCODE_WELL_I5',
            'BARCODE_WELL_I7',
            'DNA_FRAGMENTATION_METHOD',
            'AVERAGE_FRAGMENT_SIZE',
            'IMAGING_DATASET_ID',
            'ANTIBODY',
            'ANTIBODY_TARGET',
            'NOTES']
        return ilse + guide + odomlab_manual

    ordered_columns = _get_order(df)
    print(ordered_columns)
    df = df[ordered_columns]
    return df

def style_df(df):
    """Styling with StyleFrame"""
    sf = StyleFrame(df)
    header_style = Styler(bold=True, font_size=10)
    sf.apply_headers_style(styler_obj=header_style)
    info_style = Styler(bold=False, font_size=8, wrap_text=True, bg_color="#F0F3BD")
    sf.apply_column_style(cols_to_style=sf.columns,
                          styler_obj=info_style,
                          overwrite_default_style=False)
    # col_styles = {"sample": Styler( bg_color="#028090"),
    #               "experiment": Styler( bg_color="#00A896"),
    #               "sequencing": Styler(bg_color="#02C39A"),
    #               "other": Styler(bg_color="#F0F3BD")}
    # for col, styler in col_styles.items():
    #     sf.apply_style_by_indexes(indexes_to_style=sf[sf['order'] == col],
    #                               cols_to_style='Pass/Fail',
    #                               styler_obj=styler,
    #                               overwrite_default_style=False)
    # sd = sd[sd["info"].isin(["description", "example"])]

    all_rows = sf.row_indexes
    # set rows heights
    sf.set_row_height_dict(row_height_dict={
        all_rows[0]: 30
    })
    if len(sf.index) > 1:
        sf.set_row_height_dict(row_height_dict={
            all_rows[0]: 30,  # headers row
            all_rows[1]: 45,  # headers row
            all_rows[2:]: 25
        })

    # set columns widths
    sf.set_column_width(columns=sf.columns, width=20)

    return sf

def save_styled_xlsx(df, out_fname = 'build/sheets/sequencing_spreadsheet_template.xlsx'):
    info_sheet = style_df(df)
    data_sheet = style_df(pd.DataFrame(columns=df.columns.tolist()).drop("info", axis=1, errors="ignore"))

    ew = StyleFrame.ExcelWriter(out_fname)
    data_sheet.to_excel(excel_writer=ew, sheet_name='Data')
    info_sheet.to_excel(excel_writer=ew,
                        sheet_name='Examples & Info',
                        right_to_left=False,
                        columns_and_rows_to_freeze='A2', # will freeze the rows above 2 (=row 1 only) and columns that before column 'B' (=col A only)
                        #row_to_add_filters=0,
                        #allow_protection=True
                        )
    ew.save()

    return ew


if __name__ == "__main__":

    df = load_template_yaml()


    column_order_styles = {
        "by_category": df,
        "by_provider": order_df(df)  # "classic" order, given by application for ILSe, GUIDE and other tables.
    }
    for column_order_label, df_ordered in column_order_styles.items():
        ew = save_styled_xlsx(df_ordered, out_fname=f'build/sheets/sequencing_spreadsheet_template.{column_order_label}.xlsx')

    column_order_styles["by_category"] = column_order_styles["by_category"].drop("info", axis=1)  # remove info column for html
    write_html("build/index.html", **column_order_styles)


    print("---")
    df = pd.DataFrame({"SAMPLE_NAME_GPCF": ["a description", "a example"],
                       "PROJECT": ["another description", "another example"]},
                      index=["description", "example"])
    json_Data = df.to_dict()
    print(json_Data)
    with open("example.yaml", "w") as fout:
        yaml.safe_dump(json_Data, fout, allow_unicode=True)

    print(pd.DataFrame.from_dict(json_Data))

    #EOF