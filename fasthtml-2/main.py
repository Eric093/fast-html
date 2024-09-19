from fasthtml.common import *

def render(todo):
    tid = f'todo-{todo.id}'
    toggle =A('Toggle', hx_get=f'/toggle/{todo.id}', target_id=tid)
    return Li(toggle, 
              Str(todo.title) + (" []"  if todo.done else ""),
               id=tid)

app,rt,todos,Todo = fast_app('todo.db', live=True, render=render,
                              id=int, title=str, done=bool, pk='id')

# def NumList(i):
#     return Ul(*[Li(o) for o in range(i)])




@rt('/')
def get(): 
    # todos.insert(Todo(title='Un Todo', done=False))
    # items = [Li(o) for o in todos()]
    return Titled('Todos',
                  # Div(nums, id='stuff', hx_get="/change"),
                  Ul(*todos()),
                                      )

@rt('/toggle/{tid}')
def get(tid:int):
    todo = todos[tid]
    todo.done = not todo.done
    todos.update(todo)
    return todo

# @rt('/change')
# def get(): 
#     return P('Nice to be here!')
                    


serve()
