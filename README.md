[Cloud Firestore](https://firebase.google.com/docs/firestore) is a flexible, scalable NoSQL cloud database, originally developed by [Firebase](https://en.wikipedia.org/wiki/Firebase) but has been acquired by Google and evolved into its flagship offering to compete against AWS DynamoDB and Azure Cosmos DB.

Due to this history, I find Cloud Firestore's official documentations to be scattered across multiple Firebase/Google websites, and not always available in my favorite Python language:
- [Firebase - Cloud Firestore Documentation](https://firebase.google.com/docs/firestore)
- [Google Cloud - How-to guides](https://cloud.google.com/firestore/docs/how-to)
- [GoogleAPIs.dev - Python Client for Google Cloud Firestore](https://googleapis.dev/python/firestore/latest/)

To help myself and other Pythoneers, I have tested  these common database operations and summarized into this table:

Operation | Subtype | On Collections | On Documents
:--- | :--- | :--- | :--- |
Referencing | One-level | `coll_ref = db.collection('coll_id')` | `doc_ref = db.collection('coll_id').document('doc_id')`<br>`doc_ref = db.document('coll_id/doc_id')`

```python
doc_ref = db.collection('coll_id').document('doc_id')
doc_ref = db.document('coll_id/doc_id')
doc_ref = db.document('coll_id', 'doc_id')
```

<table>
  <tr>
    <th>
      Code Block
    </th>
  </tr>
  <tr> 
    <td>
      <pre lang="python">
        doc_ref = db.collection('coll_id').document('doc_id')
        doc_ref = db.document('coll_id/doc_id')
        doc_ref = db.document('coll_id', 'doc_id')
      </pre>
    </td>
  </tr>
</table>
