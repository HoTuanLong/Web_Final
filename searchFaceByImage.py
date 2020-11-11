from io import BytesIO
import boto3
import requests
from PIL import Image


BUCKET = 'web-final'
KEY = 'trump_4.jpeg'
COLLECTION = 'web_finalterm'
maxFaces = 5


def search_faces_by_image(bucket, key, collection_id, threshold=80, region="ap-southeast-1"):
    rekognition = boto3.client("rekognition", region)
    response = rekognition.search_faces_by_image(
        Image={
            "S3Object": {
                "Bucket": bucket,
                "Name": key,
            }
        },
        CollectionId=collection_id,
        FaceMatchThreshold=threshold,
        MaxFaces=maxFaces
    )
    return response['FaceMatches']


if __name__ == '__main__':
    for record in search_faces_by_image(BUCKET, KEY, COLLECTION):
        face = record['Face']
        print("Matched Face ({}%)".format(record['Similarity']))
        print("  FaceId : {}".format(face['FaceId']))
        print(face['ExternalImageId'])
        url = 'https://s3-ap-southeast-1.amazonaws.com/web-final/' + format(face['ExternalImageId'])
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        img.show(face['ExternalImageId'])

