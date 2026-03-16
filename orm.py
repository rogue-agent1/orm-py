#!/usr/bin/env python3
"""Simple ORM — object-relational mapping."""
import sys

class Field:
    def __init__(self, field_type, primary_key=False, default=None):
        self.type=field_type; self.pk=primary_key; self.default=default; self.name=None

class ModelMeta(type):
    def __new__(mcs, name, bases, attrs):
        fields={}
        for k,v in attrs.items():
            if isinstance(v,Field): v.name=k; fields[k]=v
        attrs['_fields']=fields
        return super().__new__(mcs,name,bases,attrs)

class Model(metaclass=ModelMeta):
    _store={}
    def __init__(self, **kwargs):
        for name,field in self._fields.items():
            setattr(self,name,kwargs.get(name,field.default))
    def save(self):
        cls=type(self).__name__
        if cls not in Model._store: Model._store[cls]=[]
        Model._store[cls].append(self)
    @classmethod
    def all(cls): return Model._store.get(cls.__name__,[])
    @classmethod
    def filter(cls, **kwargs):
        return [obj for obj in cls.all() if all(getattr(obj,k)==v for k,v in kwargs.items())]
    def __repr__(self):
        fields=", ".join(f"{k}={getattr(self,k)!r}" for k in self._fields)
        return f"{type(self).__name__}({fields})"

class User(Model):
    id=Field(int,primary_key=True)
    name=Field(str)
    email=Field(str)
    age=Field(int,default=0)

if __name__ == "__main__":
    for name,email,age in [("Alice","a@b.com",30),("Bob","b@b.com",25),("Charlie","c@b.com",30)]:
        User(id=hash(name)%1000,name=name,email=email,age=age).save()
    print("All users:"); 
    for u in User.all(): print(f"  {u}")
    print(f"\nAge 30: {User.filter(age=30)}")
