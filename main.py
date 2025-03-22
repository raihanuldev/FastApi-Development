from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/blogs")
def read_blog():
    return {"Welcome to Blog area"}

