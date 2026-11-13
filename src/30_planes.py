"""30 · Planes oficiales: verificación de citas, Irámuco y proyección contra censo (fase 6; D62, D63).

Documentos (release "datos-crudos", 01_descargar.py --solo planes):
  - Plan Municipal de Desarrollo Acámbaro 2030, COPLADEM Acámbaro 2003–2006.
    La página del PDF coincide con la página impresa.
  - Programa Regional de Ordenamiento Territorial de la Subregión 10 (SEDATU–IPLANEG, 2014).
    Página impresa = página del PDF − 1. Aquí se cita siempre la página impresa.

1. Extrae el texto (pdftotext -layout) y verifica que cada cita usada en
   docs/contraste_planes.md esté en la página citada -> docs/verificar_citas_planes.csv.
2. Irámuco (0027): ITER 2000, 2005, 2010 y 2020. 2000 y 2005 solo traen población y
   viviendas habitadas; 2010 y 2020, también totales, deshabitadas y de uso temporal.
   La EIC 2025 no publica localidades de menos de 50 000 hab. -> iramuco_serie.csv.
3. Proyectado contra censado: cifras transcritas de los planes (con página y cuadro)
   y población censada (ITER 2000, 2005, 2010, 2020; EIC 2025 con IC 90 %) para el
   municipio, la Subregión 10 (Acámbaro, Coroneo, Jerécuaro, Tarandacuao) y la
   ciudad (localidad 0001) -> proyecciones_vs_censo.csv, docs/figuras/fase6_proyeccion.png.
"""

import json
import re
import subprocess
import zipfile
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
RAW = RAIZ / "data" / "raw"
P = RAIZ / "data" / "processed"
FIG = RAIZ / "docs" / "figuras"
DOCS = RAIZ / "docs"

PDF = {"municipal": RAW / "planes" / "plan_municipal_desarrollo_2030.pdf",
       "prot": RAW / "planes" / "prot_subregion10_2014.pdf"}
DESFASE = {"municipal": 0, "prot": 1}   # página del PDF = impresa + desfase
SUBREGION = {"002": "Acámbaro", "010": "Coroneo", "019": "Jerécuaro", "038": "Tarandacuao"}
Z90 = 1.645

# Citas usadas en docs/contraste_planes.md: (id, documento, página impresa, texto que debe aparecer)
CITAS = [
    ("mun_migracion", "municipal", 18, "considerado como de muy alta migración"),
    ("mun_pob_1980_2006", "municipal", 18, "98,126 habitantes en 1980 a una de 115,121 en el 2006"),
    ("mun_turnos_emigracion", "municipal", 31, "emigración y la baja población que existe en edad escolar"),
    ("mun_derechohabiencia_2006", "municipal", 34, "Para 2006 se tuvo una disminución considerable a 19.01%"),
    ("mun_conapo_fuente", "municipal", 34, "Proyección de Población del Consejo Nacional de Población (CONAPO) 2000-2030"),
    ("mun_polos", "municipal", 6, "microregiones o polos de desarrollo"),
    ("mun_eje_iramuco", "municipal", 58, "Eje de desarrollo, Irámuco"),
    ("mun_iramuco_viviendas", "municipal", 59, "concentró un total de 3,557 viviendas"),
    ("mun_iramuco_escuelas", "municipal", 60, "11 centros de educación preescolar, 9 primarias y 3 tele secundarias"),
    ("mun_iramuco_concentrador", "municipal", 61, "Irámuco se constituirá como el principal concentrador de población micro regional"),
    ("mun_paracuaro_secundaria", "municipal", 64, "secundaria técnica localizada en la carretera Parácuaro- El Jaral"),
    ("mun_deficit_habitacional", "municipal", 214, "disminuir el déficit habitacional"),
    ("mun_reservas_vivienda", "municipal", 215, "Identificar y adquirir reservas de terreno para las acciones de vivienda"),
    ("mun_fraccionamientos", "municipal", 216, "Mantener estricto control de los fraccionamientos"),
    ("mun_ordenamiento_6_meses", "municipal", 241, "en un plazo no mayor a 6 meses a partir de la publicación de este plan"),
    ("mun_meta_educacion_polos", "municipal", 254, "medio superior al 100% en los Polos de Desarrollo Rural"),
    ("mun_meta_abasto_polos", "municipal", 255, "Cada Polo de Desarrollo contará con plazas públicas para el"),
    ("mun_meta_escuelas_polos", "municipal", 255, "Cada Polo deberá contar con escuelas desde preescolar hasta nivel"),
    ("mun_meta_salud_polos", "municipal", 255, "Crear centros comunitarios de salud en cada polo de desarrollo"),
    ("prot_pob_2010", "prot", 29, "183 mil 194 personas"),
    ("prot_ciudad_pct", "prot", 30, "alberga al 31.64% de la población de la Subregión"),
    ("prot_acambaro_tasas", "prot", 30, "un decremento en sus tasas poblacionales"),
    ("prot_remesas", "prot", 31, "El 20% de las viviendas de la Subregión reciben remesas"),
    ("prot_cuadro3", "prot", 38, "Dotación de equipamiento en la Subregión 10"),
    ("prot_cuadro3_acambaro_2014", "prot", 38, "112,076"),
    ("prot_cuadro3_subregion_2014", "prot", 38, "189,535"),
    ("prot_ciudad_2030", "prot", 42, "con una población esperada de 51,613"),
    ("prot_proyecciones", "prot", 47, "2.2.2.3 Proyecciones de población"),
    ("prot_exponencial", "prot", 47, "La tendencia muestra un crecimiento poblacional exponencial"),
    ("prot_migracion_no_contemplada", "prot", 47, "no parecen contempladas en esta proyección"),
    ("prot_iramuco", "prot", 59, "actualmente haya un fuerte crecimiento poblacional y de desarrollo habitacional"),
    ("prot_crec_2016", "prot", 59, "3.14%"),
    ("prot_crec_2020", "prot", 59, "5.07%"),
    ("prot_crec_2030", "prot", 59, "8.9%"),
]

