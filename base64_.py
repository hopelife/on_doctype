# # https://github.com/dougn/python-plantuml

# import base64
# # ## encode
# # mytext = "This is my secret text"
# # encoded=(base64.b64encode(mytext.encode('ascii')))
# # encoded_ascii=encoded.decode('ascii')
# # print(encoded_ascii)  # VGhpcyBpcyBteSBzZWNyZXQgdGV4dA==


# ## decode
# # base64_text = "VGhpcyBpcyBteSBzZWNyZXQgdGV4dA=="
# # decoded = base64.b64decode(base64_text.encode('ascii'))
# # decoded_ascii=decoded.decode('ascii')
# # print(decoded_ascii)


# ## NOTE: encode plantuml
# uml = """@startuml
# Alice -> Bob: Authentication Request
# Bob --> Alice: Authentication Response
# @enduml"""

# # CkBzdGFydHVtbApBbGljZSAtPiBCb2I6IEF1dGhlbnRpY2F0aW9uIFJlcXVlc3QKQm9iIC0tPiBBbGljZTogQXV0aGVudGljYXRpb24gUmVzcG9uc2UKQGVuZHVtbAo=
# # http://www.plantuml.com/plantuml/svg/CkBzdGFydHVtbApBbGljZSAtPiBCb2I6IEF1dGhlbnRpY2F0aW9uIFJlcXVlc3QKQm9iIC0tPiBBbGljZTogQXV0aGVudGljYXRpb24gUmVzcG9uc2UKQGVuZHVtbAo=

# # QHN0YXJ0dW1sCkFsaWNlIC0+IEJvYjogQXV0aGVudGljYXRpb24gUmVxdWVzdApCb2IgLS0+IEFsaWNlOiBBdXRoZW50aWNhdGlvbiBSZXNwb25zZQpAZW5kdW1s
# # https://kroki.io/plantuml/svg/CkBzdGFydHVtbApBbGljZSAtPiBCb2I6IEF1dGhlbnRpY2F0aW9uIFJlcXVlc3QKQm9iIC0tPiBBbGljZTogQXV0aGVudGljYXRpb24gUmVzcG9uc2UKQGVuZHVtbAo=
# # encoded=(base64.b64encode(uml.encode("utf-8")))
# # encoded_utf=encoded.decode("utf-8")
# # print(encoded_utf)



# Forked from https://gist.github.com/dyno/94ef6bb9644a88d6981d6a1a9eb70802
# https://plantuml.com/text-encoding
# https://github.com/dougn/python-plantuml/blob/master/plantuml.py#L64

import zlib
import base64
import string

plantuml_alphabet = string.digits + string.ascii_uppercase + string.ascii_lowercase + '-_'
base64_alphabet = string.ascii_uppercase + string.ascii_lowercase + string.digits + '+/'
b64_to_plantuml = bytes.maketrans(base64_alphabet.encode('utf-8'), plantuml_alphabet.encode('utf-8'))
plantuml_to_b64 = bytes.maketrans(plantuml_alphabet.encode('utf-8'), base64_alphabet.encode('utf-8'))


def plantuml_encode(plantuml_text):
    """zlib compress the plantuml text and encode it for the plantuml server"""
    zlibbed_str = zlib.compress(plantuml_text.encode('utf-8'))
    compressed_string = zlibbed_str[2:-4]
    return base64.b64encode(compressed_string).translate(b64_to_plantuml).decode('utf-8')


def plantuml_decode(plantuml_url):
    """decode plantuml encoded url back to plantuml text"""
    data = base64.b64decode(plantuml_url.translate(plantuml_to_b64).encode("utf-8"))
    dec = zlib.decompressobj()  # without check the crc.
    header = b'x\x9c'
    return dec.decompress(header + data).decode("utf-8")


url = "SyfFKj2rKt3CoKnELR1Io4ZDoSa700=="

print(plantuml_decode(url))
print(plantuml_encode(plantuml_decode(url)))