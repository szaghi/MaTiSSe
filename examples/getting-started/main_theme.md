---theme_canvas
background = radial-gradient(rgb(240, 240, 240), rgb(110, 110, 110))
---endtheme_canvas

---theme_toc
font-variant = small-caps
---endtheme_toc

---theme_section_emph_toc
border        = 1px solid #4788B3
border-radius = 5px
---endtheme_section_emph_toc

---theme_subsection_emph_toc
border        = 1px solid #4788B3
border-radius = 5px
---endtheme_subsection_emph_toc

---theme_slide_emph_toc
border        = 1px solid #4788B3
border-radius = 5px
---endtheme_slide_emph_toc

---theme_slide_global
width            = 900px
height           = 700px
border-radius    = 10px
background       = green
color            = rgb(102,102,102)
font-size        = 100%
slide-transition = svgpath
data-offset      = 1
---endtheme_slide_global

---theme_slide_content
background    = white
color         = rgb(102,102,102)
padding       = 1%
---endtheme_slide_content

---theme_slide_header_1
height        = 6%
padding       = 1% 2%
background    = #4788B3
color         = white
border-radius = 10px 10px 0 0
metadata      = [['slidetitle','float:left;font-variant:small-caps;font-size:150%;'],&&
                 ['logo','float:right;height:100%;']]
---endtheme_slide_header_1

---theme_slide_footer_1
height     = 6%
padding    = 1% 2%
background = #86B2CF
color      = white
metadata   = [['timer','controls;font-size:70%;font-variant:small-caps;float:right'],&&
              ['total_slides_number','float:right;padding:0 1%;'],                   &&
              ['|custom| of ','float:right;'],                                       &&
              ['slidenumber','float:right;padding:0 1%;'],                           &&
              ['|custom|slide ','float:right;']]
---endtheme_slide_footer_1

---theme_slide_sidebar_1
position      = R
width         = 20%
padding       = 1% 2%
background    = linear-gradient(#4788B3,#86B2CF)
color         = white
border-radius = 0
metadata      = [['title','font-weight:bold;font-variant:small-caps;font-size:105%;display:inline-block'],                                          &&
                 ['authors','font-variant:small-caps;font-size:90%;display:inline-block'],                                                          &&
                 ['affiliations','margin-top:4%;margin-bottom:10%;font-variant:small-caps;font-size:70%;white-space:pre-wrap;display:inline-block'],&&
                 ['toc','font-size:70%;',2]]
---endtheme_slide_sidebar_1

---theme_figure
style   = font-variant:small-caps;text-align:center;
caption = font-size:80%;color:#4788B3;
---endtheme_figure

---theme_note
style   = display:inline-block;font-variant:small-caps;box-shadow: 7px 7px 5px rgba(200,200,200,0.3);border-radius:20px
caption = padding:0 2%;color:#4788B3;border-bottom:1px solid #4788B3;display:inline-block;
content = padding:0 2%;font-size:120%;
---endtheme_note
