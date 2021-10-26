# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
#Mengakses API
import requests
resp = requests.get('https://data.covid19.go.id/public/api/update.json')


# %%
print(resp)


# %%
print(resp.headers)


# %%
#ekstrak isi respon
cov_id_raw = resp.json()
cov_id_raw


# %%
print('Length of cov_id_raw : %d.' %len(cov_id_raw))
print('Komponen cov_id_raw  : %s.' %cov_id_raw.keys())
cov_id_update = cov_id_raw['update']
cov_id_update


# %%
#analisis data
print('Tanggal pembaharuan data penambahan kasus :', cov_id_update['penambahan']['tanggal'])
print('Jumlah penambahan kasus sembuh :', cov_id_update['penambahan']['jumlah_sembuh'])
print('Jumlah penambahan kasus meninggal :', cov_id_update['penambahan']['jumlah_meninggal'])
print('Jumlah total kasus positif hingga saat ini :', cov_id_update['total']['jumlah_positif'])
print('Jumlah total kasus meninggal hingga saat ini:', cov_id_update['total']['jumlah_meninggal'])


# %%
import requests
resp_jatim = requests.get('https://data.covid19.go.id/public/api/prov_detail_JAWA_TIMUR.json')
cov_jatim_raw = resp_jatim.json()


# %%
print(resp_jatim)


# %%
print('Nama-nama elemen utama:\n', cov_jatim_raw.keys())
print('\nJumlah total kasus COVID-19 di Jawa Timur : %d' %cov_jatim_raw['kasus_total'])
print('Persentase kematian akibat COVID-19 di Jawa Timur : %f%%' %cov_jatim_raw['meninggal_persen'])
print('Persentase tingkat kesembuhan dari COVID-19 di Jawa Timur : %f%%' %cov_jatim_raw['sembuh_persen'])


# %%
cov_jabar_raw


# %%
#mendapatkan informasi yang lebih lengkap
import numpy as np
import pandas as pd
cov_jatim = pd.DataFrame(cov_jatim_raw['list_perkembangan'])
print('Info cov_jatim:\n', cov_jatim.info())
print('\nLima data teratas cov_jatim:\n', cov_jatim.head())


# %%
#menjinakkan data
cov_jatim_tidy = (cov_jatim.drop(columns=[item for item in cov_jatim.columns
                                          if item.startswith('AKUMULASI')
                                          or item.startswith('DIRAWAT')])
.rename(columns=str.lower)
.rename(columns={'kasus': 'kasus_baru'})
)
cov_jatim_tidy['tanggal'] = pd.to_datetime(cov_jatim_tidy['tanggal']*1e6, unit='ns')
print('Lima data teratas:\n', cov_jatim_tidy.head())


# %%
cov_jatim_tidy.shape


# %%
cov_jatim_tidy.isnull().sum()


# %%
cov_jatim_tidy.to_csv('D:\\downloads\\DATASET-DATASCIENCE-20211015T124508Z-001\\Analisis Data Covid di Indonesia\\data-API-Jatim.csv')


# %%
#visualisasi data
import matplotlib.pyplot as plt

plt.clf()
fig, ax = plt.subplots(figsize=(10,5))
ax.bar(data=cov_jatim_tidy, x='tanggal', height='kasus_baru')
plt.show()


# %%
#grafik kasus baru
import matplotlib.dates as mdates
plt.clf()
fig, ax = plt.subplots(figsize=(10,5))
ax.bar(data=cov_jatim_tidy, x='tanggal', height='kasus_baru', color='salmon')
fig.suptitle('Kasus Harian Positif COVID-19 di Jawa Timur', 
             y=1.00, fontsize=16, fontweight='bold', ha='center')
ax.set_title('Terjadi pelonjakan kasus di awal bulan Agustus',
             fontsize=10)
ax.set_xlabel('')
ax.set_ylabel('Jumlah kasus')
ax.text(1, -0.3, 'Sumber data: covid.19.go.id', color='blue',
        ha='right', transform=ax.transAxes)
ax.set_xticklabels(ax.get_xticks(), rotation=90)

ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

plt.grid(axis='y')
plt.tight_layout()
plt.show()


# %%
#grafik kasus sembuh
plt.clf()
fig, ax = plt.subplots(figsize=(10,5))
ax.bar(data=cov_jatim_tidy, x='tanggal', height='sembuh', color='olivedrab')
ax.set_title('Kasus Harian Sembuh Dari COVID-19 di Jawa Timur',
fontsize=22)
ax.set_xlabel('')
ax.set_ylabel('Jumlah kasus')
ax.text(1, -0.3, 'Sumber data: covid.19.go.id', color='blue',
        ha='right', transform=ax.transAxes)
ax.set_xticklabels(ax.get_xticks(), rotation=90)

ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

plt.grid(axis='y')
plt.tight_layout()
plt.show()


# %%
#grafik kasus meninggal
plt.clf()
fig, ax = plt.subplots(figsize=(10,5))
ax.bar(data=cov_jatim_tidy, x='tanggal', height='meninggal', color='slategrey')
ax.set_title('Kasus Harian Meninggal Dari COVID-19 di Jawa Timur',
fontsize=22)
ax.set_xlabel('')
ax.set_ylabel('Jumlah kasus')
ax.text(1, -0.3, 'Sumber data: covid.19.go.id', color='blue',
        ha='right', transform=ax.transAxes)
ax.set_xticklabels(ax.get_xticks(), rotation=90)

ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

plt.grid(axis='y')
plt.tight_layout()
plt.show()


