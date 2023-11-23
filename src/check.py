from fastapi import FastAPI

app = FastAPI()


h = "I would have expected the install command to create an isolated environment, install the build requirements and perform the build in that isolated environment, and then install the produced artifact in my current environment."


print(h)
