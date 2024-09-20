
"""
This module provides a simple web application for managing a todo list using the FastHTML framework.

Functions:
    render(item: 'Todo') -> Li:
        Renders a todo item as an HTML list item with a delete link.

    get(request) -> Titled:
        Handles GET requests to the root URL ("/"). Returns an HTML page with a form to add new todo items,
        a list of existing todo items, and a logout link.

    post(todo: 'Todo') -> None:
        Handles POST requests to the root URL ("/"). Inserts a new todo item into the database.

    delete(id: int) -> None:
        Handles DELETE requests to the URL pattern "/todo/{id}". Deletes the specified todo item from the database.

Variables:
    auth:
        Middleware for user authentication using username and password.

    app, rt, todos, Todo:
        FastHTML application instance, route decorator, todo items collection, and Todo model class.

    serve:
        Function to start the FastHTML application server.
"""

from fasthtml.common import *

def render(item:'Todo'):
    id = f'todo-{item.id}'
    dellink = AX('Delete', hx_delete=f'/todo/{item.id}', target_id=id, hx_swap='delete')
    return Li(item.title, dellink, id=id)

auth = user_pwd_auth(user='s3kret', skip=[r'/favicon\.ico', r'/static/.*', r'.*\.css'])

app,rt,todos,Todo = fast_app(
    'data/tbl.db', middleware=[auth], render=render,
    id=int, title=str, pk='id')

@rt("/")

async def get(request):
    new_frm = Form(hx_post='/', target_id='todo-list', hx_swap='beforeend')(
        Group(
            Input(name='title', placeholder='Title'),
            Button('Add')
        )
    )
    items = Ul(*todos(), id='todo-list')
    logout = A('logout', href=basic_logout(request))
    return Titled('Todo list', new_frm, items, logout)

@rt("/")
async def post(todo:Todo): return todos.insert(todo)

@rt("/todo/{id}")
async def delete(id:int): todos.delete(id)

serve()
