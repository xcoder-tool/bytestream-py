import struct
from collections.abc import Buffer
from io import BytesIO
from typing import Literal


class BinaryWriter:
    def __init__(self, endian: Literal["little", "big"]) -> None:
        self._internal_writer: BytesIO = BytesIO()

        self._endian: Literal["little", "big"] = endian
        self._endian_sign: Literal["<", ">"] = "<" if endian == "little" else ">"

    @property
    def buffer(self) -> bytes:
        return self._internal_writer.getvalue()

    def write(self, value: Buffer) -> None:
        _ = self._internal_writer.write(value)

    def fill(self, size: int) -> None:
        self.write(b"\x00" * size)

    def write_bool(self, value: bool) -> None:
        self.write(int(value).to_bytes(1, self._endian))

    def write_char(self, value: int) -> None:
        self.write(struct.pack("b", value))

    def write_uchar(self, value: int) -> None:
        self.write(struct.pack("B", value))

    def write_short(self, value: int) -> None:
        self.write(struct.pack(f"{self._endian_sign}h", value))

    def write_ushort(self, value: int) -> None:
        self.write(struct.pack(f"{self._endian_sign}H", value))

    def write_int(self, value: int) -> None:
        self.write(struct.pack(f"{self._endian_sign}i", value))

    def write_uint(self, value: int) -> None:
        self.write(struct.pack(f"{self._endian_sign}I", value))

    def write_ascii(self, value: str | None) -> None:
        if not value:
            self.write_uchar(0xFF)
        else:
            self.write_uchar(len(value))
            self.write(value.encode("ascii"))

    def write_twip(self, value: float) -> None:
        self.write_int(int(round(value * 20)))
