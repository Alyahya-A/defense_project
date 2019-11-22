from django.shortcuts import render
from numpy.compat import long


def home(request):
    selected_type = request.POST.get('select', None)
    key = (request.POST.get('key', None))
    if key is not None:
        key = int(key)
    text = request.POST.get('message', None)
    context = {
        'first_time': True,
        'selected_type': selected_type,
        'input_message': text,
    }

    print(selected_type)
    print(key)
    print(text)

    if selected_type == 'encryption':
        cipher_text, matrix = encrypt(text, key)
        print(cipher_text)
        context['first_time'] = False
        context['output_message'] = cipher_text
        context['table'] = matrix

    elif selected_type == 'decryption':
        plain_text, matrix = decrypt(text, key)
        context['first_time'] = False
        context['output_message'] = plain_text
        context['table'] = matrix

    return render(request, 'defense_app/home.html', context)


# m value is depand if is en or de. if en: m=plain_text, if de: m=text range.
def rail_fence(m, key):

    # Generate matrix
    matrix = [[None for x in range(len(m))] for y in range(int(key))]

    r1 = list(range(key - 1))
    r2 = list(range(key - 1, 0, -1))
    rails = r1 + r2

    # 1-Put the number or char in his place
    for n, x in enumerate(m):
        matrix[rails[n % len(rails)]][n] = x
    # The matrix will be number if it was De, and letter if it was En.

    return matrix


def encrypt(plain_text, key):

    matrix = rail_fence(plain_text, key)
    cipher_text = ''
    x = 0
    for lis in matrix:  # x
        y = 0
        for elm in lis:  # y
            if elm is None:
                matrix[x][y] = ''

            elif elm != '':
                cipher_text += elm
            y += 1
        x += 1

    print('The Cipther Text is: {}'.format(cipher_text))
    return cipher_text, matrix


def decrypt(cipher_text, key):
    text_range = range(len(cipher_text))

    # 1-
    matrix = rail_fence(text_range, key)

    # 2-
    x = 0
    y = 0
    index = 0

    for lis in matrix:  # x
        y = 0
        for elm in lis:  # y
            if elm is None:
                matrix[x][y] = ''

            # Reaplace the number(1) with char (from the cipher text)
            # 1- The number came from the range of cipther text. (text_range)
            elif elm != '':
                matrix[x][y] = cipher_text[index]
                index += 1
            y += 1
        x += 1

    # بعد ما سويت ماتركس ورتبت الارقام فيها (بشكل تنازلي وتصاعدي في خطوة 1)
    # وحوّلت الارقام الى حروف بناء على موقعا في السايفر تكست في خطوة 2
    # Now read the matrix. Ex: [0,0] + [1,1] + [2,2].. and so on.

    plain_text = ''
    row = 0

    for col in text_range:

        if row == 0:
            go_back = False

        elif row == key:
            if not go_back:
                row -= 2
                go_back = True

        plain_text += matrix[row][col]

        if go_back:
            row -= 1

        elif not go_back:
            row += 1

    print('The Plain Text is: {}'.format(plain_text))
    return plain_text, matrix
