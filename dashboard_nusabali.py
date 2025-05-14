import streamlit as st
import pandas as pd

# --- Load dataset ---
df = pd.read_csv("dataset_tempat_wisata_bali.csv")

# Pastikan kolom rating diproses dengan benar
df['rating'] = df['rating'].astype(str).str.replace(',', '.').astype(float)

# Hapus baris dengan rating kosong
df_clean = df.dropna(subset=['rating'])

# --- Sidebar: Input User ---
st.sidebar.title("Filter Wisata")

# Pilihan kategori
kategori_options = sorted(df_clean['kategori'].dropna().unique())
kategori = st.sidebar.selectbox("Pilih Kategori Wisata", kategori_options)

# Pilihan kabupaten/kota
kabupaten_options = sorted(df_clean['kabupaten_kota'].dropna().unique())
kabupaten = st.sidebar.selectbox("Pilih Kabupaten/Kota", kabupaten_options)

# Pilihan rating minimal
rating_min = st.sidebar.slider("Pilih Rating Minimal", min_value=1.0, max_value=5.0, value=4.0, step=0.1)

# Tombol untuk menampilkan hasil
if st.sidebar.button("Tampilkan Rekomendasi"):
    # Filter berdasarkan input pengguna
    hasil = df_clean[
        (df_clean['kategori'].str.lower() == kategori.lower()) &
        (df_clean['kabupaten_kota'].str.lower() == kabupaten.lower()) &
        (df_clean['rating'] >= rating_min)
    ]

    st.subheader("Daftar Rekomendasi Tempat Wisata")

    if not hasil.empty:
        for i, row in hasil.iterrows():
            # Menampilkan gambar dengan ukuran yang lebih kecil
            if 'link_gambar' in row and pd.notna(row['link_gambar']):
                st.image(row['link_gambar'], caption=row['nama'], use_container_width=True)

            # Menampilkan informasi lainnya
            st.markdown(f"{row['nama']}  \n"
                        f"Kategori: {row['kategori']}  \n"
                        f"Kabupaten/Kota: {row['kabupaten_kota']}  \n"
                        f"Rating: {row['rating']}  \n")

            # Tombol "Rute" untuk membuka Google Maps
            if 'link' in row and pd.notna(row['link']):
                google_maps_route_url = f"https://www.google.com/maps/dir/Denpasar/{row['link']}"
                st.link_button(f"Rute ke {row['nama']}", google_maps_route_url)

            st.markdown("---")
    else:
        st.warning("Tidak ada tempat wisata yang sesuai dengan kriteria.")

# --- Main: Tampilkan seluruh data jika belum memilih ---
else:
    st.title("Daftar Tempat Wisata di Bali")
    for i, row in df_clean.iterrows():
        # Menampilkan gambar dengan ukuran yang lebih kecil
        if 'link_gambar' in row and pd.notna(row['link_gambar']):
            st.image(row['link_gambar'], caption=row['nama'], use_container_width=True)

        # Menampilkan informasi lainnya
        st.markdown(f"{row['nama']}  \n"
                    f"Kategori: {row['kategori']}  \n"
                    f"Kabupaten/Kota: {row['kabupaten_kota']}  \n"
                    f"Rating: {row['rating']}  \n")

        # Tombol "Rute" untuk membuka Google Maps
        if 'link' in row and pd.notna(row['link']):
            google_maps_route_url = f"https://www.google.com/maps/dir/Denpasar/{row['link']}"
            st.link_button(f"Rute ke {row['nama']}", google_maps_route_url)

        st.markdown("---")
