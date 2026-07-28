import pya

BLOCKS = {
    "LNA_77G_XTOR": "/home/bthomas3/Videos/77GHz_phased_array/layout/LNA_77G_XTOR.gds",
    "MIXER_77G_XTOR": "/home/bthomas3/Videos/77GHz_phased_array/layout/MIXER_77G_XTOR.gds",
    "TXPA_77G_XTOR": "/home/bthomas3/Videos/77GHz_phased_array/layout/TXPA_77G_XTOR.gds",
    "IFA_77G_XTOR": "/home/bthomas3/Videos/77GHz_phased_array/layout/IFA_77G_XTOR.gds",
}

LVS_DIR = "/home/bthomas3/Videos/77GHz_phased_array/lvs"

for cell_name, gds_path in BLOCKS.items():
    print(f"Exporting {cell_name} from {gds_path}...")
    src = pya.Layout()
    src.read(gds_path)

    # List top cells and find matching one
    top_cells = src.top_cells()
    top_names = [c.name for c in top_cells]
    print(f"  Top cells: {top_names}")
    # Use the cell matching cell_name, or first top cell
    match = [c for c in top_cells if c.name == cell_name]
    if match:
        cell_idx = match[0].cell_index()
    else:
        # Use first top cell
        cell_idx = top_cells[0].cell_index()
        print(f"  Using '{top_cells[0].name}' as source")

    out = pya.Layout()
    out.dbu = src.dbu
    out_top = out.create_cell(cell_name)
    out_top.copy_tree(src.cell(cell_idx))

    out_path = f"{LVS_DIR}/{cell_name}_lvs.gds"
    out.write(out_path)
    print(f"  Exported to {out_path}, cells: {out.cells()}")

print("\nAll blocks exported.")
