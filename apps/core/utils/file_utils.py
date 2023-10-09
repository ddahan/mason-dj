def file_to_str(file_path) -> str:
    with open(file_path, "r") as file:
        data = file.read()
    return data
