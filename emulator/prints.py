from sqlalchemy import select

from db.engine import session
from db.models import Fingerprint, Device


class Fprint:

    fprint_id: int = None,
    brand_id: int = None

    def __init__(self, android_version: str = "7.1.2"):
        self.version = android_version

    def __get_sdk_by_version(self) -> int:
        convert = {"4.2": 17, "4.3": 18, "4.4": 19, "5.0": 21, "5.1": 22, "6.0": 23, "7.0": 24, "7.1": 25,
                   "8.0": 26, "8.1": 27, "9": 28, "10": 29, "11": 30, "12": 31}
        return convert[self.version[:3]]

    def get_basic_props(self, include_additional_props: bool = False) -> dict:
        query = select(Fingerprint).where(Fingerprint.product_version == self.version)
        fprint: Fingerprint = session.scalar(query)

        self.fprint_id = fprint.id
        self.brand_id = fprint.brand_id

        prints = {
            "ro.build.fingerprint": fprint.print,
            "ro.build.description": fprint.build_description,
            "ro.build.version.security_patch": fprint.security_patch,
            "ro.build.version.release": self.version,
            "ro.product.brand": fprint.product_brand,
            "ro.product.name": fprint.product_name,
            "ro.product.device": fprint.product_device,
            "ro.build.id": fprint.build_id,
            "ro.build.version.incremental": fprint.incremental
        }

        if include_additional_props:
            prints["ro.build.product"] = fprint.product_device
            prints["ro.build.display.id"] = fprint.build_description
            prints["ro.build.version.sdk"] = self.__get_sdk_by_version()

        return prints

    def get_simulation_props(self) -> dict:
        query = select(Device).where(Device.id == self.brand_id)
        device: Device = session.scalar(query)

        prints = {
            "ro.product.manufacturer": device.manufacturer,
            "ro.product.mode": device.model,
        }

        return prints