# Cifras proyectadas transcritas de los planes (D62). tipo: exacta (número escrito) o derivada.
PROYECCIONES = [
    # unidad, año, valor, documento, página, cuadro, tipo, nota
    ("municipio", 2006, 115121, "Plan Municipal", "18 y 34", "tabla 'Población atendida por institución 2006'",
     "exacta", "2006 no fue año censal; la tabla de p. 34 da como fuente la proyección CONAPO 2000-2030"),
    ("municipio", 2014, 112076, "PROT", "38", "Cuadro 3, columna 'Población 2014'", "exacta",
     "proyección (CONAPO 2010-2030, según la fuente del cuadro)"),
    ("subregion", 2014, 189535, "PROT", "38", "Cuadro 3, columna 'Población 2014'", "exacta", "ídem"),
    ("subregion", 2016, None, "PROT", "59", "texto, 'Crecimiento poblacional'", "derivada", "+3.14 % sobre 2010"),
    ("subregion", 2020, None, "PROT", "59", "texto, 'Crecimiento poblacional'", "derivada", "+5.07 % sobre 2010"),
    ("subregion", 2030, None, "PROT", "59", "texto, 'Crecimiento poblacional'", "derivada", "+8.9 % sobre 2010"),
    ("ciudad", 2030, 51613, "PROT", "42", "texto, esquema subregional de ciudades 2030", "exacta", "estimación CONAPO (2010)"),
]
PCT_PROT = {2016: 3.14, 2020: 5.07, 2030: 8.9}
BASE_PROT_2010 = 183194   # PROT p. 29; coincide con la suma del censo 2010 de los 4 municipios


def texto_paginas(doc):
    out = subprocess.run(["pdftotext", "-layout", str(PDF[doc]), "-"], capture_output=True, check=True, text=True).stdout
    return out.split("\f")


def normal(t):
    return re.sub(r"\s+", " ", t).replace("- ", "-")


def leer_iter(fuente, nombre_zip, interno):
    with zipfile.ZipFile(RAW / fuente / nombre_zip) as z, z.open(interno) as f:
        t = pd.read_csv(f, dtype=str, encoding_errors="replace")
    t.columns = [c.upper().replace("ENTIDAD", "ENT") for c in t.columns]
    # El ITER 2005 usa otros nombres de columna
    return t.rename(columns={"P_TOTAL": "POBTOT", "T_VIVHAB": "TOTVIVHAB"})


