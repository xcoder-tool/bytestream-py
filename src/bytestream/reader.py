import struct
from io import BytesIO
from typing import Literal


class BinaryReader:
    def __init__(self, initial_buffer: bytes, endian: Literal["little", "big"]) -> None:
        self._internal_reader: BytesIO = BytesIO(initial_buffer)

        self.endian: Literal["little", "big"] = endian
        self._endian_sign: Literal["<", ">"] = "<" if endian == "little" else ">"

    def seek(self, position: int) -> None:
        _ = self._internal_reader.seek(position)

    def tell(self) -> int:
        return self._internal_reader.tell()

    def read(self, size: int) -> bytes:
        return self._internal_reader.read(size)

    def read_bool(self) -> bool:
        return self.read_uchar() == 1

    def read_char(self) -> int:
        return struct.unpack_from("b", self.read(1))[0]

    def read_uchar(self) -> int:
        return struct.unpack("B", self.read(1))[0]

    def read_short(self) -> int:
        return struct.unpack(f"{self._endian_sign}h", self.read(2))[0]

    def read_ushort(self) -> int:
        return struct.unpack(f"{self._endian_sign}H", self.read(2))[0]

    def read_int(self) -> int:
        return struct.unpack(f"{self._endian_sign}i", self.read(4))[0]

    def read_uint(self) -> int:
        return struct.unpack(f"{self._endian_sign}I", self.read(4))[0]

    def read_twip(self) -> float:
        return self.read_int() / 20

    def read_ascii(self) -> str | None:
        length = self.read_uchar()
        if length == 0xFF:
            return None

        return self.read(length).decode()
