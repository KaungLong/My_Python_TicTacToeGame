
from unicodedata import name
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import threading
import time
# 引用私密金鑰
# path/to/serviceAccount.json 請用自己存放的路徑
cred = credentials.Certificate('ggdog-72aa5-firebase-adminsdk-uatst-9f83c733a5.json')
# 初始化firebase，注意不能重複初始化
firebase_admin.initialize_app(cred)
#db = firestore.client()
db = firestore.client()

def quickstart_add_data_one(col,doc,column,pl_n):
    # [START firestore_setup_dataset_pt1]
    doc_ref = db.collection(col).document(doc)
    doc_ref.set({
        column:pl_n 
    })
    # [END firestore_setup_dataset_pt1]
def quickstart_uppade(col,doc,column,pl_n):
    document = db.collection(col).document(doc)
    document.update({
        column:pl_n 
    })
def quickstart_get_collection(col,id,column):

    # [START firestore_setup_dataset_read]
    # [START quickstart_get_collection]
    users_ref = db.collection(col)
    docs = users_ref.stream()

    for doc in docs:
        if doc.id == id :
            return doc.to_dict()[column]
print(quickstart_get_collection("game","room1","whos_turn"))
print("T")

#quickstart_uppade()
#print(quickstart_get_collection('player_online',"player1","name"))
#quickstart_get_collection('player_online',"player1","name")
#quickstart_add_data_one('player_online','player','qqcat')