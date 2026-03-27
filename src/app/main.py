import typer

app = typer.Typer()

@app.command()
def greet():
    """Print Hello World!"""
    print("Hello World!")

if __name__ == "__main__":
    app()
