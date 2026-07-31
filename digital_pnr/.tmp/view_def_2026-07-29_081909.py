import pya

lef_files = [
    "/home/bthomas3/Videos/IHP-Open-PDK/ihp-sg13g2/libs.ref/sg13g2_stdcell/lef/sg13g2_tech.lef",
    "/home/bthomas3/Videos/IHP-Open-PDK/ihp-sg13g2/libs.ref/sg13g2_stdcell/lef/sg13g2_stdcell.lef",
    "/home/bthomas3/Videos/IHP-Open-PDK/ihp-sg13g2/libs.ref/sg13g2_sram/lef/RM_IHPSG13_1P_1024x32_c2_bm_bist.lef",
]

gds_files = [
    "/home/bthomas3/Videos/IHP-Open-PDK/ihp-sg13g2/libs.ref/sg13g2_stdcell/gds/sg13g2_stdcell.gds",
]

def_file = "/home/bthomas3/Videos/77GHz_phased_array/digital_pnr/build/slowtime_fft_routed.def"

opt = pya.LoadLayoutOptions()
opt.lefdef_config.lef_files = lef_files
opt.lefdef_config.map_file = ""
opt.lefdef_config.macro_resolution_mode = 1
opt.lefdef_config.read_lef_with_def = True

app = pya.Application.instance()
mw = app.main_window()

cv = mw.load_layout(def_file, opt, 0)
layout = cv.layout()

for gds in gds_files:
    layout.read(gds)

view = mw.current_view()
view.zoom_fit()