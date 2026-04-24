from urllib.parse import urlparse, parse_qs, unquote, urlunparse
from urllib import request
from io import BytesIO
from astropy.io import fits
from astropy.wcs import WCS
from astropy.io.fits.header import Header
from wwt_data_formats.imageset import ImageSet
from wwt_data_formats.enums import ProjectionType
import os
from bs4 import BeautifulSoup


# http://www.worldwidetelescope.org/wwtweb/ShowImage.aspx?ra=24.17437150224632&dec=15.780613507831623&x=640.0&y=400.7170294494238&scale=0.06305105117&rotation=250.5199999999998&name=NGC+628&imageurl=http://esawebb.org/media/archives/images/screen/weic2403c.jpg&thumb=http://esawebb.org/media/archives/images/thumbs/weic2403c.jpg&credits=&creditsUrl=http://esawebb.org/images/weic2403c/
def wwt_url_to_fits_header(wwt_url, scale_factor=1.0, height = None):
    url = urlparse(wwt_url)
    query_params = parse_qs(url.query)
    
    # wcs = WCS(naxis=2)
    # wcs.wcs.crval = [float(query_params['ra'][0]), float(query_params['dec'][0])]
    # wwt_scale = float(query_params['scale'][0]) # arcseconds per pixel
    # scale_deg = wwt_scale / 3600.0 * scale_factor # degrees per pixel
    
    # # https://wwt-data-formats.readthedocs.io/en/latest/_modules/wwt_data_formats/imageset.html#ImageSet.set_position_from_wcs
    #     # In FITS/WCS, pixel coordinates are 1-based and integer pixel
    #     # coordinates land on pixel centers. Therefore in standard FITS
    #     # orientation, where the "first" pixel is at the lower-left, the
    #     # lower-left corner of the image has pixel coordinate (0.5, 0.5). For
    #     # the WWT offset parameters, the lower-left corner of the image has
    #     # coordinate (0, 0).
    # wcs.wcs.crpix = [
    #     float(query_params['x'][0]) * scale_factor + 0.5,
    #     float(query_params['y'][0]) * scale_factor + 0.5
    #     ]
    # wcs.wcs.cdelt = [float(query_params['scale'][0]), float(query_params['scale'][0])]
    # wcs.wcs.crota = [float(query_params['rotation'][0]), 0.0]
    # wcs.wcs.ctype = ['RA---TAN', 'DEC--TAN']
    
    imageset = ImageSet()
    imageset.center_x = float(query_params['ra'][0])
    imageset.center_y = float(query_params['dec'][0])
    wwt_scale = float(query_params['scale'][0]) # arcseconds per pixel
    scale_deg = wwt_scale / 3600.0 / scale_factor # degrees per pixel
    
    imageset.base_degrees_per_tile = scale_deg # for an image it is just the degrees per pixel
    imageset.rotation_deg = float(query_params['rotation'][0]) - 180
    imageset.base_tile_level = 0 # for an image it is just one tile
    # Match AVM/toasty's tiled-study pixel convention: the URL pixel coordinates
    # describe image pixel centers, while WWT ImageSet offsets describe corners.
    imageset.offset_x = float(query_params['x'][0]) * scale_factor - 0.5
    imageset.offset_y = float(query_params['y'][0]) * scale_factor - 0.5
    imageset.projection = ProjectionType.SKY_IMAGE
    
    wcs_headers_as_dict = imageset.wcs_headers_from_position(height=height)

    header = Header(wcs_headers_as_dict)
    for key, value in wcs_headers_as_dict.items():
        header[key] = value
    return header


from PIL import Image

def source_image_size_from_url(wwt_url):
    url = urlparse(wwt_url)
    query_params = parse_qs(url.query)
    image_url = unquote(query_params['imageurl'][0])
    parts = urlparse(image_url)
    if parts.scheme == 'http':
        image_url = urlunparse(('https', parts.netloc, parts.path, parts.params, parts.query, parts.fragment))

    req = request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
    with request.urlopen(req, timeout=20) as response:
        image = Image.open(BytesIO(response.read()))
        return image.size
    

def write_header_for_image(wwt_url, image_path):
    out = os.path.splitext(image_path)[0] + '.wcs'
    
    output_size = Image.open(image_path).size
    source_size = source_image_size_from_url(wwt_url)
    scale_x = output_size[0] / source_size[0]
    scale_y = output_size[1] / source_size[1]
    print(f"input size: {source_size[0]}x{source_size[1]}")
    print(f"output size: {output_size[0]}x{output_size[1]}")
    print(f"scale_x: {scale_x}")
    print(f"scale_y: {scale_y}")
    print(f"using scale_x: {scale_x}")

    header = wwt_url_to_fits_header(wwt_url, scale_factor=scale_x, height=output_size[1])
    hdu = fits.PrimaryHDU(data=None, header=header)
    hdu.writeto(out, overwrite=True)
    
    
def get_wwt_url(esa_page = "https://esawebb.org/images/weic2403c/"):
    # get the <a> tag that as a "worldwidetelescope*ShowImage" link
    req = request.Request(esa_page, headers={'User-Agent': 'Mozilla/5.0'})
    with request.urlopen(req, timeout=20) as response:
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
        a_tags = soup.find_all('a', href=True)
        for a in a_tags:
            if 'worldwidetelescope' in a['href'] and 'ShowImage' in a['href']:
                return a['href']
    return None
    
    
    
    

import argparse
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert WWT URL to FITS header')
    parser.add_argument('wwt_url', type=str, help='WWT URL to convert')
    parser.add_argument('image_path', type=str, help='Path to the image file (used to determine height)')
    #optional scale factor
    # parser.add_argument('--scale', type=float, default=1.0, help='Scale factor to apply to the WWT scale (default: 1.0)')
    
    args = parser.parse_args()
    
    write_header_for_image(args.wwt_url, args.image_path)
