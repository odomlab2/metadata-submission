
import subprocess
from datetime import date


CSS_TEXT = '''
<html>
<head>
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
<h2> <a href="../sheets/template.xlsx"> Download Excel template here </a> </h2>
In case of questions please open a issue at <a href="https://github.com/odomlab2/metadata-submission/issues" >GitHub</a> - Thanks!
</p>
    {table}
</body>
</html>
'''

DATE = date.today()

def get_version():
    version_label = subprocess.check_output(["git", "describe", "--always", "--tags"]).strip().decode("utf-8")
    return version_label

def write_html(df, htmlfile="template.html"):
    # OUTPUT AN HTML FILE
    df = df.transpose()
    with open(htmlfile, 'w') as f:
        f.write(CSS_TEXT.format(table=df.to_html(classes="table table-striped table-condensed"),
                                date=DATE,
                                commit=get_version()))