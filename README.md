# JWT_ES256_dpop

This is the command to Generate Key Pair

#Generate a private key for signature signing key
openssl ecparam -name prime256v1 -genkey -noout -out dpop-key.pem

#Generate a public key for signature verification key (it may not need in my code because in the code already get directly from private)
openssl ec -in dpop-key.pem -pubout -out dpop-public-key.pem
