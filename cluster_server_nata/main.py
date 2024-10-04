import json
#import nltk
#import math

from sklearn.feature_extraction.text import CountVectorizer
#import pandas as pd

#import numpy as np
import sklearn
from sklearn.cluster import KMeans
from sklearn.cluster import MiniBatchKMeans
from sklearn.cluster import AgglomerativeClustering


def get_stems_frequency(vector_list, count_words_in_text):
    # преобразование numpy.int64 во numpy.float64
    # vector_list = np.float64(vector_list)

    i = 0
    for vector in vector_list:
        j = 0
        count_text = count_words_in_text[i]
        for elem_vector in vector:
            if elem_vector != 0:
                frequency = round(elem_vector / count_text * 100, 3)
                #vector_list[vector][elem_vector]
                vector_list[i][j] = frequency
            j = j + 1
        i = i + 1

    return vector_list


def Create_Bag_of_Words(documents):
    # Design the Vocabulary
    # The default token pattern removes tokens of a single character. That's why we don't have the "I" and "s" tokens in the output
    count_vectorizer = CountVectorizer()

    # Create the Bag-of-Words Model
    bag_of_words = count_vectorizer.fit_transform(documents)
    bag = bag_of_words.toarray()
    # print(bag)

    # bag_with_frequency = get_stems_frequency(bag, count_words_in_text) 1111

    # Show the Bag-of-Words Model as a pandas DataFrame
    feature_names = count_vectorizer.get_feature_names()  # названия стемм

    # df = pd.DataFrame(bag_with_frequency, columns=feature_names) 11111
    # print(df)
    # названия строк: номер строки соответствует индексу данного текста в массиве
    # названия столбцов: неповторяющиеся стеммы
    # return bag_with_frequency
    return bag


def cluster_kmeans(count_clusters, bag):
    kmeans = KMeans(n_clusters=count_clusters, random_state=0).fit(bag)
    clusters_list = kmeans.labels_
    return clusters_list


def cluster_miniBatchKMeans(count_clusters, bag):
    mbk = MiniBatchKMeans(n_clusters=count_clusters,
                          random_state=0,
                          batch_size=6)
    #mbk.fit_transform(bag)
    mbk.fit(bag)
    clusters_list = mbk.labels_
    return clusters_list


def cluster_agglomerativeClustering(count_clusters, bag):
    agglomer = AgglomerativeClustering(n_clusters=count_clusters).fit(bag)
    clusters_list = agglomer.labels_
    return clusters_list


def distribute_texts_on_clusters(clusters_list, hash_list):
    # создание списка списков
    # кластер 1 [hash1, hash3]
    # кластер 2 [hash2]
    list_clusters = init_list_of_objects(count_clusters)
    for i in range(len(clusters_list)):
        cluster = int(clusters_list[i])
        hash = hash_list[i]
        #col = len(list_clusters[cluster])
        list_clusters[cluster].append(hash)
    return list_clusters


def init_list_of_objects(size):
    list_of_objects = list()
    for i in range(0, size):
        list_of_objects.append(list())  #different object reference each time
    return list_of_objects


def result_kmeans(bag):
    res = "Метод K-means.\n\n"
    kmeans = cluster_kmeans(count_clusters, bag)
    clusters_kmeans = distribute_texts_on_clusters(kmeans, hash_list)
    result = clusters_kmeans
    # result = serialize(clusters_kmeans, res)
    return result


def result_mbk(bag):
    res = "Метод Mini batch K-means.\n\n"
    mbk = cluster_miniBatchKMeans(count_clusters, bag)
    clusters_mbk = distribute_texts_on_clusters(mbk, hash_list)
    result = clusters_mbk
    # result = serialize(clusters_mbk, res)
    return result


def result_agglomerat(bag):
    res = "Agglomerative Clustering.\n\n"
    agglomerat = cluster_agglomerativeClustering(count_clusters, bag)
    clusters_agglomerat = distribute_texts_on_clusters(agglomerat, hash_list)
    result = clusters_agglomerat
    #result = serialize(clusters_agglomerat, res)
    return result


def all_methods(bag):
    result = []
    result.append(result_kmeans(bag))
    result.append(result_agglomerat(bag))
    result.append(result_mbk(bag))
    return result


w = ['dsd s dsd rrr', 'dsd dsdd dsd rrr', 'dsd dsdd dsd rrr', 'kkk ttt aaa']

a_path = "C:\\Users\Max\Documents\GitHub\cluster_server\preparedArticles.json"
id_path = "C:\\Users\Max\Documents\GitHub\cluster_server\preparedIds.json"


def load_data(path):
    with open(path, "r", encoding="utf-8") as read_file:
        data = json.load(read_file)
    return data


data = load_data(a_path)
#print(data[0])

bag = Create_Bag_of_Words(data)
#print(bag)

hash_list = load_data(id_path)
out  = []
count_clusters = 8
res = result_kmeans(bag)
out.append(res)
#print(res)
res = result_mbk(bag)
out.append(res)
#print(res)
res = result_agglomerat(bag)
out.append(res)
#print(res)
with open('./clusters.json', "w") as file:
    json.dump(out, file)

print('1')
