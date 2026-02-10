d = {}
d["a"] = 1
d["b"] = 2
print(d["a"])   
print("----")        # 1
print(d.get("c", -1))   # -1 (default if missing)
print("a" in d)         # True
del d["b"]
for k, v in d.items():
    print(k, v)