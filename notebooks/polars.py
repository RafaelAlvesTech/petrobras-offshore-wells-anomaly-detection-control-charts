import marimo

__generated_with = "0.15.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import polars as pl

    df = pl.read_csv("../languages.csv", inter_schema_legth=1000)
    df.head()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
