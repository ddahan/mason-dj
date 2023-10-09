from ._main import api


@api.get("/add")
def addi(request, a: int, b: int):
    return {"result": a + b}


# TODO: build CRUD for badges here