def main():
    v = {}
    # --- 1. Citas ------------------------------------------------------------------------
    pags = {d: texto_paginas(d) for d in PDF}
    filas = []
    for cid, doc, pag, cad in CITAS:
        t = normal(pags[doc][pag - 1 + DESFASE[doc]])
        ok = normal(cad) in t
        otras = [i + 1 - DESFASE[doc] for i, x in enumerate(pags[doc]) if normal(cad) in normal(x)]
        filas.append({"id": cid, "documento": doc, "pagina_impresa": pag, "texto": cad,
                      "encontrada_en_la_pagina": "sí" if ok else "no", "paginas_donde_aparece": ";".join(map(str, otras))})
    citas = pd.DataFrame(filas)
    citas.to_csv(DOCS / "verificar_citas_planes.csv", index=False)
    v["citas"] = {"total": len(citas), "no_encontradas": citas[citas.encontrada_en_la_pagina == "no"].id.tolist()}

    # --- Censos ---------------------------------------------------------------------------
    it = {
        2000: leer_iter("iter2000", "cgpv2000_iter_11_csv.zip", "cgpv2000_iter_11/conjunto_de_datos/cgpv2000_iter_11.csv"),
        2005: leer_iter("iter2005", "cpv2005_iter_11_csv.zip", "cpv2005_iter_11/conjunto_de_datos/cpv2005_iter_11.csv"),
        2010: leer_iter("iter2010", "iter_11_2010_csv.zip", "iter_11_cpv2010/conjunto_de_datos/iter_11_cpv2010.csv"),
        2020: leer_iter("iter2020", "iter_11_cpv2020_csv.zip", "iter_11_cpv2020/conjunto_de_datos/conjunto_de_datos_iter_11CSV20.csv"),
    }

    def valor(anio, mun, loc, col):
        t = it[anio]
        r = t[(t.MUN == mun) & (t.LOC == loc)]
        if col not in t.columns or not len(r):
            return np.nan
        return pd.to_numeric(r[col].iloc[0], errors="coerce")

    # --- 2. Irámuco ----------------------------------------------------------------------
    hab = {2000: "TOTVIVHAB", 2005: "TOTVIVHAB", 2010: "TVIVHAB", 2020: "TVIVHAB"}
    ir = []
    for a in it:
        ir.append({"anio": a, "fuente": f"ITER {a}", "nombre_en_iter": it[a][(it[a].MUN == "002") & (it[a].LOC == "0027")].NOM_LOC.iloc[0],
                   "POBTOT": valor(a, "002", "0027", "POBTOT"), "VIVTOT": valor(a, "002", "0027", "VIVTOT"),
                   "viviendas_habitadas": valor(a, "002", "0027", hab[a]),
                   "VIVPAR_DES": valor(a, "002", "0027", "VIVPAR_DES"), "VIVPAR_UT": valor(a, "002", "0027", "VIVPAR_UT")})
    ir.append({"anio": 2025, "fuente": "EIC 2025: no publica localidades de menos de 50 000 hab."})
    ir = pd.DataFrame(ir)
    ir["pct_deshabitadas"] = (100 * ir.VIVPAR_DES / ir.VIVTOT).round(1)
    ir.to_csv(P / "iramuco_serie.csv", index=False)
    a, b = ir.set_index("anio").loc[2010], ir.set_index("anio").loc[2020]
    v["iramuco_2010_2020"] = {c: {"2010": a[c], "2020": b[c], "cambio": b[c] - a[c], "cambio_pct": round(100 * (b[c] / a[c] - 1), 1)}
                              for c in ["POBTOT", "VIVTOT", "viviendas_habitadas", "VIVPAR_DES", "VIVPAR_UT"]}

    # --- 3. Proyectado contra censado -------------------------------------------------------
    eic = pd.read_csv(P / "comparacion_regional.csv", dtype={"cve_mun": str})
    cens = []
    for a in it:
        mun = {m: valor(a, m, "0000", "POBTOT") for m in SUBREGION}
        cens += [("municipio", a, mun["002"], None, None, f"ITER {a}"),
                 ("subregion", a, sum(mun.values()), None, None, f"ITER {a} (suma de 4 municipios)"),
                 ("ciudad", a, valor(a, "002", "0001", "POBTOT"), None, None, f"ITER {a}, localidad 0001")]
    e = eic[(eic.nivel == "municipio") & eic.cve_mun.isin(SUBREGION)].set_index("cve_mun")
    se = (e.pob_eic2025_ls90 - e.pob_eic2025_li90) / (2 * Z90)
    s_val, s_se = e.pob_eic2025.sum(), float(np.sqrt((se ** 2).sum()))
    cens.append(("municipio", 2025, e.loc["002", "pob_eic2025"], e.loc["002", "pob_eic2025_li90"], e.loc["002", "pob_eic2025_ls90"], "EIC 2025"))
    cens.append(("subregion", 2025, s_val, s_val - Z90 * s_se, s_val + Z90 * s_se,
                 "EIC 2025 (suma de 4 municipios; IC suponiendo errores independientes)"))
    c = eic[(eic.nivel == "cabecera") & (eic.cve_mun == "002")].iloc[0]
    cens.append(("ciudad", 2025, c.pob_eic2025, c.pob_eic2025_li90, c.pob_eic2025_ls90, "EIC 2025, cabecera"))
    censada = pd.DataFrame(cens, columns=["unidad", "anio", "valor", "li90", "ls90", "fuente"]).assign(serie="censada")
    assert censada.query("unidad == 'subregion' and anio == 2010").valor.iloc[0] == BASE_PROT_2010

    proy = []
    for u, an, val, doc, pag, cuadro, tipo, nota in PROYECCIONES:
        if val is None:
            val = round(BASE_PROT_2010 * (1 + PCT_PROT[an] / 100))
            nota += f" de {BASE_PROT_2010:,} (PROT p. 29)".replace(",", " ")
        proy.append({"unidad": u, "anio": an, "valor": val, "serie": "proyectada", "documento": doc, "pagina": pag,
                     "cuadro": cuadro, "tipo": tipo, "nota": nota})
    tabla = pd.concat([censada, pd.DataFrame(proy)], ignore_index=True)
    tabla.to_csv(P / "proyecciones_vs_censo.csv", index=False)

    cz = censada.set_index(["unidad", "anio"]).valor
    v["proyeccion_vs_censo"] = {
        "subregion_2020_proyectada": round(BASE_PROT_2010 * 1.0507), "subregion_2020_censada": cz[("subregion", 2020)],
        "subregion_diferencia_2020": cz[("subregion", 2020)] - round(BASE_PROT_2010 * 1.0507),
        "municipio_2014_proyectada_PROT": 112076, "municipio_2010": cz[("municipio", 2010)], "municipio_2020": cz[("municipio", 2020)],
        "municipio_2006_plan": 115121, "municipio_2005": cz[("municipio", 2005)], "municipio_2000": cz[("municipio", 2000)],
        "ciudad_2030_proyectada": 51613, "ciudad_2010": cz[("ciudad", 2010)], "ciudad_2020": cz[("ciudad", 2020)],
        "ciudad_2020_interpolada_lineal_2010_2030": round(cz[("ciudad", 2010)] + (51613 - cz[("ciudad", 2010)]) / 2),
        "ciudad_pct_prot_p30_x_pob_2010": round(0.3164 * BASE_PROT_2010),
        "nota_definicion_ciudad": "PROT p. 30: la ciudad tiene 31.64 % de 183 194 = 57 963 hab., igual a la localidad 0001 del censo 2010 (57 972): misma definición",
        "censada": {f"{u} {an}": val for (u, an), val in cz.items()},
    }
    figura(tabla)

    # --- Punto de verificación en campo: secundaria técnica de Parácuaro ---------------------
    # Plan Municipal p. 64: "secundaria técnica localizada en la carretera Parácuaro- El Jaral".
    # D39: la ST 24 (11DST0024Y) está en la carretera Acámbaro–Parácuaro km 9. No se asume cuál
    # es correcta (otra escuela o reubicación). Lista aparte para no tocar docs/verificar_campo.csv.
    sed = pd.read_csv(P / "servicios_sedes_fase4.csv", dtype=str)
    st = sed[sed.claves_sep_clues.fillna("").str.contains("11DST0024Y")].iloc[0]
    pd.DataFrame([{
        "orden": 1, "id": st.id_sede, "tipo": "secundaria", "nombre": st.nombre, "clave_sep": "11DST0024Y",
        "localidad_catalogo": st.localidad,
        "motivo": "Plan Municipal (p. 64) la ubica en la carretera Parácuaro–El Jaral; D39, en la carretera "
                  "Acámbaro–Parácuaro km 9. Confirmar si es la misma escuela, si se reubicó o si hay otra secundaria técnica.",
        "lat": st.lat, "lon": st.lon,
        "enlace_google_maps": f"https://www.google.com/maps/search/?api=1&query={st.lat},{st.lon}",
        "existe_campo": "", "fecha_visita": "", "foto": "", "notas": ""}]).to_csv(DOCS / "verificar_campo_fase6.csv", index=False)

    f = P / "validacion_fase6.json"
    todo = json.loads(f.read_text()) if f.exists() else {}
    todo["planes"] = v
    f.write_text(json.dumps(todo, ensure_ascii=False, indent=1, default=lambda x: x.item() if hasattr(x, "item") else str(x)))
    print(citas[["id", "pagina_impresa", "encontrada_en_la_pagina", "paginas_donde_aparece"]].to_string())
    print(ir.to_string())
    print(tabla.to_string())
    print(json.dumps(v["proyeccion_vs_censo"], ensure_ascii=False, indent=1, default=lambda x: x.item() if hasattr(x, "item") else str(x)))


