import pymongo

URL = "mongodb+srv://vargur:inrustwetrust@cluster0.g0cm2.mongodb.net/incursions?retryWrites=true&w=majority"

mongoClient = pymongo.MongoClient(URL)
db = mongoClient['incursions']
coll=db['focus_data']
doc=coll.find_one()
print(doc)
doc['focusUp'] = not doc['focusUp']
coll.update_one({'_id': 'data'},{"$set":doc})

# ODk5NjI2NDk1MzI3MjE5NzUy.YW1gdg.Mgv4-212h_2o7mB-ln3bkqCDbVg
# ODkzODU4NTE1MzgxMjY4NTQw.YVhknQ.mu0lf7HKkwRT8RWi_jfbgF-7ZC8