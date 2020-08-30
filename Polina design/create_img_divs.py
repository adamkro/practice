mport os
dirname = 'img'
html = '<div id="myCarousel" class="carousel slide" data-interval="false">\n\t<div class="carousel-inner">'
active = "active"
for filename in os.listdir(dirname):
    if ".jpg" in filename:
        html = html + '\n\t\t<div class="item %s"><img src="%s"/></div>' % (active, dirname + "/" + filename)
        active = ""
html = html + '</div><!-- .carousel-inner -->\n</div><!-- .carousel -->'
