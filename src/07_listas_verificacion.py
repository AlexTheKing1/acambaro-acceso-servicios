"""07 · Listas para verificar con imágenes satelitales y Street View.

Sin trabajo de campo, la validación se hace mirando imágenes históricas de
Google Earth y Street View. Este script prepara dos tablas en docs/:

  verificar_zonas_nuevas.csv     cada zona de crecimiento (2010–2020 y posterior a 2020)
  verificar_servicios_muestra.csv  muestra aleatoria del catálogo de servicios

"Zona" = grupo de manzanas nuevas (criterio D03/D12) contiguas o separadas por
menos de DIST_ZONA metros, dentro de la misma localidad y el mismo periodo. Se
agrupan para no pedir que se revise cuadra por cuadra un mismo fraccionamiento.

Las columnas "existe_en_imagen" y "notas" quedan vacías para quien revise.
"""

from pathlib import Path

import geopandas as gpd
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
P = RAIZ / "data" / "processed"
DOCS = RAIZ / "docs"
DIST_ZONA = 30           # m
SEMILLA = 20261022       # la muestra se puede repetir exactamente
MUESTRA_ACAMBARO = 5     # sedes por estrato dentro del municipio
MUESTRA_FRANJA = 2       # sedes por estrato en la franja de 10 km
# Se revisan completos (son pocos y pesan mucho en el resultado): salud de primer
# nivel y bachillerato dentro del municipio, y todos los mercados.
COMPLETOS = ["salud_primer_nivel", "bachillerato"]

ENLACE_SATELITE = "https://www.google.com/maps/@{lat:.6f},{lon:.6f},300m/data=!3m1!1e3"
ENLACE_STREET_VIEW = "https://www.google.com/maps/@?api=1&map_action=pano&viewpoint={lat:.6f},{lon:.6f}"

QUE_VER = {
    "2010-2020": "¿En la imagen de 2010 el terreno estaba vacío y en la de 2020 ya hay casas o calles?",
    "posterior a 2020": "¿En la imagen de 2020 el terreno estaba vacío y en la más reciente ya hay casas o calles?",
}


def zonas(capa, periodo, nombres, pob):
    m = gpd.read_file(P / "manzanas_cambios.gpkg", layer=capa)
    m = m[m.geometria_nueva].copy()
    filas = []
    for loc, sel in m.groupby("CVE_LOC"):
        grupos = gpd.GeoDataFrame(geometry=[sel.buffer(DIST_ZONA / 2).union_all()], crs=m.crs).explode(ignore_index=True)
        j = gpd.sjoin(sel, grupos, predicate="intersects", how="left")
        j = j[~j.index.duplicated()]
        for _, s in j.groupby("index_right"):
            forma = s.geometry.union_all()
            centro = gpd.GeoSeries([forma.representative_point()], crs=m.crs).to_crs("EPSG:4326").iloc[0]
            p = pob.reindex(s.CVEGEO)
            filas.append({
                "periodo": periodo, "cve_loc": loc, "localidad": nombres.get(loc, ""),
                "n_cuadras": len(s),
                "superficie_ha": round(s.area_m2.sum() / 10_000, 2),
                "pob_2020": int(p.sum()) if periodo == "2010-2020" and p.notna().any() else None,
                "localidad_ya_cartografiada": bool(s.localidad_ya_cartografiada.all()),
                "lat": round(centro.y, 6), "lon": round(centro.x, 6),
                "enlace_satelite": ENLACE_SATELITE.format(lat=centro.y, lon=centro.x),
                "que_verificar": QUE_VER[periodo] if s.localidad_ya_cartografiada.all() else
                QUE_VER[periodo] + " (La localidad no tenía cartografía en 2010: puede que las casas ya existieran.)",
                "claves_cuadras": " ".join(sorted(s.CVEGEO)),
            })
    return filas