def figura(t):
    AZUL, GRIS, TINTA, TINTA2 = "#2a78d6", "#52514e", "#0b0b0b", "#52514e"
    paneles = [("municipio", "Municipio de Acámbaro"), ("subregion", "Subregión 10 (Acámbaro, Coroneo,\nJerécuaro, Tarandacuao)"),
               ("ciudad", "Ciudad de Acámbaro (localidad 0001)")]
    fig, axs = plt.subplots(1, 3, figsize=(13, 4.6))
    for ax, (u, tit) in zip(axs, paneles):
        c = t[(t.unidad == u) & (t.serie == "censada")].sort_values("anio")
        p = t[(t.unidad == u) & (t.serie == "proyectada")].sort_values("anio")
        ax.plot(c.anio, c.valor / 1000, color=AZUL, lw=2, marker="o", ms=8, mec="white", mew=1.5, zorder=3, label="Censada (INEGI)")
        e = c[c.li90.notna()]
        ax.errorbar(e.anio, e.valor / 1000, yerr=[(e.valor - e.li90) / 1000, (e.ls90 - e.valor) / 1000],
                    fmt="none", ecolor=AZUL, elinewidth=1.2, capsize=4, zorder=2)
        if len(p):
            ax.plot(p.anio, p.valor / 1000, color=GRIS, lw=2, ls="--", marker="o", ms=8, mfc="white", mec=GRIS, mew=2,
                    zorder=4, label="Proyectada en los planes")
        for _, r in c.iterrows():
            ax.annotate(f"{r.valor/1000:.1f}", (r.anio, r.valor / 1000), xytext=(0, -15), textcoords="offset points",
                        ha="center", fontsize=8, color=TINTA2)
        for _, r in p.iterrows():
            izq = u == "subregion" and r.anio == 2014   # evita que choque con 2016
            ax.annotate(f"{r.valor/1000:.1f}", (r.anio, r.valor / 1000), xytext=(-6, 8) if izq else (0, 9),
                        textcoords="offset points", ha="right" if izq else "center", fontsize=8, color=TINTA2)
        ax.set_title(tit, loc="left", fontsize=11, color=TINTA)
        ax.set_xlim(1997, 2033)
        ax.set_xticks([2000, 2005, 2010, 2015, 2020, 2025, 2030])
        lo = min(c.li90.min() if c.li90.notna().any() else c.valor.min(), c.valor.min(), p.valor.min() if len(p) else np.inf) / 1000
        hi = max(c.ls90.max() if c.ls90.notna().any() else c.valor.max(), c.valor.max(), p.valor.max() if len(p) else 0) / 1000
        pad = (hi - lo) * 0.15
        ax.set_ylim(lo - pad, hi + pad)
        ax.grid(axis="y", color="#e6e5e0", lw=0.8)
        ax.set_axisbelow(True)
        for s in ["top", "right"]:
            ax.spines[s].set_visible(False)
        ax.tick_params(colors=TINTA2, labelsize=9)
        ax.set_ylabel("miles de habitantes", fontsize=9, color=TINTA2)
    h, lab = axs[0].get_legend_handles_labels()
    fig.legend(h, lab, loc="upper right", ncol=2, frameon=False, fontsize=9, bbox_to_anchor=(0.99, 0.985))
    fig.suptitle("Población proyectada en los planes contra población censada", x=0.01, ha="left", fontsize=13, color=TINTA)
    fig.text(0.01, 0.01,
             "Censada: INEGI, ITER de los censos 2000, 2010 y 2020 y del II Conteo 2005; 2025 = Encuesta Intercensal (barra = intervalo de 90 %). "
             "Cada panel tiene su propia escala. "
             "Proyectada: Plan Municipal 2030 (2006, p. 18 y 34); PROT Subregión 10 (2014: cuadro 3, p. 38; "
             "2016–2030: % de p. 59 sobre 2010; ciudad 2030: p. 42).",
             fontsize=7, color=TINTA2, wrap=True)
    fig.tight_layout(rect=(0, 0.04, 1, 0.94))
    fig.savefig(FIG / "fase6_proyeccion.png", dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    main()
