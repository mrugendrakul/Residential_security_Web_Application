from PythonFiles.initFirebase import delivery_collection
import firebase_admin
from firebase_admin import credentials, storage
from firebase_admin import firestore
import os
import datetime
import pytz
from pytz import timezone

bucket = storage.bucket()

def apiDelivery(
        imagePath
):
    now_utc = datetime.datetime.now(tz=datetime.timezone.utc)
    now_ist = now_utc.astimezone(timezone('Asia/Kolkata'))
    current_time = now_ist.timestamp()

    destination_blob_name = 'DeliveryPeople/'+str(now_ist)

    blob  = bucket.blob(destination_blob_name)
    blob.upload_from_filename(imagePath)

    print(f"Unknown {imagePath} uploaded to {destination_blob_name}")

    download_url = blob.generate_signed_url(expiration=253402300799) # URL won't expire

    now_utc = datetime.datetime.now(tz=datetime.timezone.utc)
    now_ist = now_utc.astimezone(timezone('Asia/Kolkata'))
    current_time = now_ist.timestamp()
    print('Download URL:', download_url)
    #Create document for uploading
    document = {
        "imageLink" : str(download_url),
        "timeStamp" : now_ist
    }

    # unknownPeople_collection.document(now_ist).set(document)
    try:
        delivery_collection.document(str(now_ist)).set(document)
        print("Delivery person added to collection")
        # print('Document added with id : '+f"{doc_ref[1].id}")
    except Exception as e:
        print('Unable to add delivery person with unique id : '+f"{e}")

if __name__ == "__main__":
    apiDelivery(
        imagePath="PythonFiles/frame.jpg"
    )