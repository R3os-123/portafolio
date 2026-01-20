import base64

n_b64 = "sNYuG6mp-PGaUzzpab1AwLJx4R19sY3OYcA-0vJ1ng4g97z20OQW6rwFDRQSGcFFmn_c4biPxP7XZ0an9NJKu4QTnaDeVrtPsbngRyXtaOrpclFSSoWEP5NWlXfP89mwVlNBn6OlFkK0o1t_rit6RV2wteEEpp6tOC2O1dW2rMSzQNkWb8N1b5dW_MtljS-KhEq1tYcZST6zwB2neXCrPsIUrGy54nP97cOqA2OMeNStaLXCDr8rSzEdydy05p_KWZXjOCs7ufwJDnNy2nUcxgz7JfCKLYbzZ8_72ZSm4bLO_7AnTPmC7m8zsRZ69UxmLlq4dhXImkx8Ky2MaCB2IQ"
e_b64 = "AQAB"

def b64url_decode(data):
    data += '=' * (4 - len(data) % 4)
    return base64.urlsafe_b64decode(data)

def encode_length(length):
    if length <= 127:
        return bytes([length])
    else:
        l_bytes = length.to_bytes((length.bit_length() + 7) // 8, 'big')
        return bytes([0x80 | len(l_bytes)]) + l_bytes

def to_asn1_int(data):
    if data[0] > 127:
        data = b'\x00' + data
    return b'\x02' + encode_length(len(data)) + data

n_bytes = b64url_decode(n_b64)
e_bytes = b64url_decode(e_b64)

rsa_pub_key_content = to_asn1_int(n_bytes) + to_asn1_int(e_bytes)
rsa_pub_key = b'\x30' + encode_length(len(rsa_pub_key_content)) + rsa_pub_key_content

header = b'\x30\x0d\x06\x09\x2a\x86\x48\x86\xf7\x0d\x01\x01\x01\x05\x00'
bit_string = b'\x03' + encode_length(len(rsa_pub_key) + 1) + b'\x00' + rsa_pub_key
full_der = b'\x30' + encode_length(len(header + bit_string)) + header + bit_string

print("-----BEGIN PUBLIC KEY-----")
print(base64.b64encode(full_der).decode())
print("-----END PUBLIC KEY-----")
