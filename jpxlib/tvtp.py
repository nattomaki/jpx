import csv
import re
import os
from jpxlib.utils import date2iso
from jpxlib.rowutils import Range, RowData, RowDataHandler
from jpxlib.exceptions import InvalidTradeData
from datetime import datetime
from logging import getLogger

logger = getLogger(__name__)


class TradingVolumeByParticipant:
    """
    マーケット情報 > 先物・オプション関連 > 取引参加者別取引高（手口上位一覧）
    https://www.jpx.co.jp/markets/derivatives/participant-volume/index.html
    """

    re_date = re.compile(r"(?P<date>\d{8})")
    re_inst = re.compile(r"(?P<product_class>^[^_]+_[^_]+)_(?P<contract_month>\d{4,6})_?(?P<price>\d+)?")

    def __init__(self, csv_file, row_handlers=None):
        self._file = csv_file
        if row_handlers is None:
            self._handlers = self._get_default_handlers()
        else:
            self._handlers = row_handlers

    def _do_parse(self):
        with open(self._file, encoding="utf-8") as f:
            reader = csv.reader(f)
            _ = next(reader)
            m = self.re_date.search("".join(next(reader)))
            if m:
                trade_date = date2iso(m.group("date"))
            else:
                raise ValueError("Cannot find the trade-date")
            fname = os.path.basename(self._file)
            meta = dict(data_source=fname, trade_date=trade_date, **self._get_session_info(fname))

            for row in reader:
                if self._is_ignore_row(row):
                    continue
                if row[0].startswith("Instrument"):
                    product_info = self._get_instrument(row[1])
                    continue
                for handler in self._handlers:
                    try:
                        x = handler(row)
                        x.update(**meta, **product_info)
                        yield x
                    except Exception as err:
                        yield err

    def _is_ignore_row(self, row):
        if not row:
            return True
        if row[0].startswith("JPX"):
            return True
        return False

    def _get_instrument(self, value):
        if self.re_inst.match(value):
            info = self.re_inst.search(value).groupdict()
            if info["price"] is None:
                del info["price"]
            info["contract_month"] = date2iso(info["contract_month"])
            return info
        raise ValueError("must match the instrument pattern : %s" % value)

    def _get_session_info(self, filename):
        x = {}
        if "whole" in filename:
            x["session"] = "whole"
        elif "night" in filename:
            x["session"] = "night"
        if "J-NET" in filename:
            x["market"] = "j-net"
        elif filename.endswith(".csv"):
            x["market"] = "floor"
        return x

    def _get_default_handlers(self):
        def chk(values):
            if any(x in ["-", ""] for x in values):
                raise InvalidTradeData(values)

        def set_sell_vol(x):
            x["vol"] = int(x["volume"]) * -1
            return x

        def set_buy_vol(x):
            x["vol"] = int(x["volume"])
            return x

        f = ["participant_code", "participant_name", "participant_name_en", "volume"]
        x = RowDataHandler()
        x.add(x=Range([4, 8], fields=f, validator=chk), trade_type="buy", cb=set_buy_vol)
        x.add(x=Range([0, 4], fields=f, validator=chk), trade_type="sell", cb=set_sell_vol)
        return x

    def __iter__(self):
        return self._do_parse()
