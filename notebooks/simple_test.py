import marimo as mo


def hello():
    mo.md("# Hello World")
    return "Hello from Marimo!"


def counter():
    mo.md("## Counter")
    return 42


app = mo.App(title="Simple Test", cells=[mo.Cell(hello), mo.Cell(counter)])

if __name__ == "__main__":
    app.run()
