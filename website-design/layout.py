import lorem

def layout_0001():
    h1 = 'Medium length display headline'
    p = lorem.paragraph()
    
    html = f'''
        <section class="layout_0001">
            <div class="container-lg flex">
                <h1>{h1}</h1>
                <p>{p}</p>
            </div>
        </section>
    '''

    return html