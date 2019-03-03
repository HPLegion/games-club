import pandas as pd
from string import Template

HTML = """<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>List of Games in Cold Storage</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
    </head>
    <body>
        <div class="container">
                <section class="jumbotron text-center">
                    <div class="container">
                        <h1 class="jumbotron-heading">List of Games in Cold Storage</h1>
                        <p class="lead text-muted">
                            These are the games that are currently in "cold storage".
                            Please go through the list and check if there is anything that you are very interested in playing in the near future, and report those games to us.
                        </p>
                    </div>
                </section>

                <div class="album py-5 bg-light">
                        <div class="container">
                    
                          <div class="row">
                            $items
                          </div>
                        </div>
                      </div>
        </div>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
    </body>
</html>
"""
GAME_TEMPLATE = """              <div class="col-md-4">
                  <div class="card mb-4 shadow-sm">
                  <svg class="bd-placeholder-img card-img-top" width="100%" height="225" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid slice" focusable="false" role="img" aria-label="Placeholder: Thumbnail"><rect width="100%" height="100%" fill="#55595c"/><image width="100%" height="100%" xlink:href="$imagelink"/></svg>
                  <div class="card-body">
                      <h3>$name</h3>
                      <p class="card-text">$description</p>
                      <a href="$bgglink">More info on BGG...</a>
                  </div>
                  </div>
              </div>"""
EXPA_TEMPLATE = """              <div class="col-md-4">
                  <div class="card mb-4 shadow-sm">
                  <svg class="bd-placeholder-img card-img-top" width="100%" height="225" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid slice" focusable="false" role="img" aria-label="Placeholder: Thumbnail"><rect width="100%" height="100%" fill="#55595c"/><image width="100%" height="100%" xlink:href="$imagelink"/></svg>
                  <div class="card-body">
                      <h3>$name</h3>
                      <b>Expansion for: $basegame</b>
                      <p class="card-text">$description</p>
                      <a href="$bgglink">More info on BGG...</a>
                  </div>
                  </div>
              </div>"""

GAME_TEMPLATE = Template(GAME_TEMPLATE)
EXPA_TEMPLATE = Template(EXPA_TEMPLATE)
df = pd.read_csv("./lockergames.csv", dtype=str)

content = ""
for i, row in df.iterrows():
    if row.TYPE == "Expansion":
        item = EXPA_TEMPLATE.substitute(imagelink=row.IMAGE, name=row.TITLE, description=str(row.DESCRIPTION)[:600] + "...", bgglink=row.BGG_URL, basegame=row.BASEGAME)
    else:
        item = GAME_TEMPLATE.substitute(imagelink=row.IMAGE, name=row.TITLE, description=str(row.DESCRIPTION)[:600] + "...", bgglink=row.BGG_URL)
    content = content + str(item) + "\n"

with open("./lockergames.html", "w") as f:
        f.write(Template(HTML).substitute(items=content))
