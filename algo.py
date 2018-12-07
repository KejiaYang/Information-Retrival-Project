import collections
import math
import nltk
import operator
import pickle

import dataset as ds

# list_of_resumes_dict, list_of_resumes = ds.return_all(94123, 40, True)

# with open('list_of_resumes.pkl', 'wb') as f:
# 	pickle.dump(list_of_resumes, f)

# with open('list_of_resumes_dict.pkl', 'wb') as f:
# 	pickle.dump(list_of_resumes_dict, f)

class DocInfo():
	def __init__(self, list_of_resumes):
		self.resumes = [i.lower() for i in list_of_resumes]
		self.inverted_index = collections.defaultdict(lambda: collections.defaultdict(int))		
		self.all_terms = set()
		self.num_terms = 0
		# corpus_term_count: number of times a term appears in all resumes
		self.corpus_term_count = collections.defaultdict(int)
		# num_docs: total number of documents in the index
		self.num_docs = len(list_of_resumes)
		# doc_count: number of documents a term appears in
		self.doc_count = collections.defaultdict(int)		
		# doc_size: number of terms in the current document
		self.doc_size = collections.defaultdict(int)
		# avg_dl: average document length of all resumes
		self.avg_dl = 0

	def generate_inverted_index(self):
		for idx, r in enumerate(self.resumes):
			words = r.split()
			self.avg_dl += len(words)
			self.doc_size[idx] = len(set(words))
			for w in words:
				self.inverted_index[w][idx] += 1

	def get_all_terms(self):
		self.all_terms = set(self.inverted_index.keys())
		self.num_terms = len(self.all_terms)

	def get_corpus_term_count(self):
		for w in self.all_terms:
			self.corpus_term_count[w] = sum(self.inverted_index[w].values())

	def get_doc_count(self):
		for w in self.all_terms:
			self.doc_count[w] = len(self.inverted_index[w].keys())

    # could improve by incrementing avg_dl
	def get_avg_dl(self):
		self.avg_dl = 1.0 * self.avg_dl / len(self.resumes)

	def get_all_info(self):
		self.generate_inverted_index()
		self.get_all_terms()
		self.get_corpus_term_count()
		self.get_doc_count()
		self.get_avg_dl()

	def bm25(self, current_doc_idx, query_w, query_term_count, s=0.1):
		idf_up = self.num_docs + 1
		idf_down = (self.doc_count[query_w] + 1) # smoothed
		ntf_up = 1 + math.log(1 + math.log(self.inverted_index[query_w][current_doc_idx] + 1)) # smoothed
		ntf_down = 1 - s + s * (1.0 * self.doc_size[current_doc_idx] / self.avg_dl)
		qtf = query_term_count
		score = math.log(1.0 * idf_up / idf_down) * (1.0 * ntf_up / ntf_down) * qtf
		return score

	def method2(self, current_doc_idx, query_w, query_term_count, k1 = 1.2, b = 0.75, k3 = 500):
		ictf = math.log(1.0 * self.num_terms / (self.corpus_term_count[query_w] + 1)) # smoothed
		idf = math.log((self.num_docs - self.doc_count[query_w] + 0.5) / (self.doc_count[query_w] + 0.5))
		poisson_df = 1 - k1 ** (1.0 * -(self.corpus_term_count[query_w] + 1) / self.num_docs) # smoothed
		poisson_ctf = -math.log(1 - 1.0 * (self.doc_count[query_w] + 1) / self.num_docs) # smoothed
		pidf = math.log(1.0 * poisson_df / poisson_ctf + 1)
		bidf = ictf * idf * pidf
		
		tf_up = (k1 + 1) * (self.inverted_index[query_w][current_doc_idx] + 1) # smoothed
		tf_down = k1 * (1 - b + b * 1.0 * self.doc_size[query_w] / self.avg_dl) + (self.inverted_index[query_w][current_doc_idx] + 1) # smoothed
		TF = 1.0 * tf_up / tf_down

		qtf_up = (k3 + 1) * query_term_count
		qtf_down = k3 + query_term_count		
		QTF = 1.0 * qtf_up / qtf_down

		score = bidf * TF * QTF
		return score

def retrieval(query):
	with open('list_of_resumes.pkl', 'rb') as f:
		list_of_resumes = pickle.load(f)
	f.close()

	with open('list_of_resumes_dict.pkl', 'rb') as f:
		list_of_resumes_dict = pickle.load(f)
	f.close()

	sd = DocInfo(list_of_resumes)
	sd.get_all_info()

	query = query.lower()

	query_words = query.split()
	
	bm25_scores = []
	method2_scores = []

	for r_idx, r in enumerate(sd.resumes):
		bm25score = 0
		method2score = 0
		for query_w in query_words:
			query_term_count = query_words.count(query_w)
			bm25score += sd.bm25(r_idx, query_w, query_term_count)
			method2score += sd.method2(r_idx, query_w, query_term_count)
		bm25_scores.append((r_idx, bm25score))
		method2_scores.append((r_idx, method2score))

	bm25_scores = sorted(bm25_scores, key=operator.itemgetter(1), reverse=True)
	method2_scores = sorted(method2_scores, key=operator.itemgetter(1), reverse=True)

	bm25_ranking = [i[0] for i in bm25_scores]
	method2_ranking = [i[0] for i in method2_scores]

	return list_of_resumes_dict, bm25_ranking, method2_ranking

# with open('list_of_resumes.pkl', 'rb') as f:
	# list_of_resumes = pickle.load(f)

resumes_dict, bm25, method2 = retrieval('yingchen')
print(len(resumes_dict))

# print(resumes_dict[bm25[0]]["educations"][0]["school"])
