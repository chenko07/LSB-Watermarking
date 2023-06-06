from PIL import Image

def encode_lsb(image_path, message, key):
    img = Image.open(image_path)
    width, height = img.size
    pixel_map = img.load()

    # Konversi pesan dan kunci ke dalam bentuk biner
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    binary_message += '00000000'  # Tambahkan delimeter agar bisa menghentikan proses ekstraksi
    binary_key = ''.join(format(ord(char), '08b') for char in key)

    # Periksa apakah pesan dapat disembunyikan dalam citra
    max_message_length = width * height * 3
    if len(binary_message) + len(binary_key) > max_message_length:
        raise ValueError("Pesan terlalu panjang untuk diwatermarking dalam citra ini.")

    index = 0
    for y in range(height):
        for x in range(width):
            r, g, b = pixel_map[x, y]

            # Ubah bit terakhir menjadi bit pesan atau kunci
            if index < len(binary_message):
                r = (r & 0xFE) | int(binary_message[index])
                index += 1
            elif index < len(binary_message) + len(binary_key):
                r = (r & 0xFE) | int(binary_key[index - len(binary_message)])
                index += 1

            pixel_map[x, y] = (r, g, b)

    # Simpan citra yang telah diwatermarking
    encoded_image_path = 'encoded_image.png'
    img.save(encoded_image_path)
    print("Citra berhasil diwatermarking dan disimpan sebagai encoded_image.png")

def decode_lsb(encoded_image_path, key):
    img = Image.open(encoded_image_path)
    width, height = img.size
    pixel_map = img.load()

    binary_message = ""
    binary_key = ''.join(format(ord(char), '08b') for char in key)
    key_index = 0
    for y in range(height):
        for x in range(width):
            r, _, _ = pixel_map[x, y]

            # Ekstrak bit terakhir dari pesan atau kunci
            if key_index < len(binary_key):
                binary_message += bin(r)[-1]
                key_index += 1
            else:
                break

    # Pisahkan pesan dari delimeter
    binary_message = binary_message.rstrip('0')
    split_message = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]

    # Konversi biner ke karakter
    message = ""
    for binary in split_message:
        char = chr(int(binary, 2))
        message += char

    return message

# Menggunakan fungsi encode_lsb untuk menerapkan watermarking pada citra
image_path = 'gambar.jpg'
message = "jul"
key = "R"

encode_lsb(image_path, message, key)

print("Citra sebelum diwatermarking:")
before_img = Image.open(image_path)
before_img.show()

# Tampilkan citra sebelum dan sesudah diwatermarking
print("Citra setelah diwatermarking:")
after_img = Image.open('encoded_image.png')
after_img.show()

# Menggunakan fungsi decode_lsb untuk mengekstraksi pesan dari citra yang telah diwatermarking
print("Langkah-langkah dekripsi:")
decode_lsb('encoded_image.png', key)

# Menggunakan fungsi decode_lsb untuk mengekstraksi pesan dari citra yang telah diwatermarking
decoded_message = decode_lsb('encoded_image.png', key)
print("Pesan yang diekstraksi: ", decoded_message)
