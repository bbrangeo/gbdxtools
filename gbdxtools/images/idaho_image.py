from gbdxtools.images.base import RDABaseImage
from gbdxtools.images.drivers import IdahoDriver
from gbdxtools.images.util import vector_services_query
from gbdxtools.ipe.util import calc_toa_gain_offset, ortho_params
from gbdxtools.ipe.interface import Ipe

from shapely import wkt
from shapely.geometry import box

ipe = Ipe()

class IdahoImage(RDABaseImage):
    """
      Dask based access to IDAHO images via IPE.
    """
    __Driver__ = IdahoDriver

    @property
    def idaho_id(self):
        return self.__rda_id__

    @classmethod
    def _build_graph(cls, idaho_id, proj=None, bucket="idaho-images", gsd=None, acomp=False, bands="MS", **kwargs):
        if bucket is None:
            vq = "item_type:IDAHOImage AND id:{}".format(idaho_id)
            result = vector_services_query(vq)
            if result:
               bucket = result[0]["properties"]["attributes"]["tileBucketName"]

        gsd = gsd if gsd is not None else ""
        correction = "ACOMP" if acomp else kwargs.get("correctionType")
        spec = kwargs.get('spec')
        if spec == "1b":
            graph = ipe.IdahoRead(bucketName=bucket, imageId=idaho_id, objectStore="S3", targetGSD=gsd)
        else:
            graph = ipe.DigitalGlobeImage(bucketName=bucket, imageId=idaho_id, bands=bands, CRS=proj, correctionType=correction, GSD=gsd)

        return graph

