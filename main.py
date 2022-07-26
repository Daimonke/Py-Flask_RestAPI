import resource
from flask import Flask
from flask_restful import Resource, Api, reqparse
import json

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument("title", type=str, required=True, help="No title provided")


def all_videos():
    with open("videos.json", "r") as file:
        videos = json.load(file)
    return videos


def write_to_file(data):
    videos = all_videos()
    videos.append(data)

    with open("videos.json", "w") as file:
        json.dump(videos, file)


class Video(Resource):
    def get(self, video_id):
        for video in all_videos():
            if video["id"] == int(video_id):
                return video, 200
        return {"message": "Video not found"}, 404

    def put(self, video_id):
        args = parser.parse_args()
        title = args["title"]

        for video in all_videos():
            if video["id"] == int(video_id):
                video["title"] = title
                return video, 200
        return {"message": "Video not found"}, 404

    def delete(self, video_id):
        for video in all_videos():
            if video["id"] == int(video_id):
                videos = all_videos()
                videos.remove(video)
                with open("videos.json", "w") as file:
                    json.dump(videos, file)
                return {"message": "Video deleted"}, 200
        return {"message": "Video not found"}, 404


class VideoList(Resource):
    def get(self):
        return all_videos(), 200

    def post(self):
        args = parser.parse_args()
        title = args["title"]

        video = {
            "id": all_videos()[len(all_videos()) - 1]["id"] + 1,
            "title": title,
            "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        }
        write_to_file(video)
        return video, 201


api.add_resource(Video, "/videos/<video_id>/")
api.add_resource(VideoList, "/videos/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
