from fasthtml.common import *

app,rt = fast_app(live=True)

@rt('/')
def get(): 
    nums = Ul(*[Li(o) for o in range(10)])
    return Titled('Salut !',
                  nums,
                  Div(P(H1('Hello World!')),
                    P(A('LIEN', href='/change')))
                    )

@rt('/change')
def get(): 
    return Div(P('Nice to be here!'),
                    P(A('Home', href='/')))


serve()
