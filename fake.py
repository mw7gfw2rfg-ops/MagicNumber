# Program to create a 'fake' PNG file that is actually empty
# PNG magic number is 89 50 4E 0D 0A 1A 0A

magic_bytes = bytes.fromhex("89504E470D0A1A0A")

with open("fake_image.png", 'wb') as f:
    f.write(magic_bytes)
    f.write(b'This is not actually an image, but the header says it is!')

print("Created an image with a valid PNG header")