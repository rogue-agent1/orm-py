class Field:
    def __init__(s, ftype=str, required=True, default=None):
        s.ftype=ftype;s.required=required;s.default=default
class Model:
    _tables = {}
    def __init_subclass__(cls, **kw):
        super().__init_subclass__(**kw)
        cls._fields = {k:v for k,v in cls.__dict__.items() if isinstance(v, Field)}
        cls._rows = []; cls._next_id = 1; Model._tables[cls.__name__] = cls
    def __init__(s, **kw):
        s.id = s.__class__._next_id; s.__class__._next_id += 1
        for name, field in s._fields.items():
            val = kw.get(name, field.default)
            if field.required and val is None: raise ValueError(f"{name} required")
            setattr(s, name, field.ftype(val) if val is not None else None)
        s.__class__._rows.append(s)
    def __repr__(s):
        fields = ", ".join(f"{k}={getattr(s,k)!r}" for k in s._fields)
        return f"{s.__class__.__name__}(id={s.id}, {fields})"
    @classmethod
    def all(cls): return list(cls._rows)
    @classmethod
    def find(cls, id): return next((r for r in cls._rows if r.id == id), None)
    @classmethod
    def where(cls, **kw): return [r for r in cls._rows if all(getattr(r,k)==v for k,v in kw.items())]
    @classmethod
    def count(cls): return len(cls._rows)
    def delete(s): s.__class__._rows.remove(s)
class User(Model):
    name = Field(str)
    email = Field(str)
    age = Field(int, default=0)
def demo():
    User(name="Alice", email="alice@test.com", age=30)
    User(name="Bob", email="bob@test.com", age=25)
    User(name="Charlie", email="charlie@test.com", age=30)
    print(f"All users: {User.count()}")
    print(f"Find #2: {User.find(2)}")
    print(f"Age 30: {User.where(age=30)}")
    User.find(1).delete()
    print(f"After delete: {User.count()}")
if __name__ == "__main__": demo()
