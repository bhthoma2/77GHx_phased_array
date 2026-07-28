import pya

layout = pya.Layout()
layout.dbu = 0.001
um = lambda x: int(round(x / layout.dbu))

top = layout.create_cell("LO_TEST")

base = "/home/bthomas3/Videos/77GHz_phased_array/layout/"
for fname, cname, px, py in [
    ('VCO_77G_XTOR.gds', 'VCO_77G_XTOR', 900, 1125),
    ('MIXER_77G_XTOR.gds', 'MIXER_77GD', 550, 1125),
]:
    layout.read(base + fname)
    cell = layout.cell(cname)
    top.insert(pya.CellInstArray(cell.cell_index(), pya.Trans(um(px), um(py))))

ly = {layout.get_info(i).to_s().split('/')[0].replace(' ',''):i
      for i in layout.layer_indices()}
layer_map = {'M5': layout.find_layer(67, 0), 'M3': layout.find_layer(30, 0),
             'M4': layout.find_layer(50, 0), 'Via3': layout.find_layer(49, 0),
             'Via4': layout.find_layer(66, 0)}

def via_stack(x, y, bot, top_l):
    stack = [('M3','Via3','M4',0.19,0.5),('M4','Via4','M5',0.19,0.5)]
    started = False
    for b, v, t, vs, ps in stack:
        if b == bot: started = True
        if started:
            vsi = um(vs); psi = um(ps); cx = um(x); cy = um(y)
            top.shapes(layer_map[b]).insert(pya.Box(cx-psi//2,cy-psi//2,cx+psi//2,cy+psi//2))
            top.shapes(layer_map[v]).insert(pya.Box(cx-vsi//2,cy-vsi//2,cx+vsi//2,cy+vsi//2))
            top.shapes(layer_map[t]).insert(pya.Box(cx-psi//2,cy-psi//2,cx+psi//2,cy+psi//2))
        if t == top_l: break

route_w = 3.0
vco_x, vco_y = 900, 1125
mix_x, mix_y = 550, 1125

vco_outp_x = vco_x + 144.0
vco_outn_x = vco_x + 139.0
vco_port_y = vco_y + 219.0
mix_lop_y = mix_y + 263.775
mix_lon_y = mix_y + 279.775
mix_lo_x = mix_x + 150.0

lo_chan_x_p = 880.0
lo_chan_x_n = 860.0
outp_h_y = vco_port_y + 10.0
outn_h_y = vco_port_y - 10.0

# via_stack(vco_outp_x, vco_port_y, 'M3', 'M5')  # disabled for debug
# via_stack(vco_outn_x, vco_port_y, 'M4', 'M5')  # disabled for debug

M5 = layer_map['M5']
# OUTP: vertical up, horizontal left, channel vertical up, horizontal into mixer
top.shapes(M5).insert(pya.Box(um(vco_outp_x-route_w/2),um(vco_port_y-route_w/2),um(vco_outp_x+route_w/2),um(outp_h_y+route_w/2)))
top.shapes(M5).insert(pya.Box(um(lo_chan_x_p-route_w/2),um(outp_h_y-route_w/2),um(vco_outp_x+route_w/2),um(outp_h_y+route_w/2)))
top.shapes(M5).insert(pya.Box(um(lo_chan_x_p-route_w/2),um(outp_h_y-route_w/2),um(lo_chan_x_p+route_w/2),um(mix_lop_y+route_w/2)))
top.shapes(M5).insert(pya.Box(um(lo_chan_x_p-route_w/2),um(mix_lop_y-route_w/2),um(mix_lo_x+route_w/2),um(mix_lop_y+route_w/2)))

# OUTN: use M4 bridge at OUTP channel (x=880)
bridge_start = lo_chan_x_p + 8.0  # 888
bridge_end = lo_chan_x_p - 8.0    # 872
M4 = layer_map['M4']
Via4 = layer_map['Via4']
# Vertical from port to outn_h_y
top.shapes(M5).insert(pya.Box(um(vco_outn_x-route_w/2),um(outn_h_y-route_w/2),um(vco_outn_x+route_w/2),um(vco_port_y+route_w/2)))
# M5 from VCO to bridge start
top.shapes(M5).insert(pya.Box(um(bridge_start-route_w/2),um(outn_h_y-route_w/2),um(vco_outn_x+route_w/2),um(outn_h_y+route_w/2)))
# Via M5->M4
ps=um(0.5); vs=um(0.19); cx=um(bridge_start); cy=um(outn_h_y)
top.shapes(M5).insert(pya.Box(cx-ps//2,cy-ps//2,cx+ps//2,cy+ps//2))
top.shapes(Via4).insert(pya.Box(cx-vs//2,cy-vs//2,cx+vs//2,cy+vs//2))
top.shapes(M4).insert(pya.Box(cx-ps//2,cy-ps//2,cx+ps//2,cy+ps//2))
# M4 bridge
top.shapes(M4).insert(pya.Box(um(bridge_end-route_w/2),um(outn_h_y-route_w/2),um(bridge_start+route_w/2),um(outn_h_y+route_w/2)))
# Via M4->M5
cx=um(bridge_end)
top.shapes(M4).insert(pya.Box(cx-ps//2,cy-ps//2,cx+ps//2,cy+ps//2))
top.shapes(Via4).insert(pya.Box(cx-vs//2,cy-vs//2,cx+vs//2,cy+vs//2))
top.shapes(M5).insert(pya.Box(cx-ps//2,cy-ps//2,cx+ps//2,cy+ps//2))
# M5 from bridge end to channel
top.shapes(M5).insert(pya.Box(um(lo_chan_x_n-route_w/2),um(outn_h_y-route_w/2),um(bridge_end+route_w/2),um(outn_h_y+route_w/2)))
# Channel vertical
top.shapes(M5).insert(pya.Box(um(lo_chan_x_n-route_w/2),um(outn_h_y-route_w/2),um(lo_chan_x_n+route_w/2),um(mix_lon_y+route_w/2)))
# Into Mixer
top.shapes(M5).insert(pya.Box(um(lo_chan_x_n-route_w/2),um(mix_lon_y-route_w/2),um(mix_lo_x+route_w/2),um(mix_lon_y+route_w/2)))

layout.write(base + "lo_test.gds")
print("Done - LO routes only")
