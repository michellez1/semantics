import math

def norm(vec):
    sum_of_squares = 0.0  
    for x in vec:
        sum_of_squares += vec[x] * vec[x]
    return math.sqrt(sum_of_squares)


def cosine_similarity(vec1, vec2): 
    num , den, den1, den2 = 0 ,0, 0, 0
    for k in vec1:
        if k in vec2:
            num += vec1[k] * vec2[k]
    for k in vec1:
        den1 += vec1[k]**2
    for k in vec2:
        den2 += vec2[k]**2
    den = math.sqrt(den1 * den2)
    return num / den
            


def build_semantic_descriptors(sentences): 
    sem_descriptor = {}
    for sentence in sentences:
        sentence = list(set(sentence))
        for word in sentence:
            if word != "":

                if word not in sem_descriptor:
                    sem_descriptor[word] = {}

                for word_comp in sentence:
                        if word_comp != word:
                            if word_comp in sem_descriptor[word]:
                                sem_descriptor[word][word_comp] += 1
                            else:
                                sem_descriptor[word][word_comp] = 1
                    
        
    return sem_descriptor


def build_semantic_descriptors_from_files(filenames): #DONE
    sentences = []
    for file in filenames:
        l = []
        f = open(file, "r").read().lower()

        for punct in [",", "-", "--", ":", ";", '"', "'"]:
            f = f.replace(punct, " ")

        f = f.replace("?", ".").replace("!", ".")

        f = f.split(".")
        for item in f:
           l.append(item.split())
        sentences += l
    return build_semantic_descriptors(sentences)
       

def most_similar_word(word, choices, semantic_descriptors, similarity_fn): 
    results = []
    if word not in semantic_descriptors:
        return []
    for choice in choices:
        if choice not in semantic_descriptors:
            results.append(-1)
        else: 
            results.append(similarity_fn(semantic_descriptors[word], semantic_descriptors[choice]))
    #print(choices[results.index(max(results))])
    return choices[results.index(max(results))]
    

def run_similarity_test(filename, semantic_descriptors, similarity_fn): 
    text = open(filename, "r").read()
    lines = text.split("\n")
    #lines.remove("")
    correct = 0.0
    for i in range(len(lines)):
        if lines[i] == "":
            del lines[i]
    for i in range(len(lines)):
        lines[i] = lines[i].split(" ")
        
        word = lines[i][0]
        ans = lines[i][1]
        choices = lines[i][2:]
    #print(lines)
    
        if most_similar_word(word, choices, semantic_descriptors,similarity_fn) == ans:
            correct += 1

    return correct/len(lines)*100
    
    
    
if __name__ == '__main__':
    sem_descriptors = build_semantic_descriptors_from_files(["war_and_peace.txt", "swanns_way.txt"])
    print(run_similarity_test("test_file_proj3.txt", sem_descriptors, cosine_similarity))
