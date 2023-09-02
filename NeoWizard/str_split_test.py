def split_string(input_str):
    if len(input_str) <= 600:
        return [input_str]

    max_length = 500
    sentences = input_str.split("\n")
    result = []

    temp_str = ""
    for sentence in sentences:
        if len(temp_str) + len(sentence) + 1 <= max_length:
            temp_str += sentence + "\n"
        else:
            result.append(temp_str.strip())
            temp_str = sentence + "\n"

    result.append(temp_str.strip())
    return result

res = split_string("To solve the given problem, let's use the information provided:\n\nWe are given that the sum of the real part and the imaginary part of a complex number z is 2. Let's denote the real part as a and the imaginary part as b. Therefore, we have a + b = 2.\n\nWe are also given that (2 + i)z is a real number. Here, i represents the imaginary unit. Multiplying a complex number by a real number only affects its magnitude, not its imaginary part. Therefore, we can write the equation as:\n\n(2 + i)z = 2z + iz = Re(2z) + Im(2z)i = a' + b'i,\n\nwhere a' and b' are the real and imaginary parts of the complex number (2 + i)z, respectively.\n\nSince (2 + i)z is a real number, the imaginary part b' must be equal to zero. This implies that b = 0, and from the first equation a + b = 2, we can conclude that a = 2.\n\nSo, we have found that the real part a is equal to 2 and the imaginary part b is equal to 0 for the complex number z. Therefore, z can be written as z = 2 + 0i, which simplifies to z = 2.\n\nThe modulus (or absolute value) of a complex number is the distance between the number and the origin on the complex plane. It can be calculated using the formula: |z| = √(a^2 + b^2), where a and b are the real and imaginary parts, respectively.\n\nIn this case, the modulus of z can be calculated as |z| = √(2^2 + 0^2) = √4 = 2.\n\nHence, the modulus of the complex number z is 2.")

for r in res:
    print(r)
    print("-----")

str1 = ""
str1 += "abc"
str1 +="\ncde\n"
print(str1)