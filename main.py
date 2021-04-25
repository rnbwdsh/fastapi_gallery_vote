import os
import uvicorn
import yaml
from fastapi import FastAPI, Request, File, UploadFile, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Optional

from voteable import Voteable, IMGDIR

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.on_event("startup")
def startup():
    try:
        with open("store.yml", "r") as votef:
            app.images = yaml.load(votef, Loader=yaml.UnsafeLoader)
            print(app.images)
    except:
        app.images = {fn: Voteable(fn) for fn in os.listdir(IMGDIR)}


@app.on_event("shutdown")
def persist():  # just dump everything, lol
    with open("store.yml", "w") as jsonf:
        yaml.dump(app.images, jsonf)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request, sort: int = 0):
    sortings = [lambda img: img.filename,
                lambda img: -img.score(),
                lambda img: -img.nr_votes()]
    img = sorted(app.images.values(), key=sortings[sort if sort in range(3) else 0])
    return templates.TemplateResponse("index.html", {"request": request, "images": img})


@app.post("/upload")
async def create_upload_file(file: UploadFile = File(...)):
    if file.content_type != "image/png":
        raise Exception("Invalid file")
    new_filename = f"{len(app.images.keys()) + 1}.png"
    with open(IMGDIR + new_filename, "wb") as new_file:
        new_file.write(await file.read())
    app.images[new_filename] = Voteable(new_filename)
    return RedirectResponse(url='/', status_code=status.HTTP_303_SEE_OTHER)


@app.get("/vote")
async def vote(vote: str, item: str, request: Request):
    app.images[item].vote(vote, request.client.host)
    return RedirectResponse(url='/')


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
