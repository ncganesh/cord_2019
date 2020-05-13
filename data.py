from sentence_transformers import SentenceTransformer
import scipy.spatial
import pandas as pd
import joblib
embedder = SentenceTransformer('bert-base-nli-mean-tokens')
import dash_html_components as html


meddfr = pd.read_csv('/home/gn/semanticsearch/data/cord2019.csv')
corpus = meddfr['body_text'].values.tolist()

corpus_embeddings = joblib.load('/home/gn/semanticsearch/hap_semanticsearch/corpus_embeddingsfilfull.sav')
#filename = 'corpus_embeddings.sav'
#joblib.dump(corpus_embeddings, filename)


def get_similar_sentences(queries):
    query_embeddings = embedder.encode(queries)

    closest_n = 5
    res=[]
    rows=[]
    for query, query_embedding in zip(queries, query_embeddings):
        distances = scipy.spatial.distance.cdist([query_embedding], corpus_embeddings, "cosine")[0]

        results = zip(range(len(distances)), distances)
        results = sorted(results, key=lambda x: x[1])

        print("\n\n======================\n\n")
        print("Query:", query)
        print("\nTop 5 most similar sentences from similar")

        for idx, distance in results[0:closest_n]:
            #print(meddfr['paper_id'][idx],meddfr['url'][idx],meddfr['url'][idx],meddfr['abstract'][idx], "(Score: %.4f)" % (1-distance))
            res.append([meddfr['title'][idx],meddfr['url'][idx],meddfr['publish_time'][idx], "(Score: %.4f)" % (1-distance)])
    df = pd.DataFrame(res,columns = ['title','url','publish_date','score'])
    return df