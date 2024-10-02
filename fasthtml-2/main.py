from fasthtml.common import *

#--------------------------------------------
def render(todo):
    """
    Génère un élément de liste HTML pour une tâche à faire (todo).

    Args:
        todo (object): Un objet représentant une tâche à faire avec les attributs suivants :
            - id (int): L'identifiant unique de la tâche.
            - title (str): Le titre de la tâche.
            - done (bool): L'état de la tâche (terminée ou non).

    Returns:
        Li: Un élément de liste HTML contenant des liens pour basculer et supprimer la tâche,
            ainsi que le titre de la tâche avec une indication de son état.
    """
    tid = f'todo-{todo.id}'
    toggle =A('Toggle - ', hx_get=f'/toggle/{todo.id}', target_id=tid)
    delete =A('Delete - ', hx_delete=f'/{todo.id}',
              hx_swap='outerHTML', target_id=tid)
    return Li(toggle, delete,
              Str(todo.title) + (" [👆]"  if todo.done else "❌"),
               id=tid)
#--------------------------------------------


app,rt,todos,Todo = fast_app('todo.db', live=True, render=render,
                              id=int, title=str, done=bool, pk='id')





@rt('/')
def get(): 
    frm = Form(Group(Input(placeholder='Ajouter un nouveau Todo', name="title"),
                      Button('Ajouter')),
                    hx_post='/', target_id='todo-list', hx_swap='beforeend')

    return Titled('Todos',
                  Card(
                    Ul(*todos(), id='todo-list'),
                    header=frm)
                    )

@rt('/')
def post(todo:Todo): return todos.insert(todo)
    
    

@rt('/{tid}')
def delete(tid:int): todos.delete(tid)
    

@rt('/toggle/{tid}')
def get(tid:int):
    todo = todos[tid]
    todo.done = not todo.done
    return todos.update(todo)
    

# @rt('/change')
# def get(): 
#     return P('Nice to be here!')
                    


serve()
