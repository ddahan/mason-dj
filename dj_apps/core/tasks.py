from toto.celery import app


@app.task()
def add(a, b):
    """This dumb task is used for testing purposes"""
    return a + b
