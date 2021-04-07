
"""

"""
from flask import Flask, render_template
app = Flask(__name__)
@app.route("/plot/")
def plot():
    from bokeh.models.annotations import Title
    from pandas_datareader import data
    import datetime
    from bokeh.plotting import figure, show, output_file
    from bokeh.embed import components
    from bokeh.resources import CDN

    start = datetime.datetime(2021, 1, 1)
    end = datetime.datetime(2021, 4, 1)
    df = data.DataReader(name="AAPL", data_source="yahoo", start=start, end=end)

    def inc_dec(c, o):
        """
        define the days when the indexes increased or dereased
        """
        if c > o:
            value = "Increase"
        elif c < o:
            value = "Decrease"
        else:
            value = "Equal"
        return value

    df["Status"] = [inc_dec(c, o) for c, o in zip(df.Close, df.Open)]
    df["Middle"] = (df.Open + df.Close) / 2
    df["Height"] = abs(df.Open - df.Close)

    p = figure(x_axis_type="datetime", width=1000, height=300, sizing_mode="scale_width")
    t = Title()
    t.text = 'Candlestick Chart of AAPL from 01.01.2021 till 01.04.2021'
    p.title = t

    p.grid.grid_line_alpha = 0.3

    p.segment(df.index, df.High, df.index, df.Low, color="Black")
    hours_12 = 12 * 60 * 60 * 1000
    # color the charts to red when the index increased
    p.rect(df.index[df.Status == "Increase"], df.Middle[df.Status == "Increase"],
           hours_12, df.Height[df.Status == "Increase"], fill_color="#008B8B", line_color="black")
    # color the chart to cyjana when the index decreased
    p.rect(df.index[df.Status == "Decrease"], df.Middle[df.Status == "Decrease"],
           hours_12, df.Height[df.Status == "Decrease"], fill_color="#A52A2A", line_color="black")

    # putting on live webpage
    # send these two components to html templates
    script1, div1 = components(p)
    cdn_js = CDN.js_files[0]
    cdn_css = CDN.css_files

    return render_template("plot.html",
     script1=script1,
     div1=div1,
     cdn_js=cdn_js)

@app.route('/')
def home():
    return render_template("home.html")

# if we import this script from another script, this script we will be assigned the script1.py
#when you execute the script Python assigns the name __main__.

if __name__ == "__main__":
    app.run(debug=True, port=5000)


