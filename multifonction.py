# Ce fichier va permettre de désengorger certaines parties du code

# import os
# import googleapiclient.discovery
# import youtube_search as ys
from requests import get
from yt_dlp import YoutubeDL


# Chopper l'url YouTube de la vidéo -- ***YOUTUBE API V3***
# def get_youtube_url_api(mot_clé: str):
#     # Disable OAuthlib's HTTPS verification when running locally.
#     # *DO NOT* leave this option enabled in production.
#     os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

#     api_service_name = "youtube"
#     api_version = "v3"
#     DEVELOPER_KEY = "AIzaSyCzAWiVDlmS-cgjISUP1s3e7z8rKW3ywPU"

#     youtube = googleapiclient.discovery.build(
#         api_service_name, api_version, developerKey=DEVELOPER_KEY
#     )

#     request = youtube.search().list(
#         part="snippet", maxResults=6, q=mot_clé, type="video"
#     )
#     response = request.execute()

#     dictionnaire_intéressant = {}
#     didier = 1
#     for didier in range(1, 6): # à revoir quand même
#         dictionnaire_intermédiaire = {
#             "titre": response["items"][didier]["snippet"]["title"],
#             "lien": response["items"][didier]["id"]["videoId"],
#             "auteur": response["items"][didier]["snippet"]["channelTitle"],
#         }
#         dictionnaire_intéressant[str(didier)] = dictionnaire_intermédiaire
#     return dictionnaire_intéressant


# # Chopper l'url YouTube de la vidéo -- ***MODULE***
# def get_youtube_url_module(mot_clé: str):
#     results = ys.YoutubeSearch(mot_clé, max_results=5).to_dict()
#     print(results)
#     dictionnaire_intéressant = {}
#     for didier in range(len(results)):
#         dictionnaire_intermédiaire = {
#             "titre": results[didier]["title"],
#             "lien": results[didier]["id"],
#             "auteur": results[didier]["channel"],
#         }
#         dictionnaire_intéressant[str(didier)] = dictionnaire_intermédiaire
#     return dictionnaire_intéressant

# # Choper les infos sur la vidéo avec l'URL
# def get_info_on_video(lien: str):
#     with yt_dlp.YoutubeDL() as ydl:
#       info_dict = ydl.extract_info(lien, download=False)
#     #   video_id = info_dict.get("id", None)
#     #   video_title = info_dict.get('title', None)
#     #   print(info_dict)
#       dictionnaire_intéressant = {
#             "titre": info_dict["title"],
#             "lien": info_dict["id"],
#             "url": info_dict["formats"][3]["url"],
#             "auteur": info_dict["channel"],
#         }
#       return dictionnaire_intéressant

# # def lddj(mot_clé: str):
# #     with yt_dlp.yt
# # print(get_info_on_video("https://www.youtube.com/watch?v=Uly8X8mfdGE"))
# # get_youtube_url_module("didier")

# Récupérer le lien de la vidéo
def get_link(lien: str):
    ydl_opts = {
        "quiet": True,
        "format": "m4a/bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "m4a",
            }
        ],
    }

    with YoutubeDL(ydl_opts) as ydl:
        dictionnaire_complet = ydl.extract_info(lien, download=False)
    return dictionnaire_complet


# Récupérer full infos avec un mot clé
def search(mot_clé: str):
    YDL_OPTIONS = {"format": "bestaudio", "noplaylist": "True"}
    with YoutubeDL(YDL_OPTIONS) as ydl:
        try:
            get(mot_clé)
        except:
            dictionnaire_complet = ydl.extract_info(
                f"ytsearch5:{mot_clé}", download=False
            )["entries"][0:5]
        else:
            dictionnaire_complet = ydl.extract_info(mot_clé, download=False)
    return dictionnaire_complet
