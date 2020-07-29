class Index(int):
    pass


class Range(list):
    def __init__(self, *values, fields=None, validator=None):
        super().__init__(*values)
        self.fields = fields
        self.validator = validator


class RowData(dict):
    def __call__(self, values):
        x = {}
        for k, v in self.items():
            if isinstance(v, Index):
                x[k] = values[v]
            elif isinstance(v, Range):
                y = values[v[0] : v[1]]
                if v.validator is not None:
                    v.validator(y)
                if v.fields is not None:
                    x.update(dict(zip(v.fields, y)))
                else:
                    x[k] = y
            elif isinstance(v, str):
                x[k] = v
        if callable(self.get("cb")):
            x = self["cb"](x)
        return x


class RowDataHandler(list):
    def add(self, **kwargs):
        self.append(RowData(**kwargs))
