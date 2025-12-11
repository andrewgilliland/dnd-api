from fastapi import FastAPI

app = FastAPI(title="TMNT API")


@app.get("/")
def root():
    return {"message": "Welcome to the TMNT API"}
