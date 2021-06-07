
import subprocess
import numpy as np
from shutil import copyfile
from os.path import dirname, join, basename
from datetime import date


CSS_TEXT_HEADER = '''
<html>
<head>
  <title> Metadata spreadsheet </title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
<link rel="stylesheet" type="text/css" href="df_style.css"/>
</head>
<body>
<h1> List of Metadata fields </h1>

<p>
Version: {commit} <br />
Date: {date} <br />
</p>

<p>
<h2> Download spreadsheets</h2>
<ul>
<li> <a href="sheets/sequencing_spreadsheet_template.by_provider.xlsx"> ["classic"] Sorted by Provider (ILSe, etc) </a> </li> 
<li> <a href="sheets/sequencing_spreadsheet_template.by_category.xlsx"> [new] Sorted by category (Sample, Experiment, Sequencing Info, LOTs) </a> </li> 
</ul>

</p>
<p>
In case of questions please open a issue at <a href="https://github.com/odomlab2/metadata-submission/issues" >GitHub</a> - Thanks!
</p>
<h2> Description and examples </h2> 
<p>
Click on the buttons to display the fieldnames for the schemas.
</p>
<!-- Tab links -->
<div class="tab">
  <button class="tablinks" onclick="openTab(event, 'by_provider')" id="defaultOpen">By Provider</button>
  <button class="tablinks" onclick="openTab(event, 'by_category')" >By Category</button>

</div>
'''

CSS_TEXT_FOOTER='''
<script>
function openTab(evt, TabName) {
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }
  document.getElementById(TabName).style.display = "block";
  evt.currentTarget.className += " active";
}
// Get the element with id="defaultOpen" and click on it
document.getElementById("defaultOpen").click();
</script>
</body>
</html>
'''

DATE = date.today()

def get_version():
    version_label = subprocess.check_output(["git", "describe", "--always", "--tags"]).strip().decode("utf-8")
    return version_label

def list_to_string(x):

    if type(x) == list:
        return ", ".join([str(elem) for elem in x])
    else:
        return x

def write_html(htmlfile="template.html", css_file="scripts/df_style.css", **multiple_df):
    # OUTPUT AN HTML FILE
    copyfile(css_file, join(dirname(htmlfile), basename(css_file)))

    def _write_table(df_label, df):
        html_tab = '''<!-- Tab content -->
                        <div id="{df_label}" class="tabcontent">
                        <h3>{df_label}</h3>
                        {table}
                        </div>'''.format(df_label=df_label,
                                         table=df.to_html(classes="table table-striped table-condensed"))
        return html_tab
    with open(htmlfile, 'w') as f:
        f.write(CSS_TEXT_HEADER.format(date=DATE,
                                       commit=get_version()))
        for df_label, df in multiple_df.items():
            df = df.transpose()
            df.example = df.example.apply(list_to_string)
            df.insert(loc=0, column='Field Name', value=df.index)
            #df.insert(loc=0, column='#', value=np.arange(len(df)))
            f.write(_write_table(df_label, df.reset_index(drop=True)))

        f.write(CSS_TEXT_FOOTER)
