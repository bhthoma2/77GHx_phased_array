import pya

lef_files = [
    "/home/bthomas3/Videos/IHP-Open-PDK/ihp-sg13g2/libs.ref/sg13g2_stdcell/lef/sg13g2_tech.lef",
    "/home/bthomas3/Videos/IHP-Open-PDK/ihp-sg13g2/libs.ref/sg13g2_stdcell/lef/sg13g2_stdcell.lef",
    "/home/bthomas3/Videos/IHP-Open-PDK/ihp-sg13g2/libs.ref/sg13g2_sram/lef/RM_IHPSG13_1P_1024x32_c2_bm_bist.lef",
]

def_file = "/home/bthomas3/Videos/77GHz_phased_array/digital_pnr/build/vibrometer_top.def"

opt = pya.LoadLayoutOptions()
opt.lefdef_config.lef_files = lef_files

app = pya.Application.instance()
mw = app.main_window()
mw.load_layout(def_file, opt, 0)
view = mw.current_view()
view.zoom_fit()