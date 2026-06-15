from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

router = APIRouter(tags=["pages"])


@router.get("/", response_class=HTMLResponse)
async def page_index(request: Request):
    return templates.TemplateResponse(request, "index.html", {})


@router.get("/login", response_class=HTMLResponse)
async def page_login(request: Request):
    return templates.TemplateResponse(request, "login.html", {})


@router.get("/book/add", response_class=HTMLResponse)
async def page_book_add(request: Request):
    return templates.TemplateResponse(request, "book_form.html", {"mode": "add", "book_id": None})


@router.get("/book/{book_id}/review", response_class=HTMLResponse)
async def page_book_review(request: Request, book_id: int):
    return templates.TemplateResponse(request, "review_form.html", {"book_id": book_id})


@router.get("/book/{book_id}/edit", response_class=HTMLResponse)
async def page_book_edit(request: Request, book_id: int):
    return templates.TemplateResponse(request, "book_form.html", {"mode": "edit", "book_id": book_id})


@router.get("/book/{book_id}", response_class=HTMLResponse)
async def page_book_detail(request: Request, book_id: int):
    return templates.TemplateResponse(request, "book.html", {"book_id": book_id})


@router.get("/selections", response_class=HTMLResponse)
async def page_selections(request: Request):
    return templates.TemplateResponse(request, "selections.html", {})


@router.get("/selections/{selection_id}", response_class=HTMLResponse)
async def page_selection_detail(request: Request, selection_id: int):
    return templates.TemplateResponse(request, "selection_detail.html", {"selection_id": selection_id})


@router.get("/register", response_class=HTMLResponse)
async def page_register(request: Request):
    return templates.TemplateResponse(request, "register.html", {})
