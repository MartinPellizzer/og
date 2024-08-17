def header():
    return f'''
      <header class="container-xl flex justify-between py-24">
          <a class="text-16 uppercase text-black no-underline" href="/">Ozonogroup</a>
          <nav class="flex gap-16">
              <a class="text-16 uppercase text-black no-underline" href="/news.html">News</a>
              <a class="text-16 uppercase text-black no-underline" href="/risorse.html">Risorse</a>
              <a class="text-16 uppercase text-black no-underline" href="/servizi.html">Servizi</a>
          </nav>
      </header>
    '''
  
def footer():
    return f'''
        <section class="footer-section">
            <div class="container-xl h-full">
                <footer class="flex items-center justify-center">
                    <span class="text-white">Ozonogroup s.r.l. | Tutti i diritti riservati</span>
                </footer>
            </div>
        </section>
    '''
