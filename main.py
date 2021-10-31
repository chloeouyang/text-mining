import random
import string


def read_data(filename='SMSSpamCollection.txt'):
    """
    Read the SMS Spam collection file and return the ham and spam text list.
    """
    # I got a UnicodeDecodeError here and the encoding type is learned from:
    # https://stackoverflow.com/questions/28165639/unicodedecodeerror-gbk-codec-cant-decode-byte-0x80-in-position-0-illegal-mult
    f = open(filename, encoding='utf-8')
    hams = list()
    spams = list()

    for line in f:
        line = line.strip()
        if line[0] == 'h':
            hams.append(line[4:])
        else:
            spams.append(line[5:])

    return hams, spams


def test_split(text_list, test_rate=0.2):
    """
    Randomly split the text list to test and train list with some specific rate.
    """
    random.shuffle(text_list)
    split_point = test_rate * len(text_list)
    split_point = int(split_point)

    test_text_list = text_list[:split_point]
    train_text_list = text_list[split_point:]

    return test_text_list, train_text_list


def frequency_dictionary(data_list):
    """
    Compute the word frequency in all text list.
    Every text in the data_list is a list composed of words.
    """
    d = dict()
    total = 0
    for data in data_list:
        for word in data:
            cnt = d.get(word, 0)
            d[word] = cnt + 1
            total += 1

    for key, values in d.items():
        d[key] = values / total
    return d


def preprocess(text_list):
    """
    Preprocess the text list:
        - Split every text into word list.
        - Delete punctuations in the text.
        - Lower every word.
        - Do some stuffs to numbers.
        - Recognize the web url.
    """
    data_list = list()
    for text in text_list:
        # https://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string
        text = text.translate(str.maketrans('', '', string.punctuation))

        temp_list = list()
        for word in text.split(' '):
            if not word:
                continue
            word = word.lower()

            if '£' in word:
                word = 'PRICE'

            elif word.isnumeric():
                if len(word) == 1:
                    word = 'SINGAL'
                elif len(word) <= 6:
                    word = 'PRICE'
                else:
                    word = 'PHONE'

            elif word[0:3] == 'www' or word[-3:] == 'com' or word[
                    0:4] == 'http':
                word = 'URL'

            temp_list.append(word)
        data_list.append(temp_list)

    return data_list


def compare(ham_freq, spam_freq, data_list, threshold=1.0):
    """
    Compare every text in the data_list with ham_frequency and spam_frequency
    dictionary, so we can infer that whether the text is a spam text.
    """
    ans = list()
    for data in data_list:
        ham_prob = 0.0
        spam_prob = 0.0
        for word in data:
            ham_prob += ham_freq.get(word, 0.0)
            spam_prob += spam_freq.get(word, 0.0)
        ans.append(spam_prob > ham_prob * threshold)
    return ans


def top_k(freq_dict, k=10):
    """
    Return the top k-th frequency in the given freq dictionary.
    """
    sorted_freq = sorted(freq_dict.items(), key=lambda kv: kv[1], reverse=True)
    for key, values in sorted_freq[:k]:
        print(f"{key}: {values}")


def main():
    # Read data from file and split them into train set and test set.
    hams, spams = read_data()
    ham_test, ham_train = test_split(hams)
    spam_test, spam_train = test_split(spams)

    # Proprocess the raw text into data form and generate frequency dict.
    ham_freq = frequency_dictionary(preprocess(ham_train))
    spam_freq = frequency_dictionary(preprocess(spam_train))

    # Preporcess the test set
    ham_data_test, spam_data_test = preprocess(ham_test), preprocess(spam_test)

    # Inference
    ham_ans = compare(ham_freq, spam_freq, ham_data_test)
    spam_ans = compare(ham_freq, spam_freq, spam_data_test)

    print('---------- TEST ACCURACY ----------')
    print(f"ham text accuracy is {1-sum(ham_ans)/len(ham_ans)}")
    print(f"spam text accuracy is {sum(spam_ans)/len(spam_ans)}")
    print(
        f"total accuracy is {(len(ham_ans)-sum(ham_ans)+sum(spam_ans))/(len(ham_ans)+len(spam_ans))}"
    )

    # Threshold
    ham_ans = compare(ham_freq, spam_freq, ham_data_test, 1.1)
    spam_ans = compare(ham_freq, spam_freq, spam_data_test, 1.1)

    print()
    print('---------- THRESHOLD ACCURACY ----------')
    print(f"ham text accuracy with threshold is {1-sum(ham_ans)/len(ham_ans)}")
    print(
        f"spam text accuracy with threshold is {sum(spam_ans)/len(spam_ans)}")
    print(
        f"total accuracy with threshold is {(len(ham_ans)-sum(ham_ans)+sum(spam_ans))/(len(ham_ans)+len(spam_ans))}"
    )

    print()
    print('---------- HAM TOP 10 FREQ ----------')
    top_k(ham_freq)
    print()
    print('---------- SPAM TOP 10 FREQ ----------')
    top_k(spam_freq)


if __name__ == '__main__':
    # ---------- just for testing ----------
    # hams, spams = read_data()
    # assert len(hams) == 4827
    # assert len(spams) == 747
    # test, train = test_split(spams)
    # print(len(test))
    # print(len(train))
    # data_list = preprocess(test)
    # for data in data_list:
    #     print(data)
    # spam_freq = frequency_dictionary(data_list)
    # print(spam_freq)

    main()
