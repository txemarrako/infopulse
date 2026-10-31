import streamlit as st
import urllib.request
import xml.etree.ElementTree as ET

st.set_page_config(page_title="InfoPulse PRO", page_icon="📰", layout="centered")

PERIODICOS = {
    "El País": {"rss": "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/portada", "color": "#002b49", "tag": "Nacional"},
    "20 Minutos": {"rss": "https://www.20minutos.es/rss/", "color": "#00539b", "tag": "Nacional"},
    "El Mundo": {"rss": "https://e00-elmundo.uecdn.es/elmundo/rss/portada.xml", "color": "#0d47a1", "tag": "Nacional"},
    "La Vanguardia": {"rss": "https://www.lavanguardia.com/rss/home.xml", "color": "#001a35", "tag": "Nacional"},
    "Heraldo": {"rss": "https://www.heraldo.es/index.php/mod.portadas/mem.rss", "color": "#b45309", "tag": "Aragón"},
    "La Voz": {"rss": "https://www.lavozdegalicia.es/portada/index.xml", "color": "#0369a1", "tag": "Galicia"},
    "El Correo": {"rss": "https://www.elcorreo.com/rss/2.0/portada/", "color": "#b91c1c", "tag": "País Vasco"},
    "Sur": {"rss": "https://www.diariosur.es/rss/2.0/portada/", "color": "#15803d", "tag": "Andalucía"}
}

st.markdown("<h2 style='text-align: center;'>📰 InfoPulse PRO</h2>", unsafe_allow_html=True)

seleccion = st.selectbox("Selecciona un periódico:", list(PERIODICOS.keys()))
data = PERIODICOS[seleccion]

try:
    req = urllib.request.Request(data["rss"], headers={'User-Agent': 'Mozilla/5.0'})
    xml_data = urllib.request.urlopen(req, timeout=5).read()
    items = ET.fromstring(xml_data).findall('.//item')[:5]
    
    st.markdown(f"""
        <div style="background: {data['color']}; padding: 15px; border-radius: 10px; color: white; margin-bottom: 15px;">
            <h3 style="margin: 0; color: white;">{seleccion}</h3>
            <span style="font-size: 11px; background: rgba(255,255,255,0.2); padding: 2px 6px; border-radius: 6px;">Edición {data['tag']}</span>
        </div>
    """, unsafe_allow_html=True)
    
    for i, item in enumerate(items, 1):
        t = item.find('title').text.strip() if item.find('title') is not None else ""
        l = item.find('link').text.strip() if item.find('link') is not None else "#"
        if i == 1:
            st.markdown(f"""
            <div style="background: #fff; border-left: 5px solid {data['color']}; padding: 12px; border-radius: 8px; margin-bottom: 10px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                <span style="background: #fee2e2; color: #dc2626; font-size: 9px; font-weight: bold; padding: 2px 6px; border-radius: 4px;">DESTACADA</span>
                <p style="margin: 6px 0; font-weight: bold; font-size: 14px; color: #111;">{t}</p>
                <a href="{l}" target="_blank" style="color: {data['color']}; font-size: 12px; text-decoration: none;">Leer completa &rarr;</a>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background: #f8fafc; padding: 10px; border-radius: 6px; margin-bottom: 8px;">
                <p style="margin: 0 0 4px 0; font-size: 13px; color: #333;">{t}</p>
                <a href="{l}" target="_blank" style="color: #666; font-size: 11px; text-decoration: none;">Ver fuente ↗</a>
            </div>
            """, unsafe_allow_html=True)
except:
    st.error("⚠️ No se pudo cargar el periódico en este momento.")
