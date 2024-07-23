from sklearn.cluster import KMeans
from src.types import Frame, Color

class Clustering:

    def __init__(self, n_clusters:int =2):
        self.model =KMeans(n_clusters=n_clusters, init='k-means++', n_init=1, random_state=0)
    
    def get_subject_color(self, img:Frame, channels =3):
        im =img.reshape(-1, channels)
        model =self.model
        model.fit(im)
        labels =model.labels_
        clusters =labels.reshape(img.shape[:2])
        corner_pts =[clusters[0, 0], clusters[0, -1], clusters[-1, 0], clusters[-1, -1]]
        background:int =max(set(corner_pts), key=corner_pts.count)
        subject =1 -background
        return Color(*model.cluster_centers_[subject].astype(int).tolist()[::-1])
    
    def cluster_colors(self, colors:list[tuple]):
        model =self.model
        model.fit(colors)
        return model.cluster_centers_, model