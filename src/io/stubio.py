import pickle, os

class StubIO:

    def write(self, src:str, data:any):
        if not src: return
        with open(src, 'wb') as f: pickle.dump(data, f)
        return f'Dumped to {src}'
    
    def read(self, src:str):
        if not os.path.exists(str(src)): return
        with open(src, 'rb') as f: data =pickle.load(f)
        return data