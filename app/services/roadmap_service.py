import re
from app.database.connection import execute_query

class RoadmapService:
    def __init__(self, model_service):
        self.model_service = model_service

    def clean_label(self, video_filename):
        raw_label_name = video_filename.split('-')[-1].split('.')[0]
        return re.sub(r'\s*\d+$', '', raw_label_name)

    def get_roadmap(self):
        # Lấy tất cả chapters thuộc model_id = 1
        chapters_query = """
            SELECT id, name
            FROM chapters
            WHERE model_id = 1
            ORDER BY id
        """
        chapters = execute_query(chapters_query)

        roadmap = {}
        for chapter in chapters:
            chapter_id = chapter['id']
            chapter_name = chapter['name']

            # Lấy tất cả videos thuộc chapter
            videos_query = """
                SELECT video_filename
                FROM videos
                WHERE model_id = 1 AND chapter_id = %s
            """
            videos = execute_query(videos_query, (chapter_id,))

            chapter_videos = []
            for video in videos:
                video_filename = video['video_filename']
                base = video_filename.split('.')[0]
                label = self.clean_label(video_filename)
                public_path = f"/{self.model_service.config['video_dir']}/{video_filename}".replace("Family/", "")
                embedding_path = f"{self.model_service.config['embedding_dir']}/{base}_embedding.npy".replace("\\", "/")
                chapter_videos.append({
                    "name": label,
                    "path": public_path,
                    "embedding": embedding_path
                })

            roadmap[chapter_name] = chapter_videos

        return roadmap 