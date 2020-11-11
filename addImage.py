import os
import boto3

from dotenv import load_dotenv

load_dotenv(verbose=True)

# RUN CODE THÌ BỎ DẤU @ Ở CUỐI 2 KEY

AWS_ACCESS_KEY_ID = ''
AWS_ACCESS_KEY_SECRET = ''
BUCKET = 'web-final'
COLLECTION_ID = 'web_finalterm'

def aws_session(region_name='ap-southeast-1'):
    return boto3.session.Session(
                                 aws_secret_access_key=os.getenv('AWS_ACCESS_KEY_SECRET'),
                                 region_name=region_name)


session = aws_session()
s3_resource = session.resource('s3')


def upload_file_to_bucket(bucket_name, file_path):
    session = aws_session()
    s3_resource = session.resource('s3')
    file_dir, file_name = os.path.split(file_path)

    bucket = s3_resource.Bucket(bucket_name)
    bucket.meta.client.upload_file(
        file_path, bucket_name, file_name
    )

    s3_url = f"https://{bucket_name}.s3.amazonaws.com/{file_name}"
    return s3_url

def add_faces_to_collection(bucket, photo, collection_id):
    client = boto3.client('rekognition')

    response = client.index_faces(CollectionId=collection_id,
                                  Image={'S3Object': {'Bucket': bucket, 'Name': photo}},
                                  ExternalImageId=photo,
                                  MaxFaces=1,
                                  QualityFilter="AUTO",
                                  DetectionAttributes=['ALL'])

    print('Results for ' + photo)
    print('Faces indexed:')
    for faceRecord in response['FaceRecords']:
        print('  Face ID: ' + faceRecord['Face']['FaceId'])
        print('  Location: {}'.format(faceRecord['Face']['BoundingBox']))

    print('Faces not indexed:')
    for unindexedFace in response['UnindexedFaces']:
        print(' Location: {}'.format(unindexedFace['FaceDetail']['BoundingBox']))
        print(' Reasons:')
        for reason in unindexedFace['Reasons']:
            print('   ' + reason)
    return len(response['FaceRecords'])


def main():
    for i in range(1, 6):
        file_name = 'trump_' + str(i) + '.jpeg'
        s3_url = upload_file_to_bucket('web-final', file_name)
        print("Sucessful")
        myCmd = 'aws s3api put-object-acl --bucket ' + BUCKET + ' --key ' + file_name + ' --acl public-read'
        os.system(myCmd)
        print(s3_url)
        indexed_faces_count = add_faces_to_collection(BUCKET, file_name, COLLECTION_ID)
        print("Faces indexed count: " + str(indexed_faces_count))


if __name__ == '__main__':
    main()