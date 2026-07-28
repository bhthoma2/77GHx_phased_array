import pya

app = pya.Application.instance()
mw = app.main_window()

cv_idx = mw.load_layout("/home/bthomas3/Videos/77GHz_phased_array/tapeout/PHASED_ARRAY_77G_XTOR.gds", 0)
lv = mw.current_view()
lv.max_hier()
lv.zoom_fit()

img_path = "/home/bthomas3/Videos/77GHz_phased_array/layout/full_chip_layout.png"
lv.save_image(img_path, 2500, 2500)
print(f"Saved: {img_path}")