def lista_zonas():
    # Nombres del MG EIC 2025 (incluye localidades dibujadas que no aparecen en el ITER 2020)
    loc = gpd.read_file(P / "mg_eic2025_acambaro.gpkg", layer="localidades_amanzanadas")
    nombres = dict(zip(loc.CVE_LOC, loc.NOMGEO))
    mza = gpd.read_file(P / "manzanas2020_poblacion.gpkg", layer="manzanas")
    pob = mza.set_index("CVEGEO").POBTOT
    filas = zonas("mg2020_vs_2010", "2010-2020", nombres, pob) + zonas("eic2025_vs_2020", "posterior a 2020", nombres, pob)
    t = pd.DataFrame(filas).sort_values(["periodo", "localidad", "superficie_ha"], ascending=[True, True, False])
    pref = {"2010-2020": "Z10", "posterior a 2020": "Z20"}
    t.insert(0, "id", [f"{pref[p]}-{i + 1:03d}" for p, i in zip(t.periodo, t.groupby("periodo").cumcount())])
    t["pob_2020"] = t.pob_2020.astype("Int64")
    t["existe_en_imagen"] = ""
    t["notas"] = ""
    t.to_csv(DOCS / "verificar_zonas_nuevas.csv", index=False, encoding="utf-8-sig")
    return t


def lista_servicios():
    s = pd.read_csv(P / "servicios_sedes.csv", dtype={"cve_ent": str, "cve_mun": str, "cve_loc": str})
    s = s[s.analizado].copy()
    # Estratos: tipo × fuentes (solo MG, solo DENUE, ambas) × dentro/fuera del
    # municipio para escuelas y salud; tipo de comercio para abasto. Así entran
    # sobre todo los casos dudosos (los que solo aparecen en una fuente).
    s["donde"] = s.en_acambaro.map({True: "Acámbaro", False: "franja 10 km"})
    s["estrato"] = s.tipo + " | " + s.fuentes.where(s.tipo != "abasto", s.subtipo) + " | " + s.donde

    def tomar(g):
        r = g.iloc[0]
        if r.subtipo == "mercado" or (r.tipo in COMPLETOS and r.en_acambaro):
            return g
        n = MUESTRA_ACAMBARO if r.en_acambaro else MUESTRA_FRANJA
        return g.sample(min(len(g), n), random_state=SEMILLA)

    muestra = s.groupby("estrato", group_keys=False)[s.columns.tolist()].apply(tomar)
    out = pd.DataFrame({
        "id": muestra.id_sede, "tipo": muestra.tipo, "subtipo": muestra.subtipo,
        "nombre": muestra.nombre, "fuentes": muestra.fuentes, "sector": muestra.sector,
        "localidad": muestra.localidad, "municipio": muestra.municipio, "entidad": muestra.entidad,
        "lat": muestra.lat, "lon": muestra.lon,
        "enlace_satelite": [ENLACE_SATELITE.format(lat=a, lon=o) for a, o in zip(muestra.lat, muestra.lon)],
        "enlace_street_view": [ENLACE_STREET_VIEW.format(lat=a, lon=o) for a, o in zip(muestra.lat, muestra.lon)],
        "que_verificar": "¿Se ve en la imagen o en Street View un edificio de este tipo (escuela, centro de salud, tienda o mercado) en el punto o a menos de una cuadra?",
        "existe_en_imagen": "", "notas": "", "estrato": muestra.estrato,
    }).sort_values(["tipo", "fuentes", "id"])
    out.to_csv(DOCS / "verificar_servicios_muestra.csv", index=False, encoding="utf-8-sig")
    return out, s.estrato.value_counts()


def main():
    z = lista_zonas()
    print(z.groupby(["periodo", "localidad_ya_cartografiada"]).agg(zonas=("id", "size"), cuadras=("n_cuadras", "sum"),
                                                                    ha=("superficie_ha", "sum")).to_string())
    print(z[z.periodo == "posterior a 2020"][["id", "localidad", "n_cuadras", "superficie_ha"]].to_string())
    if (P / "servicios_sedes.csv").exists():
        m, estratos = lista_servicios()
        print(f"\nmuestra de servicios: {len(m)} sedes")
        print(pd.DataFrame({"universo": estratos, "muestra": m.estrato.value_counts()}).fillna(0).astype(int).to_string())


if __name__ == "__main__":
    main()