# %%
#cek pekan ini
cov_jatim_pekanan = (cov_jatim_tidy.set_index('tanggal')['kasus_baru']
					  .resample('W')
					  .sum()
					  .reset_index()
					  .rename(columns={'kasus_baru': 'jumlah'})
                    )
cov_jatim_pekanan['tahun'] = cov_jatim_pekanan['tanggal'].apply(lambda x: x.year)
cov_jatim_pekanan['pekan_ke'] = cov_jatim_pekanan['tanggal'].apply(lambda x: x.weekofyear)
cov_jatim_pekanan = cov_jatim_pekanan[['tahun', 'pekan_ke', 'jumlah']].sort_values(['tahun', 'pekan_ke'], ascending=[False, False])

print('Info cov_jatim_pekanan:')
print(cov_jatim_pekanan.info())
print('\nLima data teratas cov_jatim_pekanan:\n', cov_jatim_pekanan)


# %%
cov_jatim_pekanan['jumlah_pekanlalu'] = cov_jatim_pekanan['jumlah'].shift().replace(np.nan, 0).astype(np.int)
cov_jatim_pekanan['lebih_baik'] = cov_jatim_pekanan['jumlah'] < cov_jatim_pekanan['jumlah_pekanlalu']

print('Sepuluh data teratas:\n', cov_jatim_pekanan.head(10))


# %%
cov_jatim_pekanan.to_csv('D:\\downloads\\DATASET-DATASCIENCE-20211015T124508Z-001\\Analisis Data Covid di Indonesia\\data-API-Jatim-pekanan.csv')


# %%
#bar chart
plt.clf()
jml_tahun_terjadi_covid19 = cov_jatim_pekanan['tahun'].nunique()
tahun_terjadi_covid19 = cov_jatim_pekanan['tahun'].unique()
fig, axes = plt.subplots(nrows=jml_tahun_terjadi_covid19,
						 figsize = (10,3*jml_tahun_terjadi_covid19))

fig.suptitle('Kasus Pekanan Positif COVID-19 di Jawa Timur',
			 y=1.00, fontsize=16, fontweight='bold', ha='center')
for i, ax in enumerate(axes):
	ax.bar(data=cov_jatim_pekanan.loc[cov_jatim_pekanan['tahun']==tahun_terjadi_covid19[i]],
	   x='pekan_ke', height='jumlah',
	   color=['mediumseagreen' if x is True else 'salmon'
		 	for x in cov_jatim_pekanan['lebih_baik']])
	if i == 0:
		 ax.set_title('Kolom hijau menunjukan penambahan kasus baru lebih sedikit dibandingkan satu pekan sebelumnya',
					   fontsize=10)
	elif i == jml_tahun_terjadi_covid19-1 :
			ax.text(1, -0.2, 'Sumber data: covid.19.go.id', color='blue',
					ha='right', transform=ax.transAxes)
					   
	ax.set_xlim([0, 52.5])
	ax.set_ylim([0, max(cov_jatim_pekanan['jumlah'])])
	ax.set_xlabel('Pekan ke-')
	ax.set_ylabel('Jumlah kasus %d'%(tahun_terjadi_covid19[i],))
	ax.grid(axis='y')

plt.tight_layout()
plt.show()


# %%
#pola dan dinamika
cov_jatim_akumulasi = cov_jatim_tidy[['tanggal']].copy()
cov_jatim_akumulasi['akumulasi_aktif'] = (cov_jatim_tidy['kasus_baru'] - cov_jatim_tidy['sembuh'] - cov_jatim_tidy['meninggal']).cumsum()
cov_jatim_akumulasi['akumulasi_sembuh'] = cov_jatim_tidy['sembuh'].cumsum()
cov_jatim_akumulasi['akumulasi_meninggal'] = cov_jatim_tidy['meninggal'].cumsum()
print(cov_jatim_akumulasi.tail())


# %%
cov_jatim_akumulasi.to_csv('D:\\downloads\\DATASET-DATASCIENCE-20211015T124508Z-001\\Analisis Data Covid di Indonesia\\data-API-Jatim-akumulasi.csv')


# %%
#Line Chart
plt.clf()
fig, ax = plt.subplots(figsize=(10,5))
ax.plot('tanggal', 'akumulasi_aktif', data=cov_jatim_akumulasi, lw=2)

ax.set_title('Akumulasi aktif COVID-19 di Jawa Timur',
             fontsize=22)
ax.set_xlabel('')
ax.set_ylabel('Akumulasi aktif')
ax.text(1, -0.3, 'Sumber data: covid.19.go.id', color='blue',
        ha='right', transform=ax.transAxes)
ax.set_xticklabels(ax.get_xticks(), rotation=90)

ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

plt.grid()
plt.tight_layout()
plt.show()


# %%
plt.clf()
fig, ax = plt.subplots(figsize=(10,5))
cov_jatim_akumulasi_ts = cov_jatim_akumulasi.set_index('tanggal')
cov_jatim_akumulasi_ts.plot(kind='line', ax=ax, lw=3, color=['salmon','slategrey','olivedrab'])

ax.set_title('Dinamika Kasus COVID-19 di Jawa Timur', fontsize=22)
ax.set_xlabel('')
ax.set_ylabel('Akumulasi aktif')
ax.text(1, -0.3, 'Sumber data: covid.19.go.id', color='blue', ha='right', transform=ax.transAxes)

plt.grid()
plt.tight_layout()
plt.show()			


# %%
cov_jatim_akumulasi_ts.to_csv('D:\\downloads\\DATASET-DATASCIENCE-20211015T124508Z-001\\Analisis Data Covid di Indonesia\\data-API-Jatim-Akumulasi-ts.csv')


# %%



