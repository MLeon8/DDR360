def get_color(price_per_sqm, color_scheme):
    for key in color_scheme:
        if price_per_sqm >= key[0] and price_per_sqm < key[1]:
            return color_scheme[key]
    return 'gray'  # Color por defecto si no se encuentra en ningún rango
