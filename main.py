from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/videos.db'
db = SQLAlchemy(app)


class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    # Represention of a class's objects as a string
    def __repr__(self):
        return f'Video(name={name}, views={views}, likes={likes})'

# # Creating Database
# db.create_all()


# Video create arguments
video_put_args = reqparse.RequestParser()
video_put_args.add_argument(
    "name", type=str, help="Name of the video is required", required=True)
video_put_args.add_argument(
    "views", type=int, help="Views of the video is required", required=True)
video_put_args.add_argument(
    "likes", type=int, help="Likes on the video is required", required=True)

# Video update arguments
video_update_args = reqparse.RequestParser()
video_update_args.add_argument(
    "name", type=str, help="Name of the video")
video_update_args.add_argument(
    "views", type=int, help="Views of the video")
video_update_args.add_argument(
    "likes", type=int, help="Likes on the video")


resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer
}


class Video(Resource):
    # Read all
    @marshal_with(resource_fields)
    def get(self):
        result = VideoModel.query.all()
        if not result:
            abort(404, message="Video ID is not valid...")
        return result

    # Read one
    @marshal_with(resource_fields)
    def get(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Video ID is not valid...")
        return result

    # Create
    @marshal_with(resource_fields)
    def put(self, video_id):
        args = video_put_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409, message="Video is already exists...")

        video = VideoModel(
            id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
        db.session.add(video)
        db.session.commit()
        return video, 201    # return created (201) status code

    # Update
    @marshal_with(resource_fields)
    def patch(self, video_id):
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Video is not exists, cannot update...")

        if args['name']:
            result.name = args['name']
        if args['views']:
            result.views = args['views']
        if args['likes']:
            result.likes = args['likes']

        db.session.commit()
        return result

    # Delete
    @marshal_with(resource_fields)
    def delete(self, video_id):
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Video is not exists, cannot delete...")
        db.session.delete(result)
        db.session.commit()


api.add_resource(Video, "/video/<int:video_id>")


if __name__ == "__main__":
    app.run(debug=True)  # For testing enviornment
