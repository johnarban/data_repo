# Data Credits




- `weic2403c.tif`, `weic2403c.jpg` — JWST NGC 628
  - https://esawebb.org/images/weic2403c/

- `potm2208a.tif`, `potm2208a.jpg` — JWST M74 (Phantom Galaxy)
  - https://esawebb.org/images/potm2208a/

- `sci25001a.jpg` — ESA/Webb "edge of the Phantom Galaxy"
  - https://esahubble.org/images/sci25001a/

- `Hubble Full Res (For Print).tif`, `ngc 628 Hubble Full Res (For Display).png` — Hubble NGC 628
  - https://science.nasa.gov/asset/webb/webb-and-hubbles-views-of-spiral-galaxy-ngc-628/
  - STScI release 2024-105

- `stsci_2024-105c_1280.jpg` — Hubble/Webb NGC 628 comparison
  - https://webbtelescope.org/contents/media/images/2024/105/
  - STScI release 2024-105

- `noao-m74mortfieldw.tif`, `noao-m74mortfieldw.jpg` — NOIRLab/Kitt Peak M74
  - https://noirlab.edu/public/images/noao-m74mortfieldw/
  - file: https://storage.noirlab.edu/media/archives/images/original/noao-m74mortfieldw.tif

- `ssc2023-01b.tif`, `spitzer_ssc2023-01b_1600.jpg` — Spitzer M74
  - https://www.spitzer.caltech.edu/image/ssc2023-01b-dusty-forming-stars-in-the-phantom-galaxy-m74
  - file via AstroPix: https://www.astropix.org/archive/spitzer/ssc2023-01b/spitzer_ssc2023-01b_1600.jpg

- `PIA14098_fig1.tif`, `PIA14098_fig5_NGC_628.tif` — WISE NGC 628
  - https://photojournal.jpl.nasa.gov/catalog/PIA14098
  - file: https://assets.science.nasa.gov/content/dam/science/psd/photojournal/pia/pia14/pia14098/tiff/PIA14098_fig5_NGC_628.tif
  - https://wise.ssl.berkeley.edu/gallery_M74.html
  - (unsecure) https://astroweb03.ipac.caltech.edu/image/ngc-628-or-messier-74-m74

- `luminosity.png`, `grayscale_2k_python.png`
  - DSS cutouts from Rubin first look image area



- eso1207a[tif, jpg] - ESO press release https://www.eso.org/public/images/eso1207a/
- `carina_cliffs_more.jpg`
  - https://science.nasa.gov/asset/hubble/ground-based-image-of-ngc-3324-in-the-carina-nebula-complex/
  
- `NGC_3324_Nebulosa_Gabriela_Mistral_en_Paleta_Hubble_(SHO).jpg`
  - https://commons.wikimedia.org/wiki/File:NGC_3324_Nebulosa_Gabriela_Mistral_en_Paleta_Hubble_(SHO).jpg
    - license: share with attribution
  
## FITS files

- `skyvrho.fits`
  - https://skyview.gsfc.nasa.gov/
  - SkyView — First Digitized Sky Survey: Blue (DSS1 Blue), STScI/CalTech/NGS
  - Rho Ophiucus

- `dssm5.fits`, `dssrho.fits`, `oriondss.fits`
  - https://archive.stsci.edu/cgi-bin/dss_form
  - Digitized Sky Survey (DSS) cutouts, UK Schmidt; ORIGIN "CASB -- STScI"

- `Orion_TAU353_full.fits`, `Orion_TAU353_reprojected.fits`
  - https://irsa.ipac.caltech.edu/Missions/planck.html
  - Planck 353 GHz dust optical depth (tau_353) map, converted to Ak; reprojected locally (Lewis & Lada 2022)

- `13CO_final.vscale.fits`
  - Processed 13CO(2-1) data cube of L1478 (California Molecular Cloud) (Lewis 2020)

## Tiled (TOAST/WWT study) data

These directories are tile pyramids. Source-file → output-directory mappings
below are taken from `tile_wwt_image.py` (each entry's `image_name` /
`avm-source` / `outdir`), except where noted.

- `hubble_ngc628/`
  - `ngc 628 Hubble Full Res (For Display).png` using AVM
  - `tile_wwt_image.py` (`hubble_has_avm`)

- `noao_ngc628/`
  - `noao-m74mortfieldw.tif` using AVM from `noao-m74mortfieldw.jpg`
  - `tile_wwt_image.py` (`noao_m74mortfieldw`)

- `potm2208a/`
  - `potm2208a.tif` using AVM from `potm2208a.jpg`
  - `tile_wwt_image.py` (`potm2208a`)

- `spitzer_ngc628/`
  - `ssc2023-01b.tif` using AVM from `spitzer_ssc2023-01b_1600.jpg`
  - `tile_wwt_image.py` (`spitzer_has_avm`)

- `weic2403c/`, `weic2403c_better/`
  - `weic2403c.tif`
  - `weic2403c/` via `tile_wwt_image.py` (`weic2403c`); `weic2403c_better/` via `weic2403c_script` (toasty, FITS WCS)

- `almagal/almagal_toast/`
  - ALMAGAL ALMA survey, galactic plane TOAST. `toasty.tile_fits` for [ALMAGAL](https://www.almagal.org/) data

- `NGC628_interpolated/`
  - Locally generated interpolation frames/video derived from the NGC 628 imagery above
