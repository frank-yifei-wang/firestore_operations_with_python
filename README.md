[Cloud Firestore](https://firebase.google.com/docs/firestore) is a flexible, scalable NoSQL cloud database, originally developed by [Firebase](https://en.wikipedia.org/wiki/Firebase) but has been acquired by Google and evolved into its flagship offering to compete against AWS DynamoDB and Azure Cosmos DB.

Due to this history, I find Cloud Firestore's official documentations to be scattered across multiple Firebase/Google websites, and not always available in my favorite Python language:
- [Firebase - Cloud Firestore Documentation](https://firebase.google.com/docs/firestore)
- [Google Cloud - How-to guides](https://cloud.google.com/firestore/docs/how-to)
- [GoogleAPIs.dev - Python Client for Google Cloud Firestore](https://googleapis.dev/python/firestore/latest/)

To help myself and other Pythoneers, I have tested  these common database operations and summarized into this table:

<table>
    <!-- Headers -->
    <tr>
        <th>Operation</th>
        <th>Subtype</th>
        <th>On Collections</th>
        <th>On Documents</th>
    </tr>
    <!-- Referencing 1 -->
    <tr> 
        <td rowspan="2">Referencing</td>
        <td>One-level</td>
        <td><pre lang="python">
            coll_ref = db.collection('coll_id')
        </pre></td>
        <td><pre lang="python">
            doc_ref = db.collection('coll_id').document('doc_id')
            doc_ref = db.document('coll_id/doc_id')
            doc_ref = db.document('coll_id', 'doc_id')
        </pre></td>
    </tr>
    <!-- Referencing 2 -->
    <tr>
        <td>Multi-level</td>
        <td><pre lang="python">
            sub_coll_ref = db.collection('coll_id').document('doc_id).collection('sub_coll_id')
            sub_coll_ref = db.collection('coll_id/doc_id/sub_coll_id')
            sub_coll_ref = db.collection('coll_id', 'doc_id', 'sub_coll_id')
        </pre></td>
        <td><pre lang="python">
            doc_ref = sub_coll_ref.document('sub_doc_id')
            doc_ref = db.document('coll_id/doc_id/sub_coll_id/sub_doc_id')
            doc_ref = db.document('coll_id', 'doc_id', 'sub_coll_id', 'sub_doc_id')
            doc_ref = doc_snapshot.reference
        </pre></td>
    </tr>
    <!-- Read -->
    <tr>
        <td>Read</td>
        <td>–</td>
        <td><pre lang="python">
            doc_list = coll_ref.get()
            if len(doc_list) > 0:
                docs = coll_ref.stream()    # docs is iterable
                for doc_snapshot in docs:
                    print(doc_snapshot.to_dict())
            #
            doc_list = coll_ref.get()
            if len(doc_list) > 0:
                doc_refs = coll_ref.list_documents()    # docs_refs is iterable
                for doc_ref in doc_refs:
                    print(doc_ref.get().to_dict())
        </pre></td>
        <td><pre lang="python">
            doc_snapshot = doc_ref.get()
            if doc_snapshot.exists:
                print(doc_snapshot.to_dict())
        </pre></td>
    </tr>
    <!-- Query 1 -->
    <tr>
        <td rowspan="3">Query</td>
        <td>Simple <code>where</code> (row-wise)</td>
        <td><pre lang="python">
            qry = coll_ref.select(fieldpath).where('col', '==', 'val')  # fieldpath is like ['col1', 'col2', …]
            doc_list = qry.get()
            if len(doc_list) > 0:
                docs = qry.stream()
            …
        </pre></td>
        <td>–</td>
    </tr>
    <!-- Query 2 -->
    <tr>
        <td>Compound <code>where</code></td>
        <td><pre lang="python">
            qry = coll_ref.select(fieldpath).where('col', '==', 'val').where()…  # Can only query on single key  if no indexing manually set            
        </pre></td>
        <td>–</td>
    </tr>
    <!-- Query 3 -->
    <tr>
        <td>Order & limit</td>
        <td><pre lang="python">
            qry = coll_ref.where('col', '==', 'val')
            .order_by('col', direction=firestore.Query.ASCENDING|DESCENDING)
            .start_at|end_at|start_after|end_before(cursor)
            .offset(num_to_skip)
            .limit|limit_to_last(count)            
        </pre></td>
        <td>–</td>
    </tr>
    <!-- Create -->
    <tr>
        <td>Create</td>
        <td></td>
        <td><pre lang="python">
            # collection automatically created once a document is created in it
            coll_ref.add(data_dict, document_id=None)  # Add with auto/given doc id            
        </pre></td>
        <td><pre lang="python">
            doc_ref = coll_ref.document('doc_id')
            doc_ref.create(data_dict)  # Create given doc id. Will fail if existing
        </pre></td>
    </tr>
    <!-- Update -->
    <tr>
        <td>Update</td>
        <td></td>
        <td><pre lang="python">
            # collection automatically created once a document is created in it
            coll_ref.add(data_dict, document_id=None)  # Add with auto/given doc id
        </pre></td>
        <td><pre lang="python">
            doc_ref = coll_ref.document('doc_id')
            doc_ref.create(data_dict)  # Create given doc id. Will fail if existing            
        </pre></td>
    </tr>
    <!-- Delete -->
    <tr>
        <td>Delete</td>
        <td></td>
        <td><pre lang="python">
            # collection automatically deleted once all documents in it are deleted            
        </pre></td>
        <td><pre lang="python">
            doc_ref.update({'field_to_delete': firestore.DELETE_FIELD})  # Delete a field
            doc_ref.delete()  # Delete the whole document            
        </pre></td>
    </tr>
    <!-- Atomic Operations 1 -->
    <tr>
        <td rowspan="2">Atomic Operations</td>
        <td>Batched writes</td>
        <td>–</td>
        <td><pre lang="python">
            my_batch = db.batch()
            my_batch.set(doc_ref, data_dict)
            my_batch.update(doc_ref, data_dict)
            my_batch.delete(doc_ref)
            my_batch.commit()  # Up to 20 document access calls before you have to commit            
        </pre></td>
    </tr>
    <!-- Atomic Operations 2 -->
    <tr>
        <td>Transactions</td>
        <td>–</td>
        <td><pre lang="python">
            @firestore.transactional
            def run_transaction(transaction, doc_ref):
                doc_dict = doc_ref.get(transaction=transaction).to_dict()
                # Do some read that must happen before write
                my_transaction.update(doc_ref, data_dict)
            #
            my_transaction = db.transaction()
            run_transaction(my_transaction, doc_ref)
        </pre></td>
    </tr>
  </table>
