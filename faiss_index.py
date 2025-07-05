import faiss, numpy as np
from sqlalchemy.orm import Session
from models import Person

class FaissIndex:
    def __init__(self, dim: int = 512):
        self.dim = dim
        self.index = faiss.IndexFlatL2(dim)
        self.id_map = {}

    def reset(self):
        self.index = faiss.IndexFlatL2(self.dim)
        self.id_map = {}

    def add(self, person_id: int, vector: np.ndarray):
        idx = self.index.ntotal
        self.index.add(np.expand_dims(vector, axis=0))
        self.id_map[idx] = person_id

    def search(self, vector: np.ndarray, k: int = 5):
        D, I = self.index.search(np.expand_dims(vector, axis=0), k)
        results = []
        for dist, idx in zip(D[0], I[0]):
            if idx == -1:
                continue
            results.append((self.id_map[idx], float(dist)))
        return results

    def rebuild_from_db(self, db: Session):
        self.reset()
        people = db.query(Person).all()
        for p in people:
            self.add(p.id, np.array(p.embedding, dtype=np.float32))
