from .google import VertexAI
from ..config import config

vertex_ai = VertexAI(config.GOOGLE_API_KEY)
