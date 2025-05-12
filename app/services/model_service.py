import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.metrics import CosineSimilarity
from app.database.connection import execute_query

class ModelService:
    def __init__(self):
        self.model = None
        self.config = None
        self.load_config_and_model()

    def load_config_and_model(self, model_id=1):
        query = """
            SELECT model_file, embedding_dir, threshold, target_shape
            FROM models
            WHERE id = %s
        """
        config = execute_query(query, (model_id,), fetch_one=True)
        if not config:
            raise Exception("Model not found in database")

        target_shape_str = config['target_shape'].strip("()").replace(" ", "")
        try:
            target_shape = tuple(int(x) for x in target_shape_str.split(","))
        except ValueError as e:
            raise Exception(f"Invalid target_shape format: {str(e)}")

        self.config = {
            "model_file": config['model_file'],
            "embedding_dir": config['embedding_dir'],
            "threshold": config['threshold'],
            "target_shape": target_shape,
            "video_dir": "Family/Family_video2"
        }
        self.model = load_model(self.config['model_file'])

    def extract_embedding(self, video_landmarks):
        video_landmarks = np.array(video_landmarks)
        target_shape = self.config['target_shape']
        
        if video_landmarks.shape[0] < target_shape[0]:
            padding = target_shape[0] - video_landmarks.shape[0]
            video_landmarks = np.pad(video_landmarks, ((0, padding), (0, 0), (0, 0)), mode='constant')
        else:
            video_landmarks = video_landmarks[:target_shape[0], :, :]
            
        video_landmarks = np.reshape(video_landmarks, (1, *target_shape))
        return self.model.predict(video_landmarks)

    def calculate_similarity(self, embedding1, embedding2):
        cosine_similarity = CosineSimilarity()
        return cosine_similarity(embedding1, embedding2).numpy()

    def get_similarity_status(self, similarity):
        return "Match!" if similarity > self.config['threshold'] else "Keep Practicing" 