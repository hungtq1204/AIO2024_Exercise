import streamlit as st


def initialize_matrix(row, column):
    # Tạo ma trận 2 chiều
    matrix = [[0] * column for _ in range(row)]

    # Đặt giá trị đầu tiên của ma trận
    for i in range(row):
        matrix[i][0] = i
    for j in range(column):
        matrix[0][j] = j

    return matrix


def char_compare(c1, c2):
    if c1 == c2:
        return 0
    else:
        return 1


def levenshtein(s1, s2):
    # Đảm bảo s1 luôn lớn hơn s2
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    # Tính số hàng và cột của ma trân levelshtein
    row = len(s1) + 1
    column = len(s2) + 1

    # Thiết lập ma trânk
    matrix = initialize_matrix(row, column)

    # Tính các giá trị còn lại cho ma trận
    for r in range(1, row):
        for c in range(1, column):
            matrix[r][c] = min(
                matrix[r - 1][c] + 1,
                matrix[r][c - 1] + 1,
                matrix[r - 1][c - 1] + char_compare(s1[r - 1], s2[c - 1]))

    return matrix[row - 1][column - 1]


def load_vocab(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        words = sorted(set([line.strip().lower() for line in lines]))
    return words


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    vocabs = load_vocab(file_path='./vocab.txt')

    st.title("Word Correction using Levenshtein Distance")
    word = st.text_input('Word:')

    if st.button("Compute"):
        leven_distances = dict()
        for vocab in vocabs:
            leven_distances[vocab] = levenshtein(word, vocab)

        # Sắp xếp các từ theo khoảng cách
        sorted_distances = dict(sorted(leven_distances.items(), key=lambda item: item[1]))
        correct_word = list(sorted_distances.keys())[0]
        st.write('Correct word: ', correct_word)

        col1, col2 = st.columns(2)
        col1.write('Vocabulary:')
        col1.write(vocabs)

        col2.write('Distances:')
        col2.write(sorted_distances)
